import os
import glob
import xml.etree.ElementTree as ET
from PIL import Image

# Максимальный размер стороны
MAX_SIDE = 1100

def resize_for_scale(img, max_side=MAX_SIDE):
    w, h = img.size
    scale = max_side / max(w, h)
    if scale >= 1.0:
        return 1.0
    return scale

def downscale_xml(xml_path, results_dir, base, scale):
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

        out_path = os.path.join(results_dir, f"{base}_scaled.xml")
        tree.write(out_path)
        return out_path
    except Exception as e:
        print(f"Ошибка обработки XML {xml_path}: {e}")
        return None

def process_for_scaled_xml():
    os.makedirs("scaled_xml", exist_ok=True)

    image_files = glob.glob("images/*.jpg") + glob.glob("images/*.jpeg") + glob.glob("images/*.png")
    if not image_files:
        print("Нет изображений в папке 'images'!")
        return

    print(f"Найдено изображений: {len(image_files)}")

    for img_path in sorted(image_files):
        base = os.path.splitext(os.path.basename(img_path))[0]
        print(f"Обработка: {base}")

        xml_path = os.path.join("images", f"{base}.xml")
        if not os.path.exists(xml_path):
            print("  Нет XML, пропускаю")
            continue

        img = Image.open(img_path).convert("RGB")
        scale = resize_for_scale(img)

        subdir = os.path.join("scaled_xml", base)
        os.makedirs(subdir, exist_ok=True)

        out_path = downscale_xml(xml_path, subdir, base, scale)
        if out_path:
            print(f"  Создан scaled.xml: {out_path}")
        else:
            print("  Масштабирование не требуется (scale >= 1)")

if __name__ == "__main__":
    process_for_scaled_xml()
