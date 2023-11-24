# a = [10, 10, 10]

# for i in range(len(a)):
#     if a != []:
#         img = a.pop()
#         for j in a:
#             if img == j:
#                 print("Same Number.")
#                 break

import os
from imagehash import ImageHash
import imagehash
from PIL import Image


def img2hash(img_name: str) -> ImageHash:
    try:
        return imagehash.dhash(Image.open(img_name))
    except:
        print(f"{img_name} open Failed")
        return ImageHash(None)


def write_file(n: int, d: int):
    with open("img_name.txt", 'w') as f:
        f.write(str(n)+'\n'+str(d))


class img_obj:
    def __init__(self, img_name, img_hash) -> None:
        self.img_name = img_name
        self.img_hash = img_hash


root_path = os.getcwd()
del_path = os.path.join(root_path, "del_images")
lo_hash_list = []

for index, lo_img in enumerate(os.listdir(os.path.join(r"C:\\Users\\tiger\\Desktop\\1", "classification")), 1):
    print(index, end='\r', flush=True)
    if lo_img.split(".").pop() in ["jpg", "JPG", "jpeg", "png", "PNG", "jfif"]:
        lo_img_hash = img2hash(os.path.join(
            r"C:\\Users\\tiger\\Desktop\\1", "classification", lo_img))
        lo_hash_list.append(img_obj(lo_img, lo_img_hash))

tmp = []
for img in lo_hash_list:
    tmp.append(img.img_hash)

for img in os.listdir(del_path):
    img_count = 0
    img_hash = img2hash(os.path.join(del_path, img))
    img_count = tmp.count(img_hash)

    if img_count == 1:
        print(f"\n\n{img} is OK.")
        with open("same_img.txt", 'a') as file:
            file.write(f"\n{img} at unique from classification")

    else:
        index_list = []
        index = 0
        while img_count != 0:
            index = tmp.index(img_hash, index)
            index_list.append(lo_hash_list[index].img_name)
            img_count -= 1
            index += 1

        print(f"{img} at {index_list} from classification ")
        with open("same_img.txt", 'a') as file:
            file.write(f"\n{img} at {index_list} from classification")
