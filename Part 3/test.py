import cv2
import numpy as np

# Load the image
image = cv2.imread("images/0_mnist.png", cv2.IMREAD_GRAYSCALE)

# Resize the image to 32x32 pixels with padding 0
desired_size = 32
old_size = image.shape[:2]
ratio = float(desired_size) / max(old_size)
new_size = tuple([int(x * ratio) for x in old_size])
image = cv2.resize(image, (new_size[1], new_size[0]))

delta_w = desired_size - new_size[1]
delta_h = desired_size - new_size[0]
top, bottom = delta_h // 2, delta_h - (delta_h // 2)
left, right = delta_w // 2, delta_w - (delta_w // 2)
image = cv2.copyMakeBorder(
    image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0
)

# Save the resized image
cv2.imwrite("resized_image.png", image)
