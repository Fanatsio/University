import os
import random
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import shutil

# ================== НАСТРОЙКИ ==================
SRC_ROOT = Path("CN_dataset_obj_detection")
OUT_ROOT = Path("dataset")  # итоговый датасет

IMG_SIZE = 640
MAX_IMAGES = 2000

NEGATIVE_PROB = 0.4        # вероятность кадра без монеты
SAMPLES_PER_IMAGE = 2

MIN_SCALE = 0.15
MAX_SCALE = 0.7

BG_MIN = 160
BG_MAX = 255

ROTATE_RANGE = (-25, 25)
BRIGHTNESS_RANGE = (0.7, 1.3)
CONTRAST_RANGE = (0.7, 1.3)

BLUR_PROB = 0.3
NOISE_PROB = 0.3

VAL_SPLIT = 0.1
TEST_SPLIT = 0.1
# ===============================================

# создаём папки
for split in ["train", "val", "test"]:
    (OUT_ROOT / "images" / split).mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "labels" / split).mkdir(parents=True, exist_ok=True)

def list_images(root):
    exts = (".jpg", ".jpeg", ".png")
    images = []
    for d in root.iterdir():
        if d.is_dir():
            for f in d.iterdir():
                if f.suffix.lower() in exts:
                    images.append(f)
    return images

def add_noise(img):
    arr = np.array(img).astype(np.float32)
    noise = np.random.normal(0, 8, arr.shape)
    arr = np.clip(arr + noise, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))

def make_background():
    gray = random.randint(BG_MIN, BG_MAX)
    bg = np.full((IMG_SIZE, IMG_SIZE, 3), gray, dtype=np.uint8)
    return Image.fromarray(bg)

def process_negative(split, out_id):
    bg = make_background()
    img_name = f"{out_id:06d}.jpg"
    lbl_name = f"{out_id:06d}.txt"
    bg.save(OUT_ROOT / "images" / split / img_name, quality=95)
    open(OUT_ROOT / "labels" / split / lbl_name, "w").close()  # пустая аннотация
    return True

def process_positive(img_path, split, out_id):
    try:
        coin = Image.open(img_path).convert("RGBA")
    except Exception:
        return False

    bg = make_background()

    # масштаб
    scale = random.uniform(MIN_SCALE, MAX_SCALE)
    new_w = int(coin.width * scale)
    new_h = int(coin.height * scale)
    coin = coin.resize((new_w, new_h), Image.BICUBIC)

    # поворот
    angle = random.uniform(*ROTATE_RANGE)
    coin = coin.rotate(angle, expand=True)

    new_w, new_h = coin.size

    # позиция
    x = random.randint(-new_w // 3, IMG_SIZE - new_w // 3)
    y = random.randint(-new_h // 3, IMG_SIZE - new_h // 3)

    bg.paste(coin, (x, y), coin)

    # bbox
    x1 = max(x, 0)
    y1 = max(y, 0)
    x2 = min(x + new_w, IMG_SIZE)
    y2 = min(y + new_h, IMG_SIZE)

    if x2 <= x1 or y2 <= y1:
        return False

    # аугментации сцены
    if random.random() < BLUR_PROB:
        bg = bg.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 2.0)))
    if random.random() < NOISE_PROB:
        bg = add_noise(bg)
    bg = ImageEnhance.Brightness(bg).enhance(random.uniform(*BRIGHTNESS_RANGE))
    bg = ImageEnhance.Contrast(bg).enhance(random.uniform(*CONTRAST_RANGE))

    # YOLO bbox
    xc = ((x1 + x2) / 2) / IMG_SIZE
    yc = ((y1 + y2) / 2) / IMG_SIZE
    w = (x2 - x1) / IMG_SIZE
    h = (y2 - y1) / IMG_SIZE

    img_name = f"{out_id:06d}.jpg"
    lbl_name = f"{out_id:06d}.txt"

    bg.convert("RGB").save(OUT_ROOT / "images" / split / img_name, quality=95)
    with open(OUT_ROOT / "labels" / split / lbl_name, "w") as f:
        f.write(f"0 {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")

    return True

def main():
    images = list_images(SRC_ROOT)
    print(f"Исходных изображений монет: {len(images)}")

    out_id = 0
    while out_id < MAX_IMAGES:
        # определяем split
        r = random.random()
        if r < TEST_SPLIT:
            split = "test"
        elif r < TEST_SPLIT + VAL_SPLIT:
            split = "val"
        else:
            split = "train"

        # негатив
        if random.random() < NEGATIVE_PROB:
            process_negative(split, out_id)
            out_id += 1
            continue

        img = random.choice(images)
        ok = process_positive(img, split, out_id)
        if ok:
            out_id += 1

        if out_id % 100 == 0:
            print(f"Сгенерировано: {out_id}")

    print(f"ГОТОВО. Всего изображений: {out_id}")

if __name__ == "__main__":
    main()
