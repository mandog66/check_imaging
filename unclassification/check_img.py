import shutil
import cv2
import os
import numpy as np
import subprocess
import re
from typing import Tuple
import time

root_dir = os.getcwd()

# 被刪除圖片的備份資料夾
try:
    os.makedirs("del_images")
    print("del_images 資料夾已創建完成")
except OSError:
    print("del_images 資料夾已存在")


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


def write_file(n: int, d: int):
    with open("img_name.txt", 'w') as f:
        f.write(str(n)+'\n'+str(d))


def read_file() -> Tuple[int, int]:
    if not os.path.exists("img_name.txt"):
        with open("img_name.txt", 'w') as f:
            n = 1
            d = 0
            return n, d
    else:
        with open("img_name.txt", 'r') as f:
            n = int(f.readline())
            d = int(f.readline())
            return n, d


class P():
    # 圖片資訊
    def __init__(self, check, img_array, img_name, img_format):
        self.check = check
        self.img_array = img_array
        self.img_name = img_name
        self.img_format = img_format


# 圖片前處理計時
s_time = time.process_time()

exist_img = []  # 已經存在的圖片(已檢查)
uncheck_img = []  # 新增的圖片(未檢查)

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

            if m.match(pictures) != None:
                exist_img.append(P(True, img_array, pictures, img_format))
            else:
                uncheck_img.append(P(False, img_array, pictures, img_format))

            count += 1

print(f"\n圖片總數 : {len(exist_img)+len(uncheck_img)}\n已檢查的圖片 : {len(exist_img)}\n未檢查的圖片 : {len(uncheck_img)}\n開始檢查!!")

e_time = time.process_time()
print(f"\n圖片前處理花費 {e_time - s_time} 秒\n")

# 圖片檢查計時
s_time = time.process_time()

cname, cdel_count = read_file()    # 記錄中的圖片尾數, 重複圖片尾數
name, del_count = 1, cdel_count  # 顯示在控制台

# 檢查有沒有重複的圖片
# un_img 是要檢查的圖片(新增的)
# ex_img 是要比對的圖片(檢查過的)
for un_img in uncheck_img:
    for ex_img in exist_img:
        # 副檔名相同
        if un_img.img_format == ex_img.img_format:
            different = cv2.subtract(un_img.img_array, ex_img.img_array)
            result = not np.any(different)

            # 找到一樣的圖片
            if result:
                un_img.check = True
                del_img = cv2.imread(un_img.img_name)

                # 備份重複的圖片
                shutil.copyfile(
                    un_img.img_name, f"./del_images/del_img_{del_count + 1}.{un_img.img_format}")

                # 刪除圖片
                os.remove(un_img.img_name)
                del_count += 1
                break

    # 更改圖片名字
    if un_img.check == False:
        rename = f"LO_{cname}.{un_img.img_format}"
        os.rename(un_img.img_name, rename)
        exist_img.append(P(True, un_img.img_array, rename, un_img.img_format))
        cname += 1
    print(f"檢查第 {name} 張", end='\r', flush=True)
    name += 1

# 檔案尾數的紀錄
write_file(cname, del_count)

del_count = del_count if del_count > 0 else 0
print(
    f"\n檢查完成!!\n新圖片的張數 : {len(uncheck_img) - del_count}\n重複的張數 : {del_count}")

e_time = time.process_time()
print(f"\n圖片檢查花費 {e_time - s_time} 秒")
