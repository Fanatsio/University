import os
import mmcv
from mmdet.apis import init_detector, inference_detector
from mmdet.registry import VISUALIZERS
from mmdet.utils import register_all_modules
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

register_all_modules()

config = './mmdetection/configs/dcn/faster-rcnn_r50-dconv-c3-c5_fpn_1x_coco.py'
checkpoint = './mmdetection/checkpoints/faster_rcnn_r50_fpn_dconv_c3-c5_1x_coco_20200130-d68aed1e.pth'

input_img_dir = Path('./images')
output_dir = Path('./results')
output_dir.mkdir(parents=True, exist_ok=True)

image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}

image_files = [
    f for f in input_img_dir.iterdir()
    if f.is_file() and f.suffix.lower() in image_extensions
]

if not image_files:
    print(f"Нет изображений в папке {input_img_dir}")
    exit()

print("Загрузка модели...")
model = init_detector(config, checkpoint, device='cpu')
print("Модель загружена.")

model.cfg.visualizer.save_dir = str(output_dir)
visualizer = VISUALIZERS.build(model.cfg.visualizer)
visualizer.dataset_meta = model.dataset_meta

for img_path in image_files:
    print(f"Обработка: {img_path.name}")

    result = inference_detector(model, str(img_path))

    img = mmcv.imread(str(img_path))
    img = mmcv.imconvert(img, 'bgr', 'rgb')

    out_file = output_dir / f"{img_path.stem}_det{img_path.suffix}"

    visualizer.add_datasample(
        name=img_path.stem,
        image=img,
        data_sample=result,
        draw_gt=False,
        show=False,
        out_file=str(out_file)
    )

print(f"\n✅ Обработка завершена. Результаты сохранены в: {output_dir.resolve()}")