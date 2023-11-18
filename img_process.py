import cv2
import os
import keras.utils as image
import time

root_dir = os.getcwd()
fileExtension = ["jpg", "JPG", "jpeg", "jfif", "png", "PNG"]


def img_process(picture):
    # 圖片前置處理
    img = cv2.imread(picture, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (24, 24))
    img = image.img_to_array(img)
    img = img.reshape(24, 24)
    return img


def file_extension():
    for pictures in os.listdir(root_dir):
        if os.path.isfile(os.path.join(root_dir, pictures)):
            print(pictures, end="\t")
            if pictures.split(".")[1] in fileExtension:
                print("True")
            else:
                print("False")


def open_img():
    # for img in os.listdir(root_dir):
    #     if img.split(".")[1] in fileExtension:
    #         open_img = cv2.imread(img)
    #         cv2.namedWindow("remove_img", cv2.WINDOW_NORMAL)
    #         cv2.resizeWindow("remove_img", 500, 500)
    #         cv2.imshow("remove_img", open_img)
    #         cv2.waitKey(0)
    #         cv2.destroyAllWindows()

    for i, img in enumerate(os.listdir(root_dir), 1):
        if img.split(".")[1] in fileExtension:
            open_img = cv2.imread(img)
            cv2.namedWindow("remove_img_{}".format(i), cv2.WINDOW_NORMAL)
            cv2.resizeWindow("remove_img_{}".format(i), 500, 500)
            cv2.imshow("remove_img_{}".format(i), open_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def del_dir():
    try:
        os.makedirs("del_images")
        print("del_images folder be created")
    except OSError:
        print("del_images folder exist")


def copy_img(i):
    img = cv2.imread("check_img_763.png")
    cv2.imwrite("./del_images/del_image_{}.png".format(i), img)


def print_same():
    for i in range(3, 0, -1):
        print(i, flush=False)
        time.sleep(1)
    print("GO")


def img_to_array():
    img = cv2.imread("check_img_763.png", cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (24, 24))
    img = img.reshape(24, 24)
    print(img)

    img = cv2.imread("check_img_763.png", cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (24, 24))
    img = image.img_to_array(img)
    img = img.reshape(24, 24)
    print(img)


if __name__ == "__main__":
    # img = img_process("check_img_763.png")
    # file_extension()
    # open_img()
    # del_dir()
    # copy_img(1)
    # copy_img(2)
    # print_same()
    img_to_array()
