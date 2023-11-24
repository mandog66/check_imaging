import shutil
import cv2
import os
import numpy as np
import re
from typing import Tuple
import time

root_dir = os.getcwd()

# 被刪除圖片的備份資料夾
try:
    os.makedirs("del_images")
    print("del_images 資料夾已創建完成\n")
except OSError:
    print("del_images 資料夾已存在\n")


def img_process(picture: str) -> Tuple[str, np.ndarray]:
    # 圖片前置處理
    img_size = 1000
    img = cv2.imread(picture, cv2.IMREAD_GRAYSCALE)

    # 檔名有中文
    if img is None:
        tmp = time.strftime("%Y%m%d%H%M%S") + "." + picture.split(".").pop()
        os.rename(picture, tmp)
        picture = tmp
        img = cv2.imread(tmp, cv2.IMREAD_GRAYSCALE)

    img = cv2.resize(img, (img_size, img_size))
    img = img.reshape(img_size, img_size)
    return picture, img


def write_file(n: int, jpg_d: int, jfif_d: int, png_d: int):
    with open("img_name.txt", 'w') as f:
        f.write(str(n) + '\n' + str(jpg_d) + '\n' +
                str(jfif_d) + '\n' + str(png_d))


def read_file() -> Tuple[int, int]:
    if not os.path.exists("img_name.txt"):
        print("img_name.txt 已創建完成\n")
        with open("img_name.txt", 'w') as f:
            n = 1
            jpg_d = 0
            jfif_d = 0
            png_d = 0
            return n, jpg_d, jfif_d, png_d

    else:
        print("img_name.txt 已存在\n")
        with open("img_name.txt", 'r') as f:
            n = int(f.readline())
            jpg_d = int(f.readline())
            jfif_d = int(f.readline())
            png_d = int(f.readline())
            return n, jpg_d, jfif_d, png_d


class P():
    # 圖片資訊
    def __init__(self, check, img_array, img_name, img_format):
        self.check = check
        self.img_array = img_array
        self.img_name = img_name
        self.img_format = img_format


# 圖片前處理計時
s_time = time.process_time()

img_dict = {"jpg": {"exist_img": [], "uncheck_img": []}, "jfif": {
    "exist_img": [], "uncheck_img": []}, "png": {"exist_img": [], "uncheck_img": []}}   # 圖片物件陣列

count = 1   # 圖片張數
file_extension = ["jpg", "JPG", "jpeg", "jfif", "png", "PNG"]   # 副檔名
m = re.compile('LO_\d+.\w+')    # 檢查固定檔名

# 圖片前處理後放到圖片物件陣列
for pictures in os.listdir(root_dir):
    if os.path.isfile(os.path.join(root_dir, pictures)):
        if pictures.split(".").pop() in file_extension:
            print(f"前處理第 {count} 張圖片中", end='\r', flush=True)
            pictures, img_array = img_process(pictures)
            img_format = pictures.split(".").pop()

            # 依照圖片副檔名分類
            if img_format in ["jpg", "JPG", "jpeg"]:
                img_cls = "jpg"
            elif img_format in ["jfif"]:
                img_cls = "jfif"
            elif img_format in ["png", "PNG"]:
                img_cls = "png"
            else:
                print("Can't find img_cls.")

            # 再依照圖片檔名分類
            if m.match(pictures) != None:
                img_dict[img_cls]["exist_img"].append(
                    P(True, img_array, pictures, img_format))
            else:
                img_dict[img_cls]["uncheck_img"].append(
                    P(False, img_array, pictures, img_format))

            count += 1

print(f"\n\n圖片總數 : {count - 1}\n\
      \n已檢查的 jpg 圖片 : {len(img_dict['jpg']['exist_img'])}\n未檢查的 jpg 圖片 : {len(img_dict['jpg']['uncheck_img'])}\n\
      \n已檢查的 jfif 圖片 : {len(img_dict['jfif']['exist_img'])}\n未檢查的 jfif 圖片 : {len(img_dict['jfif']['uncheck_img'])}\n\
      \n已檢查的 png 圖片 : {len(img_dict['png']['exist_img'])}\n未檢查的 png 圖片 : {len(img_dict['png']['uncheck_img'])}\n\
      \n開始檢查!!\n")

e_time = time.process_time()
print(f"\n圖片前處理花費 {e_time - s_time} 秒\n")

# 圖片檢查計時
s_time = time.process_time()

cname, cjpg_d, cjfif_d, cpng_d = read_file()    # 記錄中的尾數
name, jpg_d, jfif_d, png_d = 1, cjpg_d, cjfif_d, cpng_d  # 顯示在控制台

# 檢查有沒有重複的圖片
# un_img 是要檢查的圖片(新增的)
# ex_img 是要比對的圖片(檢查過的)
for img_d in img_dict:
    for un_img in img_dict[img_d]["uncheck_img"]:
        for ex_img in img_dict[img_d]["exist_img"]:
            different = cv2.subtract(un_img.img_array, ex_img.img_array)
            result = not np.any(different)

            # 找到一樣的圖片
            if result:
                un_img.check = True
                del_img = cv2.imread(un_img.img_name)

                # 備份重複的圖片
                if img_d == "jpg":
                    jpg_d += 1
                    d_img_name = jpg_d
                elif img_d == "jfif":
                    jfif_d += 1
                    d_img_name = jfif_d
                elif img_d == "png":
                    png_d += 1
                    d_img_name = png_d
                else:
                    print("Delete Image Name Failed.")
                shutil.copyfile(
                    un_img.img_name, f"./del_images/del_img_{d_img_name}.{un_img.img_format}")

                # 刪除圖片
                os.remove(un_img.img_name)
                break

        # 更改圖片名字
        if un_img.check == False:
            rename = f"LO_{cname}.{un_img.img_format}"
            os.rename(un_img.img_name, rename)
            img_dict[img_d]["exist_img"].append(
                P(True, un_img.img_array, rename, un_img.img_format))
            cname += 1
        print(f"檢查第 {name} 張", end='\r', flush=True)
        name += 1

# 檔案尾數的紀錄
write_file(cname, jpg_d, jfif_d, png_d)

jpg_d_c = jpg_d - cjpg_d
jfif_d_c = jfif_d - cjfif_d
png_d_c = png_d - cpng_d

print(f"\n檢查完成!!\
      \n新的 jpg 圖片 : {len(img_dict['jpg']['uncheck_img']) - jpg_d_c}\n重複的 jpg 圖片 : {jpg_d_c}\n\
      \n新的 jfif 圖片 : {len(img_dict['jfif']['uncheck_img']) - jfif_d_c}\n重複的 jfif 圖片 : {jfif_d_c}\n\
      \n新的 png 圖片 : {len(img_dict['png']['uncheck_img']) - png_d_c}\n重複的 png 圖片 : {png_d_c}")

e_time = time.process_time()
print(f"\n圖片檢查花費 {e_time - s_time} 秒")
