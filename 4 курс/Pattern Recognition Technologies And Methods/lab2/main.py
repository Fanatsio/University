import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

folder_path = './image/'

image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg'))]

for image_file in image_files:
    image_path = os.path.join(folder_path, image_file)

    img = mpimg.imread(image_path)

    plt.imshow(img)
    plt.title(image_file)
    plt.axis('off')
    plt.show()
