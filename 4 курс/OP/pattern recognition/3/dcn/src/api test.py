import mmcv
from mmdet.apis import init_detector, inference_detector
from mmdet.registry import VISUALIZERS
from mmdet.utils import register_all_modules

register_all_modules()

# Конфиг и чекпоинт DCN v1
config = '../mmdetection/configs/dcn/faster-rcnn_r50-dconv-c3-c5_fpn_1x_coco.py'
checkpoint = '../mmdetection/checkpoints/faster_rcnn_r50_fpn_dconv_c3-c5_1x_coco_20200130-d68aed1e.pth'

# Путь к изображению
img_path = '../img/2.jpg'

# Инициализация модели
model = init_detector(config, checkpoint, device='cpu')

# Инференс
result = inference_detector(model, img_path)

# Визуализация
visualizer = VISUALIZERS.build(model.cfg.visualizer)
visualizer.dataset_meta = model.dataset_meta

img = mmcv.imread(img_path)
img = mmcv.imconvert(img, 'bgr', 'rgb')

# Сохраняем результат в ../img/dcn_result.jpg
visualizer.add_datasample(
    'dcn_result',
    img,
    data_sample=result,
    draw_gt=False,
    show=False,  # не открываем окно
    out_file='../img/dcn_result2.jpg'
)

print("DCN результат сохранён в ../img/dcn_result.jpg")
