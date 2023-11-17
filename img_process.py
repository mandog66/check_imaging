import cv2
import os
import keras.utils as image

root_dir = os.getcwd()
fileExtension = ["jpg", "JPG", "jpeg", "jfif", "png", "PNG"]


def img_process(picture):
    # 圖片前置處理
    img = cv2.imread(root_dir + "\\" + picture, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (24, 24))
    img = image.img_to_array(img)
    img = img.reshape(24, 24)
    return img


def file_extension():
    for pictures in os.listdir(root_dir):
        print(pictures, end="\t")
        # print(pictures.split("."))
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


if __name__ == "__main__":
    # img = img_process("check_img_763.png")
    # file_extension()
    open_img()
