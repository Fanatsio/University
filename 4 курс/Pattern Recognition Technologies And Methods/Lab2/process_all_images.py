import os
import subprocess
import glob
import tempfile
import shutil
from PIL import Image
import xml.etree.ElementTree as ET
import cv2
import numpy as np

MAX_SIDE = 640

def parse_voc_xml(xml_path):
    """Парсит VOC XML и возвращает боксы ТОЛЬКО для кошек в формате (xmin, ymin, xmax, ymax)"""
    if not os.path.exists(xml_path):
        return []
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        boxes = []
        for obj in root.findall('object'):
            name = obj.find('name').text
            if name is None:
                continue
            if name.strip().lower() == 'cat':
                bndbox = obj.find('bndbox')
                xmin = int(float(bndbox.find('xmin').text))
                ymin = int(float(bndbox.find('ymin').text))
                xmax = int(float(bndbox.find('xmax').text))
                ymax = int(float(bndbox.find('ymax').text))
                boxes.append((xmin, ymin, xmax, ymax))
        return boxes
    except Exception as e:
        print(f"Ошибка парсинга XML {xml_path}: {e}")
        return []

def visualize_gt_on_resized(img_resized, gt_boxes, output_path):
    """Рисует GT-боксы НА УМЕНЬШЕННОМ ИЗОБРАЖЕНИИ"""
    img_cv = cv2.cvtColor(np.array(img_resized), cv2.COLOR_RGB2BGR)
    color = (0, 200, 255)  # Оранжевый в BGR
    
    for i, (x1, y1, x2, y2) in enumerate(gt_boxes):
        cv2.rectangle(img_cv, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            img_cv, 
            f"GT Cat #{i+1}", 
            (x1, max(20, y1-5)), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.6, 
            color, 
            2
        )
    
    cv2.imwrite(output_path, img_cv)
    print(f"GT-визуализация для уменьшенного изображения сохранена: {output_path}")

def resize_for_cpmc(img, max_side=MAX_SIDE):
    w, h = img.size
    scale = max_side / max(w, h)
    if scale >= 1.0:
        return img.copy(), 1.0
    new_w = int(w * scale)
    new_h = int(h * scale)
    return img.resize((new_w, new_h), Image.LANCZOS), scale

def save_temp_resized(img_resized, original_basename):
    tmp_dir = tempfile.mkdtemp(prefix="cpmc_")
    tmp_path = os.path.join(tmp_dir, original_basename)
    img_resized.save(tmp_path, format="JPEG")
    return tmp_path, tmp_dir

def downscale_xml(xml_path, results_subdir, base, scale):
    """
    Масштабирует координаты в XML (xmin/ymin/xmax/ymax).
    Возвращает путь к scaled XML или None.
    """
    if not os.path.exists(xml_path) or scale >= 1.0:
        return None
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        size = root.find('size')
        if size is not None:
            width_node = size.find('width')
            height_node = size.find('height')
            try:
                width_node.text = str(int(int(width_node.text) * scale))
                height_node.text = str(int(int(height_node.text) * scale))
            except Exception:
                pass
        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')
            for tag in ['xmin','ymin','xmax','ymax']:
                node = bndbox.find(tag)
                if node is not None:
                    node.text = str(int(float(node.text) * scale))
        scaled_xml_path = os.path.join(results_subdir, f"{base}_scaled.xml")
        tree.write(scaled_xml_path)
        return scaled_xml_path
    except Exception as e:
        print(f"Ошибка обработки XML: {e}")
        return None

def process_images():
    os.makedirs("results", exist_ok=True)
    image_files = glob.glob("images/*.jpg") + glob.glob("images/*.jpeg") + glob.glob("images/*.png")
    
    if not image_files:
        print("Нет изображений в папке 'images'!")
        return
    
    print(f"Найдено изображений: {len(image_files)}")
    
    for i, image_path in enumerate(sorted(image_files)):
        print(f"\n[{i+1}/{len(image_files)}] Обработка: {image_path}")
        base = os.path.splitext(os.path.basename(image_path))[0]
        results_subdir = os.path.join("results", base)
        os.makedirs(results_subdir, exist_ok=True)
        
        # 1. Загружаем изображение
        img = Image.open(image_path).convert("RGB")
        
        # 2. Уменьшаем только для CPMC
        img_resized, scale = resize_for_cpmc(img)
        
        # 3. Обрабатываем XML (оригинал лежит в images/<base>.xml)
        xml_path = os.path.join("images", f"{base}.xml")
        scaled_xml_path = downscale_xml(xml_path, results_subdir, base, scale)
        
        # 4. ВИЗУАЛИЗАЦИЯ GT НА УМЕНЬШЕННОМ ИЗОБРАЖЕНИИ (если есть)
        if scaled_xml_path and os.path.exists(scaled_xml_path):
            gt_boxes = parse_voc_xml(scaled_xml_path)
            if gt_boxes:
                # parse_voc_xml возвращает (xmin, ymin, xmax, ymax) — для визуализации используем этот формат
                gt_vis_path = os.path.join(results_subdir, f"{base}_resized_gt_visualization.jpg")
                visualize_gt_on_resized(img_resized, gt_boxes, gt_vis_path)
        
        # 5. Сохраняем во временную папку и запускаем CPMC
        tmp_resized_path, tmp_dir = save_temp_resized(img_resized, os.path.basename(image_path))
        try:
            subprocess.run([
                "python", "run_cpmc.py",
                tmp_resized_path,
                "--out", results_subdir,
                "--nseg", "1000",
                "--compact", "6",
                "--grid", "30",
                "--topk", "200",
                "--workers", "8"
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Ошибка CPMC: {e}")
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
    
    # Запускаем классификацию
    print("\nЗапуск классификации...")
    try:
        subprocess.run(["python", "classify_proposals.py"], check=True)
        print("Классификация завершена!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка классификации: {e}")

if __name__ == "__main__":
    process_images()
