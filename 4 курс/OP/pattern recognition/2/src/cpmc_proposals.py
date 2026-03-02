import os
import csv
import numpy as np
import cv2
import random
from collections import namedtuple
from multiprocessing import Pool, cpu_count

from src.cpmc_superpixels import compute_superpixels, superpixel_stats, superpixel_adjacency, grid_seeds, subframe_seeds
from src.cpmc_graphcut import build_graph_and_cut
from src.cpmc_superpixels import superpixel_histograms
from src.cpmc_superpixels import chi2_distance

Proposal = namedtuple("Proposal", ["mask", "bbox", "score", "area", "energy"])

# =====================================================================
# ГЛОБАЛЬНЫЕ переменные, которые будут видны всем воркерам multiprocessing
# =====================================================================

_global_segments = None
_global_mean_color = None
_global_histograms = None
_global_adjacency = None
_global_img_shape = None


def _worker_init(segments, mean_color, histograms, adjacency, img_shape):
    """
    Инициализация воркера.
    Все данные загружаются в глобальные переменные процесса,
    чтобы не передавать гигантские массивы в каждую задачу.
    """
    global _global_segments, _global_mean_color, _global_histograms
    global _global_adjacency, _global_img_shape

    _global_segments = segments
    _global_mean_color = mean_color
    _global_histograms = histograms
    _global_adjacency = adjacency
    _global_img_shape = img_shape


def _run_single_seed(task):
    """
    Задача для одного вызова GraphCut:
    task = (seed_label, lam, use_color, boundary_seeds)
    """
    seed_label, lam, use_color, boundary_seeds = task

    try:
        m = build_graph_and_cut(
            _global_segments,
            _global_mean_color,
            _global_adjacency,
            seed_label,
            lam=lam,
            use_color_unary=use_color,
            boundary_seeds=boundary_seeds,
            histograms=_global_histograms,
            image_shape=_global_img_shape
        )
        return m
    except Exception as e:
        print(f"GraphCut error seed={seed_label}, lam={lam}: {e}")
        return None


def mask_bbox(mask):
    ys, xs = np.where(mask)
    if xs.size == 0:
        return (0,0,0,0)
    return (int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1))


def score_mask(mask):
    return float(mask.sum() / (mask.size + 1e-6))


def iou(a, b):
    inter = np.logical_and(a,b).sum()
    union = np.logical_or(a,b).sum()
    return inter / union if union > 0 else 0.0


def dedup(masks, thr=0.9):
    out = []
    for m in masks:
        ok = True
        for k in out:
            if iou(m, k) > thr:
                ok = False
                break
        if ok:
            out.append(m)
    return out


def calculate_energy(mask, segments, mean_color, adjacency):
    labels = np.unique(segments[mask])
    boundary_edges = 0
    internal_edges = 0

    for i in labels:
        if i not in adjacency:
            continue
        for j in adjacency[i]:
            if j in labels:
                internal_edges += 1
            else:
                boundary_edges += 1

    if boundary_edges + internal_edges == 0:
        return 0.0

    return boundary_edges / (boundary_edges + internal_edges)


def generate_proposals(
    img,
    image_name,
    out_dir,
    n_segments=800,
    compactness=7,
    grid_step=50,
    lam_values=[0.05,0.1,0.2,0.5,1,2,5,10],
    top_k=200,
    use_subframes=True,
    workers=1
):
    h, w = img.shape[:2]

    # 1 — суперпиксели
    # segments = compute_superpixels(img, n_segments=n_segments, compactness=compactness)
    segments = compute_superpixels(img)

    # 2 — статистики и смежности
    adjacency = superpixel_adjacency(segments)
    mean_color = superpixel_stats(img, segments)
    histograms = superpixel_histograms(img, segments, bins=16)

    # 3 — сиды
    seeds = grid_seeds(segments, step=grid_step)

    # 4 — subframes
    subframe_seeds_list  = []
    if use_subframes:
        subframe_seeds_list  = subframe_seeds(segments)

    # ============================================================
    # Подготовим задачи для multiprocessing
    # ============================================================
    tasks = []

    # Grid seeds
    for s in seeds:
        for lam in lam_values:
            for use_color in [True, False]:
                tasks.append((s, lam, use_color, None))

    # Subframe seeds
    for s, boundary in subframe_seeds_list :
        for lam in lam_values:
            for use_color in [True, False]:
                tasks.append((s, lam, use_color, boundary))

    print(f"Total GC tasks: {len(tasks)}")

    # ============================================================
    # Параллельный запуск GraphCut
    # ============================================================
    if workers > 1:
        print(f"Running GraphCut with {workers} workers...")
        with Pool(
            processes=workers,
            initializer=_worker_init,
            initargs=(segments, mean_color, histograms, adjacency, (h, w))
        ) as pool:
            results = pool.map(_run_single_seed, tasks)
    else:
        # без параллелизма
        _worker_init(segments, mean_color, histograms, adjacency, (h, w))
        results = [_run_single_seed(t) for t in tasks]

    # Отфильтровываем пустые
    masks = [m for m in results if m is not None and m.sum() > 0]

    print(f"Valid segments: {len(masks)}")

    # dedup
    masks = dedup(masks)
    print(f"After dedup: {len(masks)}")

    # фильтр по размеру
    min_size = 0.01 * h * w
    max_size = 0.7 * h * w
    masks_filtered = [m for m in masks if min_size <= m.sum() <= max_size]
    masks = masks_filtered
    print(f"After size filtering: {len(masks)}")

    # энергия
    energies = [calculate_energy(m, segments, mean_color, adjacency) for m in masks]

    # proposals
    props = []
    for m, e in zip(masks, energies):
        bbox = mask_bbox(m)
        score = score_mask(m)
        area = m.sum()
        props.append(Proposal(m, bbox, score, area, e))

    # сортировка по энергии
    props.sort(key=lambda p: p.energy)
    props = props[:top_k]

    # запись файлов
    base = os.path.splitext(image_name)[0]
    csv_path = os.path.join(out_dir, f"{base}_proposals.csv")

    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id","x","y","w","h","score","area","energy","mask_file","crop"])
        for i, p in enumerate(props):
            x,y,ww,hh = p.bbox
            crop = img[y:y+hh, x:x+ww]
            crop_path = os.path.join(out_dir, f"{base}_crop_{i:03d}.jpg")
            mask_path = os.path.join(out_dir, f"{base}_mask_{i:03d}.png")

            cv2.imwrite(crop_path, crop)
            cv2.imwrite(mask_path, (p.mask*255).astype(np.uint8))

            w.writerow([
                i, x, y, ww, hh,
                p.score, p.area, p.energy,
                os.path.basename(mask_path),
                os.path.basename(crop_path)
            ])

    print(f"Saved {len(props)} proposals")
    return props
