import cv2
import numpy as np
from skimage.segmentation import slic
from skimage.color import rgb2lab

#new
def superpixel_histograms(img, segments, bins=16):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
    n = segments.max() + 1
    hists = np.zeros((n, bins*3), float)

    for i in range(n):
        mask = (segments == i)
        pixels = lab[mask]

        # 3 гистограммы по каналам L,a,b
        h1, _ = np.histogram(pixels[:,0], bins=bins, range=(0,255), density=True)
        h2, _ = np.histogram(pixels[:,1], bins=bins, range=(0,255), density=True)
        h3, _ = np.histogram(pixels[:,2], bins=bins, range=(0,255), density=True)

        hists[i] = np.concatenate([h1,h2,h3])

    return hists

def chi2_distance(h1, h2):
    num = (h1 - h2) ** 2
    denom = h1 + h2 + 1e-6
    return 0.5 * np.sum(num / denom)


# from skimage.segmentation import felzenszwalb


# def compute_superpixels(img, n_segments=400, compactness=10):
#     rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     seg = slic(rgb, n_segments=n_segments, compactness=compactness, start_label=0, sigma=1)
#     return seg.astype(np.int32)

from skimage.segmentation import felzenszwalb

def compute_superpixels(img, scale=100, sigma=0.5, min_size=50):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    segments = felzenszwalb(rgb, scale=scale, sigma=sigma, min_size=min_size)
    return segments.astype(np.int32)

def superpixel_adjacency(segments):
    h, w = segments.shape
    adj = {}
    for y in range(h):
        for x in range(w):
            a = segments[y, x]
            if x + 1 < w:
                b = segments[y, x+1]
                if a != b:
                    adj.setdefault(a, set()).add(b)
                    adj.setdefault(b, set()).add(a)
            if y + 1 < h:
                c = segments[y+1, x]
                if a != c:
                    adj.setdefault(a, set()).add(c)
                    adj.setdefault(c, set()).add(a)
    return adj

def superpixel_stats(img, segments):
    lab = rgb2lab(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    n = segments.max() + 1
    mean_color = np.zeros((n, 3), float)
    counts = np.zeros(n, int)

    h, w = segments.shape
    for y in range(h):
        for x in range(w):
            lbl = segments[y, x]
            mean_color[lbl] += lab[y, x]
            counts[lbl] += 1

    for i in range(n):
        if counts[i] > 0:
            mean_color[i] /= counts[i]
    return mean_color

def grid_seeds(segments, step=50):
    h, w = segments.shape
    xs = range(step//2, w, step)
    ys = range(step//2, h, step)

    seeds = []
    seen = set()

    for y in ys:
        for x in xs:
            if y < h and x < w:
                lbl = int(segments[y, x])
                if lbl not in seen:
                    seen.add(lbl)
                    seeds.append(lbl)
    return seeds

def subframe_seeds(segments, grid_size=4, subframe_ratio=0.4):
    """
    Генерация subframe seeds как описано в разделе 5.3 статьи CPMC
    """
    h, w = segments.shape
    subframe_width = int(w * subframe_ratio)
    subframe_height = int(h * subframe_ratio)
    
    seeds = []
    seen = set()
    
    # Создаем сетку subframes
    for y in range(0, h - subframe_height, subframe_height // 2):
        for x in range(0, w - subframe_width, subframe_width // 2):
            # Определяем центр subframe
            cx = x + subframe_width // 2
            cy = y + subframe_height // 2
            
            # Проверяем, чтобы центр был в пределах изображения
            if cy >= h or cx >= w:
                continue
                
            # Получаем метку суперпикселя в центре
            seed_label = int(segments[cy, cx])
            
            # Определяем фоновые сиды (все пиксели за пределами subframe)
            boundary_seeds = set()
            for yy in range(h):
                for xx in range(w):
                    if xx < x or xx >= x + subframe_width or yy < y or yy >= y + subframe_height:
                        boundary_seeds.add(int(segments[yy, xx]))
            
            if seed_label not in seen:
                seen.add(seed_label)
                seeds.append((seed_label, boundary_seeds))
    
    return seeds