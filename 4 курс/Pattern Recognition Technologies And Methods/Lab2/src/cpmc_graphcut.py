import numpy as np
import maxflow
import math
import cv2
import random
from src.cpmc_superpixels import chi2_distance, superpixel_histograms

def build_graph_and_cut(segments, mean_color, adjacency, seed_label, lam=1.0, use_color_unary=True, boundary_seeds=None, image_shape=None, histograms=None):
    """
    Расширенная реализация GraphCut с поддержкой разных типов унарных термов
    как описано в статье CPMC (раздел 3.1)
    """
    n = mean_color.shape[0]
    
    # Инициализация графа
    g = maxflow.Graph[float]()
    node_ids = g.add_nodes(n)
    
    # Pairwise terms (smoothness) с использованием контрастных границ
    for i, neighbors in adjacency.items():
        for j in neighbors:
            if j <= i:  # Избегаем дублирования ребер
                continue
            # Вычисляем вес на основе цветового различия
            diff = np.linalg.norm(mean_color[i] - mean_color[j])
            w = np.exp(-(diff**2) / (2 * (1.0**2))) # Изменено σ на 5.0
            g.add_edge(int(i), int(j), float(w), float(w))
    
    # Unary terms (data cost)
    if use_color_unary:
        # Цветовые унарные термы как в статье (раздел 3.1)
        seed_hist = histograms[seed_label]
        dists = np.array([chi2_distance(histograms[i], seed_hist) for i in range(n)])

        sigma = np.std(dists) + 1e-6
        fgScore = np.exp(-(dists**2) / (2 * sigma**2))
    else:
        # Равномерные унарные термы
        fgScore = np.ones(n) * 0.5
    
    # Обработка фоновых сидов (для subframe-CPMC)
    bg_penalty = np.ones(n)
    if boundary_seeds is not None and image_shape is not None:
        h, w = image_shape
        for i in range(n):
            if i in boundary_seeds:
                bg_penalty[i] = 0.1  # Низкий штраф для пикселей у границы
            else:
                # Пространственный штраф, зависящий от расстояния до границы
                coords = np.where(segments == i)
                if len(coords[0]) > 0:
                    cy, cx = int(coords[0].mean()), int(coords[1].mean())
                    dist_to_boundary = min(cx, w-cx, cy, h-cy)
                    bg_penalty[i] = 0.1 + 0.9 * (dist_to_boundary / max(h, w))
    
    for i in range(n):
        # Комбинированный унарный терм
        src = lam * (1 - fgScore[i]) * bg_penalty[i]  # Стоимость подключения к источнику (фону)
        sink = lam * fgScore[i]  # Стоимость подключения к стоку (объекту)
        
        # Принудительно относим seed суперпиксель к переднему плану
        if i == seed_label:
            src = 1e-6
            sink = 1e3
        
        g.add_tedge(int(i), float(src), float(sink))
    
    # Вычисляем максимальный поток/минимальный разрез
    try:
        g.maxflow()
    except Exception as e:
        print(f"Maxflow error: {e}")
        # Возвращаем пустую маску в случае ошибки
        return np.zeros(segments.shape, dtype=bool)
    
    # Получаем метки сегментации (0 = источник/фон, 1 = сток/объект)
    labels = np.array([g.get_segment(i) for i in range(n)], dtype=bool)
    mask = np.isin(segments, np.where(labels)[0])
    
    # Обрабатываем пустые маски путем инвертирования
    if mask.sum() == 0:
        labels = ~labels
        mask = np.isin(segments, np.where(labels)[0])
    
    # Фильтрация по связности компонентов (раздел 3.4 статьи)
    num_labels, labeled_mask = cv2.connectedComponents(mask.astype(np.uint8))
    if num_labels > 2:  # Есть фон + несколько компонентов объекта
        # Находим самый большой компонент (исключая фон)
        component_sizes = [np.sum(labeled_mask == i) for i in range(1, num_labels)]
        if component_sizes:
            largest_component = np.argmax(component_sizes) + 1
            mask = (labeled_mask == largest_component)
    
    return mask.astype(bool)