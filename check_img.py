import cv2
import os
import numpy as np
import keras.utils as image

root_dir = os.getcwd()
try:
    os.makedirs("del_images")
    print("del_images folder be created")
except OSError:
    print("del_images folder already exist")


def img_process(picture):
    # 圖片前置處理
    img = cv2.imread(picture, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (24, 24))
    img = image.img_to_array(img)
    img = img.reshape(24, 24)
    return img


class P():
    # 圖片資訊
    def __init__(self, check, img_array, img_name, img_format):
        self.check = check
        self.img_array = img_array
        self.img_name = img_name
        self.img_format = img_format


img_temp = []   # 圖片物件陣列
count = 1   # 圖片張數
file_extension = ["jpg", "JPG", "jpeg", "jfif", "png", "PNG"]   # 副檔名

img_name = input("輸入圖片名稱 : ")

# 圖片前處理後放到圖片物件陣列
for pictures in os.listdir(root_dir):
    if os.path.isfile(os.path.join(root_dir, pictures)):
        if pictures.split(".")[1] in file_extension:
            print(f"\r前處理第 {count} 張圖片中", end='', flush=True)
            img_array = img_process(pictures)
            img_format = pictures.split(".")[1]
            img_temp.append(P(False, img_array, pictures, img_format))
            count += 1

print("\n圖片總數 : ", len(img_temp))

index = 1   # 切割圖片物件陣列
name = 1    # 圖片檔名
del_count = 0   # 重複圖片的數量

# 重複的圖片要不要顯示
# show_del_img = input("是否顯示被刪除的圖片(y/n) : ")
# if show_del_img != "y" and show_del_img != "n":
#     while (1):
#         show_del_img = input("是否顯示被刪除的圖片(y/n) : ")
#         if show_del_img == "y" or show_del_img == "n":
#             break
#         else:
#             print("再輸入一次(y/n) : ")
#             continue

# 檢查有沒有重複的圖片
# img 是要檢查的圖片
# check_img 是要比對的圖片
for img in img_temp:
    for check_img in img_temp[index:]:
        if check_img.check == False:
            different = cv2.subtract(img.img_array, check_img.img_array)
            result = not np.any(different)
            if result == True:
                check_img.check = True
                del_img = cv2.imread(check_img.img_name)
                cv2.imwrite("./del_images/del_img_{}.{}".format(
                    del_count + 1, check_img.img_format))

                # 刪除圖片備份到 del_images
                # if show_del_img == "y":
                #     del_img = cv2.imread(check_img.img_name)
                #     cv2.imwrite("./del_images/del_img_{}.{}".format(
                #         del_count + 1, check_img.img_format))
                # elif show_del_img == "n":
                #     pass

                # 刪除圖片
                os.remove(check_img.img_name)
                del_count += 1

    # 更改圖片名字
    if img.check == False:
        if img.img_name.endswith(".png") or img.img_name.endswith(".PNG"):
            os.rename(img.img_name, img_name + str(name) + ".png")
        else:
            os.rename(img.img_name, img_name + str(name) + ".jpg")
        print(f"\r檢查第 {name} 張", end='', flush=True)
        name += 1
    index += 1
    img.check = True

print("\n重複的張數 : ", del_count)
