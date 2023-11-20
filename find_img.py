import os
import cv2
import numpy as np

root_dir = os.getcwd()
find_img = input("輸入檔名 : ")
path = os.path.join("./del_images", find_img)
file_extension = ["jpg", "JPG", "jpeg", "jfif", "png", "PNG"]


def img_to_array(image):
    s = 300
    img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (s, s))
    img = img.reshape(s, s)
    return img


find_img_array = img_to_array(path)
result = False

for img in os.listdir(root_dir):
    if os.path.isfile(os.path.join(root_dir, img)):
        if img.split(".")[1] in file_extension and img.split(".")[1] == find_img.split(".")[1]:
            print(f"配對 : {img}")
            LO_img_array = img_to_array(img)
            different = cv2.subtract(find_img_array, LO_img_array)
            result = not np.any(different)
            if result:
                print('\nFind.\t', img)
                break
if not result:
    print("Not find.")
