# 找到重複的圖片

## 方法

我一開始最先想到是利用圖片像素去比對資料夾內的所有圖片，這感覺非常直觀。後來在查找資料時，找到可以利用圖片生成雜湊值的方法。

1. 圖片像素
    將圖片轉換成陣列，兩張圖片陣列相減，如果陣列中有任何非0數字，表示圖片不相同。除了利用像素比對之外，也將檔名固定，如果是特定檔名，那就表示圖片已經本檢查過，不需要將這張圖片加到檢查的行列，避免重複檢查的情況。

    * 被刪除圖片的備份資料夾
        因為我想知道被刪除的圖片是哪幾張，也可以順便檢查自己的程式有沒有錯誤，所以將被刪除的圖片統一放在一起。

        ```PYTHON
        try:
            os.makedirs("del_images")
            print("del_images 資料夾已創建完成")
        except OSError:
            print("del_images 資料夾已存在")
        ```

    * 圖片的前處理
        將圖片轉換成陣列

        ```PYTHON
        def img_process(picture: str) -> Tuple[str, np.ndarray]:
            # 圖片前置處理
            img_size = 300
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
        ```

        > [!NOTE]
        > 有時圖片檔名會有中文字，會導致圖片無法被讀取，這裡是將當下時間當成新檔名，並重新讀取圖片。
        >
        > 圖片長寬設置成300，原因是如果圖片縮太小，會造成明明是兩張不一樣的圖片，卻被當成是相同的。我沒有非常仔細去測試到底多少長寬就足夠判斷，大略測試發現300即可。也發現長寬越大，比對的時間越久。

    * 圖片物件
        設定會需要使用的資訊，包含:
        * check : 圖片是否有被檢查過
        * img_array : 圖片陣列
        * img_name : 圖片檔名
        * img_format : 圖片副檔名

            ```PYTHON
            class P():
                # 圖片資訊
                def __init__(self, check, img_array, img_name, img_format):
                    self.check = check
                    self.img_array = img_array
                    self.img_name = img_name
                    self.img_format = img_format
            ```

    * 分類
        為了加快比對速度，我將圖片依照副檔名做分類，副檔名相同才需要比對，否則跳過。
        * 讀取圖片並轉換成陣列，依照檔名和副檔名進行分類。

            ```PYTHON
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
            ```

        * 比對圖片

            ```PYTHON
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
            ```

        * 檔名讀取和寫入
            因為檔案會重新命名，而且檔名有編號，除了可以避免檔名重複，還可以讓畫面好看一點。為了可以順利從最後一個編號接續下去，我把編號記錄在`img_name.txt`中。也按照副檔名去編號。

            ```PYTHON
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
            ```

    * 未分類
        最一開始想到的方法，沒有任何分類，就是一張一張比對，不管副檔名是否一樣。
        * 讀取圖片並轉換成陣列，再依照圖片檔名區分。

            ```PYTHON
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
            ```

        * 比對圖片

            ```PYTHON
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
            ```

        * 檔名讀取和寫入
            因為檔案會重新命名，而且檔名有編號，除了可以避免檔名重複，還可以讓畫面好看一點。為了可以順利從最後一個編號接續下去，我把編號記錄在`img_name.txt`中。這個就不像是有分類方式，需要讀檔的變數比較少。

            ```PYTHON
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
            ```

2. 雜湊值
    將圖片轉換成雜湊值，比較兩張圖片的雜湊值，如果雜湊值不同，表示圖片不相同。大部分的程式跟像素方法差不多，就是比對圖片方式不同。
    * 被刪除圖片的備份資料夾

        ```PYTHON
        # 被刪除圖片的備份資料夾
        try:
            os.makedirs("del_images")
            print("del_images 資料夾已創建完成")
        except OSError:
            print("del_images 資料夾已存在")
        ```

    * 圖片的前處理
        生成圖片雜湊值

        ```PYTHON
        def img2hash(img_name: str) -> ImageHash:
            try:
                return imagehash.dhash(Image.open(img_name))
            except:
                print("Open Failed")
                return ImageHash(None)
        ```

        > [!NOTE]
        > 好像不會因為中文字而無法讀取圖片。
    * 圖片物件
        設定會需要使用的資訊，包含:
        * img_name : 圖片檔名
        * img_hash : 圖片雜湊值

            ```PYTHON
            class img_obj:
                def __init__(self, img_name: str, img_hash: ImageHash) -> None:
                    self.img_name = img_name
                    self.img_hash = img_hash
            ```

    * 讀取圖片並生成雜湊值，再依照圖片檔名區分。

        ```PYTHON
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
        ```

    * 比對圖片

        ```PYTHON
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
        ```

    * 檔名讀取和寫入

        ```PYTHON
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
        ```

## 筆記

## 版本

* python : 3.10.13
* opencv-python : 4.8.1.78
* numpy : 1.26.2
* imagehash : 4.3.1
* pillow : 10.0.1
