import cv2
import os
import numpy as np
import subprocess
import re

root_dir = os.getcwd()
# 被刪除圖片的備份
try:
    os.makedirs("del_images")
    print("del_images 資料夾已創建完成")
except OSError:
    print("del_images 資料夾已存在")


def img_process(picture: str) -> str | np.ndarray:
    # 圖片前置處理
    not_img_format = [".jfif"]  # 圖片無法寫入的副檔名
    img_name, img_format = os.path.splitext(picture)
    if img_format in not_img_format:
        subprocess.run(['magick', 'mogrify', '-format',
                       'jpg',  picture], shell=True)
        os.remove(picture)
        picture = f"{img_name}.jpg"
    else:
        subprocess.run(['magick', 'mogrify', picture], shell=True)
    img = cv2.imread(picture, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (24, 24))
    img = img.reshape(24, 24)
    return picture, img


def write_file(n: int, d: int):
    with open("img_name.txt", 'w') as f:
        f.write(str(n)+'\n'+str(d))


def read_file() -> int | int:
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


img_temp = []   # 圖片物件陣列

exist_img = []  # 已經存在的圖片(已檢查)
uncheck_img = []  # 新增的圖片(未檢查)

count = 1   # 圖片張數
file_extension = ["jpg", "JPG", "jpeg", "jfif", "png", "PNG"]   # 副檔名
m = re.compile('LO_\d+.\w+')  # 找出符合的檔名

# 圖片前處理後放到圖片物件陣列
for pictures in os.listdir(root_dir):
    if os.path.isfile(os.path.join(root_dir, pictures)):
        if pictures.split(".")[1] in file_extension:
            print(f"前處理第 {count} 張圖片中", end='\r', flush=True)
            pictures, img_array = img_process(pictures)
            img_format = pictures.split(".")[1]

            if m.match(pictures) != None:
                exist_img.append(P(True, img_array, pictures, img_format))
            else:
                uncheck_img.append(P(False, img_array, pictures, img_format))

            count += 1

for i in exist_img:
    print("exist images : ", i.img_name)
for i in uncheck_img:
    print("uncheck images : ", i.img_name)

print(f"\n圖片總數 : {len(exist_img)+len(uncheck_img)}\n已檢查的圖片 : {len(exist_img)}\n未檢查的圖片 : {len(uncheck_img)}\n開始檢查!!")

index = 1   # 切割圖片物件陣列
cname, cdel_count = read_file()    # 圖片檔名, 重複圖片的數量
name, del_count = 1, cdel_count

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
                print(check_img.img_name)
                del_img = cv2.imread(check_img.img_name)
                cv2.imwrite(
                    f"./del_images/del_img_{del_count + 1}.{check_img.img_format}", del_img)

                # 刪除圖片
                os.remove(check_img.img_name)
                del_count += 1

    # 更改圖片名字
    if img.check == False:
        os.rename(img.img_name, f"LO_{cname}.{img.img_format}")
        print(f"檢查第 {name} 張", end='\r', flush=True)
        cname += 1
        name += 1
    index += 1
    img.check = True

# 檔案尾數的紀錄
write_file(name, del_count)

del_count = del_count-cdel_count
print(
    f"\n檢查完成!!\n檢查的張數 : {len(img_temp)}\n重複的張數 : {del_count if del_count > 0 else 0}")
