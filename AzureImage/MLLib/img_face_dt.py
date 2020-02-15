import os
import pathlib
import glob
import cv2
from .. import path_setting
from PIL import Image
import numpy as np
import base64
import io

# Origin Image Pattern
#IMAGE_PATH_PATTERN = "./origin_image/*"
# Output Directory
#OUTPUT_IMAGE_DIR = "./face_image"
ImageSize = 64
def load_name_images(image_path_pattern):
    name_images = []
    # 指定したパスパターンに一致するファイルの取得
    image_paths = glob.glob(image_path_pattern)
    # ファイルごとの読み込み
    for image_path in image_paths:
        path = pathlib.Path(image_path)
        # ファイルパス
        fullpath = str(path.resolve())
        print(f"画像ファイル（絶対パス）:{fullpath}")
        # ファイル名
        filename = path.name
        print(f"画像ファイル（名前）:{filename}")
        # 画像読み込みß
        image = cv2.imread(fullpath)
        if image is None:
            print(f"画像ファイル[{fullpath}]を読み込めません")
            continue
        name_images.append((filename, image))
    return name_images


def cv2detectfaces(image):
    # 画像ファイルのグレースケール化
    image_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # カスケードファイルの読み込み
    cascade = cv2.CascadeClassifier(path_setting.CASCADE_FILE_PATH)
    return cascade.detectMultiScale(image_gs, scaleFactor=1.2, minNeighbors=5, minSize=(ImageSize, ImageSize))


def encode_png_image(image):
    is_success, img_buffer = cv2.imencode(".png", image)
    if is_success:
        # 画像をインメモリのバイナリストリームに流し込む
        io_buffer = io.BytesIO(img_buffer)
        # インメモリのバイナリストリームからBASE64エンコードに変換
        result_img = base64.b64encode(io_buffer.getvalue()).decode().replace("'", "")
    return result_img


def detect_image_face(image_rgb,file_name):
    face_ImageList = []

    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    # 顔認識
    faces = cv2detectfaces(image_bgr)
    if len(faces) == 0:
        print(f"顔認識失敗")
        return encode_png_image(image_bgr), face_ImageList
    # 1つ以上の顔を認識
    face_count = 1

    for (xpos, ypos, width, height) in faces:
        face_image = image_bgr[ypos:ypos+height, xpos:xpos+width]
        if face_image.shape[0] > ImageSize:
            face_image = cv2.resize(face_image, (ImageSize, ImageSize))
        print(face_image.shape)
        # 保存
        filename, extension = os.path.splitext(file_name)
        output_path = os.path.join(path_setting.TRAIN_IMAGE_DIR, f"{filename}_{face_count:03}{extension}")
        print(f"出力ファイル（絶対パス）:{output_path}")
        cv2.imwrite(output_path, face_image)
        # BASE64にエンコード
        result_img = encode_png_image(face_image)
        face_ImageList.append(result_img)
        face_count = face_count + 1
    return encode_png_image(image_bgr), face_ImageList


def createimgfile(image_filed):
    print("===================================================================")
    print("イメージ顔認識 OpenCV 利用版")
    print("指定した画像ファイルの正面顔を認識して抜き出し、サイズ変更"+ f"{ImageSize} x {ImageSize}" + "を行います。")
    print("===================================================================")

    # ディレクトリの作成
    if not os.path.isdir(path_setting.TRAIN_IMAGE_DIR):
        os.mkdir(path_setting.TRAIN_IMAGE_DIR)
    # ディレクトリ内のファイル削除
    path_setting.delete_dir(path_setting.TRAIN_IMAGE_DIR, False)
    return detect_image_face(np.array(Image.open(image_filed)),image_filed.name)

'''
    face_list = []
    # 画像ごとの顔認識
 #   for imageName in imageNameList:
        # 画像ファイルの読み込み
        # name_images = load_name_images(path_setting.IMAGE_PATH_PATTERN)

   # file_path = os.path.join(path_setting.OUTPUT_IMAGE_DIR, imageName+f"{face_cnt}")
    #image = name_image[1]
    face_list.append(detect_image_face(imageNameList))

    #print(f"Total face count {face_list.len}")
'''


def get_imageCaptrue():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return

    while(True):
        # フレームをキャプチャする
        ret, frame = cap.read()

        # 画面に表示する
        cv2.imshow('frame',frame)

        # キーボード入力待ち
        key = cv2.waitKey(1) & 0xFF

        # qが押された場合は終了する
        if key == ord('q'):
            break
        # sが押された場合は保存する
        if key == ord('s'):
            path = "photo.jpg"
            cv2.imwrite(path,frame)
    # キャプチャの後始末と，ウィンドウをすべて消す
    cap.release()
    cv2.destroyAllWindows()
