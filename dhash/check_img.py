import re
import shutil
import time
from typing import Tuple
import imagehash
from imagehash import ImageHash
from PIL import Image
import os

s_time = time.process_time()

path = os.getcwd()

# 被刪除圖片的備份資料夾
try:
    os.makedirs("del_images")
    print("del_images 資料夾已創建完成")
except OSError:
    print("del_images 資料夾已存在")


class img_obj:
    def __init__(self, img_name: str, img_hash: ImageHash) -> None:
        self.img_name = img_name
        self.img_hash = img_hash


def img2hash(img_name: str) -> ImageHash:
    try:
        return imagehash.dhash(Image.open(img_name))
    except:
        print("Open Failed")
        return ImageHash()


def write_file(n: int, d: int):
    with open("img_name.txt", 'w') as f:
        f.write(str(n)+'\n'+str(d))


def read_file() -> Tuple[int, int]:
    if not os.path.exists("img_name.txt"):
        with open("img_name.txt", 'w') as f:
            n = 0
            d = 0
            return n, d
    else:
        with open("img_name.txt", 'r') as f:
            n = int(f.readline())
            d = int(f.readline())
            return n, d


# 圖片前處理計時
s_time = time.process_time()

img_format = ["jpg", "png", "jfif", "JPG", "PNG", "jpeg"]

uncheck_imgList = []
checked_imgList = []

img_allCount = 0
m = re.compile('LO_\d+.\w+')

# 生成圖片雜湊值
for img in os.listdir(path):
    if img.split(".").pop() in img_format:
        print(f"前處理第 {img_allCount + 1} 張圖片中", end='\r', flush=True)
        img_hash = img2hash(img)

        if m.match(img) != None:
            checked_imgList.append(img_obj(img, img_hash))
        else:
            uncheck_imgList.append(img_obj(img, img_hash))

        img_allCount += 1

checked_imgCount = len(checked_imgList)
uncheck_imgCount = len(uncheck_imgList)

print(
    f"\n\n圖片總數 : {img_allCount}\n\n已檢查的圖片 : {checked_imgCount}\n未檢查的圖片 : {uncheck_imgCount}\n\n開始檢查!!\n")

e_time = time.process_time()
print(f"\n圖片前處理花費 {e_time - s_time} 秒\n")

# 圖片檢查計時
s_time = time.process_time()

cname, cdel_count = read_file()    # 記錄中的圖片尾數, 重複圖片尾數
del_count = cdel_count  # 顯示在控制台

# 比對圖片雜湊值
for num, org_img_obj in enumerate(uncheck_imgList, 1):
    print(f"檢查第 {num} 張", end='\r', flush=True)

    # 圖片改檔名的訊號
    flag = False

    org_img_name = org_img_obj.img_name
    org_img_hash = org_img_obj.img_hash
    org_img_format = org_img_obj.img_name.split('.').pop()

    for target_img_obj in checked_imgList:
        target_img_name = target_img_obj.img_name
        target_img_hash = target_img_obj.img_hash
        target_img_format = target_img_obj.img_name.split('.').pop()

        # 找到相同的雜湊值
        if org_img_hash == target_img_hash:
            flag = True

            # 備份重複的圖片
            shutil.copyfile(
                org_img_name, f"./del_images/del_img_{del_count + 1}.{org_img_format}")

            # 刪除圖片
            os.remove(org_img_name)
            del_count += 1
            break

    # 更改圖片名字
    if not flag:
        cname += 1
        rename = f"LO_{cname}.{org_img_format}"
        os.rename(org_img_name, rename)
        checked_imgList.append(img_obj(rename, org_img_hash))

# 檔案尾數的紀錄
write_file(cname, del_count)

same_imgCount = del_count - cdel_count
new_imgCount = uncheck_imgCount - same_imgCount

print(
    f"\n\n檢查完成!!\n\n新圖片的張數 : {new_imgCount}\n重複的張數 : {same_imgCount}")

e_time = time.process_time()
print(f"\n圖片檢查花費 {e_time - s_time} 秒")
