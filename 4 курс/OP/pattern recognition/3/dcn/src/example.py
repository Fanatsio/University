import torch
from torchvision.ops import DeformConv2d
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


IMAGE_PATH = "../img/2010_003781.jpg"
OUTPUT_FEATURE = "../img/dcn_output.png"

# --- Загружаем изображение ---
img = Image.open(IMAGE_PATH).convert("RGB")
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])
x = transform(img).unsqueeze(0)  # [1, 3, H, W]

# --- Слой DeformConv2d ---
dcn = DeformConv2d(
    in_channels=3,
    out_channels=16,  # больше каналов для выявления признаков
    kernel_size=3,
    padding=1
)

# --- Генерация случайных offsets ---
offset = torch.randn(1, 2*3*3, x.shape[2], x.shape[3])

# --- Прямой проход ---
y = dcn(x, offset)  # [1, 16, H, W]

# --- Усреднение каналов для наглядного отображения ---
y_mean = y.mean(dim=1, keepdim=True)  # [1, 1, H, W]

# --- Нормализация для визуализации ---
y_vis = y_mean.squeeze().detach().numpy()
y_vis = (y_vis - np.min(y_vis)) / (np.max(y_vis) - np.min(y_vis))

# --- Сохраняем и отображаем результат ---
plt.figure(figsize=(6,6))
plt.imshow(y_vis, cmap='gray')
plt.axis('off')
plt.savefig(OUTPUT_FEATURE, bbox_inches='tight')
plt.show()

print("Output shape:", y.shape)
print(f"Результат сохранён в {OUTPUT_FEATURE}")
