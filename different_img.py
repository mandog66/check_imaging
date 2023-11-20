import os
import cv2
import numpy as np


def img_to_array(image):
    s = 300
    img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (s, s))
    img = img.reshape(s, s)
    return img


a_name = "del_img_1.jpg"
b_name = "LO_1238.png"
a_path = os.path.join("./del_images", a_name)

a_array = img_to_array(a_path)
b_array = img_to_array(b_name)

different = cv2.subtract(a_array, b_array)
result = not np.any(different)

if result:
    print("Same img.")
else:
    print("Different img.")

# a_img = cv2.imread(a_path)
# b_img = cv2.imread(b_name)
# cv2.imshow("1", a_img)
# cv2.imshow("2", b_img)
# cv2.waitKey(0)
