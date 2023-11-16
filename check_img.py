import cv2
import os
import numpy as np
import keras.utils as image
from PIL import Image

root_dir = os.getcwd()

def img_process(picture):
    try:
        img = image.load_img(root_dir + "\\" + picture, target_size=(24, 24), color_mode="grayscale")
    except:
        img = cv2.imread(root_dir + "\\" + picture, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (24, 24))
    img = image.img_to_array(img)
    img = img.reshape(24, 24)
    return img

class P():
    def __init__(self, check, img_array, img_name):
        self.check = check
        self.img_array = img_array
        self.img_name = img_name

img_temp = []
count = 1
img_name = input("輸入圖片名稱 : ")
for pictures in os.listdir(root_dir):
    if pictures.endswith(".jpg") or pictures.endswith(".png") or pictures.endswith(".JPG") or pictures.endswith(".PNG") or pictures.endswith(".jfif") or pictures.endswith(".jpeg"):
        print(f"\r前處理第 {count} 張圖片中", end = '', flush = True)
        img_array = img_process(pictures)
        img_temp.append(P(False, img_array, pictures))
        count += 1

print("\n圖片總數 : ", len(img_temp))

index = 1
name = 1
del_count = 0
show_del_img = input("是否顯示被刪除的圖片(y/n) : ")
if show_del_img != "y" and show_del_img != "n":
    while(True):
        show_del_img = input("是否顯示被刪除的圖片(y/n) : ")
        if show_del_img == "y" or show_del_img == "n":
            break
        else:
            continue
for img in img_temp:
    for check_img in img_temp[index:]:
        if check_img.check == False:
            different = cv2.subtract(img.img_array, check_img.img_array)
            result = not np.any(different)
            if result == True:
                check_img.check = True
                if show_del_img == "y":
                    try:
                        open_img = Image.open(check_img.img_name)
                        open_img.show()
                    except:
                        open_img = cv2.imread(check_img.img_name)
                        cv2.imshow("remove_img", open_img)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                elif show_del_img == "n":
                    pass
                os.remove(check_img.img_name)
                del_count += 1

    if img.check == False:
        if img.img_name.endswith(".png") or img.img_name.endswith(".PNG"):
            os.rename(img.img_name, img_name + str(name) + ".png")
        else:
            os.rename(img.img_name, img_name + str(name) + ".jpg")
        print(f"\r檢查第 {name} 張", end = '', flush = True)
        name += 1
    index += 1
    img.check = True

print("\n重複的張數 : ", del_count)

