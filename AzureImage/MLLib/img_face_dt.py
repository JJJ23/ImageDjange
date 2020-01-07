import os
import pathlib
import glob
import cv2
from .. import path_setting
from PIL import Image
import numpy as np

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


def detect_image_face(imageName):

    # アップロードされた画像ファイルをメモリ上でOpenCVのimageに格納
    image = np.asarray(Image.open(imageName))

    # 画像をOpenCVのBGRからRGB変換
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # 顔認識
    faces = cv2detectfaces(image_rgb)
    if len(faces) == 0:
        print(f"顔認識失敗")
        return 0
    # 1つ以上の顔を認識
    face_count = 1
    facePathList = []
    for (xpos, ypos, width, height) in faces:
        face_image = image_rgb[ypos:ypos+height, xpos:xpos+width]
        if face_image.shape[0] > ImageSize:
            face_image = cv2.resize(face_image, (ImageSize, ImageSize))
        print(face_image.shape)
        # 保存
        filename, extension = os.path.splitext(imageName.name)
        output_path = os.path.join(path_setting.OUTPUT_IMAGE_DIR, f"{filename}_{face_count:03}{extension}")
        print(f"出力ファイル（絶対パス）:{output_path}")
        cv2.imwrite(output_path, face_image)
        facePathList.append(output_path)
        face_count = face_count + 1

    return facePathList


def createimgfile(imageNameList):
    print("===================================================================")
    print("イメージ顔認識 OpenCV 利用版")
    print("指定した画像ファイルの正面顔を認識して抜き出し、サイズ変更"+ f"{ImageSize} x {ImageSize}" + "を行います。")
    print("===================================================================")

    # ディレクトリの作成
    if not os.path.isdir(path_setting.OUTPUT_IMAGE_DIR):
        os.mkdir(path_setting.OUTPUT_IMAGE_DIR)
    # ディレクトリ内のファイル削除
    path_setting.delete_dir(path_setting.OUTPUT_IMAGE_DIR, False)

    face_cnt = 0
    facelistpath = []
    # 画像ごとの顔認識
 #   for imageName in imageNameList:
        # 画像ファイルの読み込み
        # name_images = load_name_images(path_setting.IMAGE_PATH_PATTERN)

   # file_path = os.path.join(path_setting.OUTPUT_IMAGE_DIR, imageName+f"{face_cnt}")
    #image = name_image[1]
    facelistpath.append(detect_image_face(imageNameList))

    print(f"Total face count {face_cnt}")
    return facelistpath
