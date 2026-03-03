import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
import argparse
from PIL import Image
import numpy as np
import torch
from torchvision import transforms
from torchvision import models
import cv2

def get_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input_dir", default="images", help="Папка с изображениями (jpg/png и т.д.)")
    p.add_argument("--output_dir", default="outputs", help="Куда сохранить маски и результаты")
    p.add_argument("--device", default="cpu", help="cpu или cuda")
    p.add_argument("--min_size", type=int, default=640, help="По желанию: минимальная сторона масштабирования (0 — без масштабирования)")
    return p.parse_args()

def random_colors(n, seed=42):
    rng = np.random.RandomState(seed)
    colors = rng.randint(0, 256, size=(n, 3), dtype=np.uint8)
    colors[0] = np.array([0,0,0], dtype=np.uint8)  # класс 0 — фон чёрный
    return colors

def image_paths_from_dir(d):
    exts = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")
    files = [os.path.join(d,f) for f in sorted(os.listdir(d)) if f.lower().endswith(exts)]
    return files

def main():
    args = get_args()
    os.makedirs(args.output_dir, exist_ok=True)

    device = torch.device(args.device if torch.cuda.is_available() and args.device.startswith("cuda") else "cpu")

    # Загрузка предобученной FCN
    model = models.segmentation.fcn_resnet101(pretrained=True)
    model.eval()
    model.to(device)

    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std =[0.229, 0.224, 0.225]),
    ])

    img_paths = image_paths_from_dir(args.input_dir)
    if not img_paths:
        print("Не найдено изображений в", args.input_dir)
        return

    colors = random_colors(256)

    for p in img_paths:
        name = os.path.splitext(os.path.basename(p))[0]
        print("Обработка:", p)
        img = Image.open(p).convert("RGB")
        w, h = img.size

        if args.min_size and min(w, h) < args.min_size:
            scale = args.min_size / min(w, h)
            new_w = int(round(w * scale))
            new_h = int(round(h * scale))
            img = img.resize((new_w, new_h), Image.BILINEAR)
            w, h = img.size

        input_tensor = preprocess(img).unsqueeze(0).to(device)  # 1,C,H,W

        with torch.no_grad():
            out = model(input_tensor)['out']  # shape 1, num_classes, H, W
            # preds: H,W of class indices
            preds = torch.argmax(out.squeeze(0), dim=0).cpu().numpy().astype(np.uint8)

        # Создаем цветную маску
        mask_rgb = colors[preds]  # shape H,W,3
        mask_pil = Image.fromarray(mask_rgb)

        # Сохраняем маску
        mask_path = os.path.join(args.output_dir, f"{name}_mask.png")
        mask_pil.save(mask_path)

        # Создаем оверлей: альфа смешивание
        orig_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        mask_cv = cv2.cvtColor(mask_rgb, cv2.COLOR_RGB2BGR)
        alpha = 0.5
        overlay = cv2.addWeighted(orig_cv, 1.0 - alpha, mask_cv, alpha, 0)
        overlay = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
        overlay_pil = Image.fromarray(overlay)
        overlay_path = os.path.join(args.output_dir, f"{name}_overlay.png")
        overlay_pil.save(overlay_path)

        print("Сохранено:", mask_path, overlay_path)

    print("Готово. Результаты в", args.output_dir)

if __name__ == "__main__":
    main()
