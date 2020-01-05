import base64
import io
import cv2
import numpy as np
from PIL import Image
from .. import path_setting
import tensorflow as tf
from . import img_face_dt
import keras
from keras.backend import tensorflow_backend as backend


def detect(upload_image):
    result_name = upload_image.name
    result_list = []
    result_img = ''

    # 設定からモデルファイルのパスを取得
    model_file_path = path_setting.MODEL_FILE_PATH
    # kerasでモデルを読み込む
    model = keras.models.load_model(model_file_path)

    # アップロードされた画像ファイルをメモリ上でOpenCVのimageに格納
    image = np.asarray(Image.open(upload_image))

    # 画像をOpenCVのBGRからRGB変換
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # OpenCVを利用して顔認識
    face_list = img_face_dt.cv2detectfaces(image)

    imgsize = img_face_dt.ImageSize
    # 顔が１つ以上検出できた場合
    if len(face_list) > 0:
        count = 1
        for (xpos, ypos, width, height) in face_list:
            # 認識した顔の切り抜き
            face_image = image_rgb[ypos:ypos+height, xpos:xpos+width]
            # 切り抜いた顔が小さすぎたらスキップ
            if face_image.shape[0] < imgsize or face_image.shape[1] < imgsize:
                continue
            # 認識した顔のサイズ縮小
            face_image = cv2.resize(face_image, (imgsize, imgsize))
            # 認識した顔のまわりを赤枠で囲む
            cv2.rectangle(image_rgb, (xpos, ypos),
                          (xpos+width, ypos+height), (0, 0, 255), thickness=2)
            # 認識した顔を1枚の画像を含む配列に変換
            face_image = np.expand_dims(face_image, axis=0)
            # 認識した顔から名前を特定
            name, result = detect_who(model, face_image)
            # 認識した顔に名前を描画
            cv2.putText(image_rgb, f"{count}. {name}", (xpos, ypos+height+20),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            # 結果をリストに格納
            result_list.append(result)
            count = count + 1

    # 画像をPNGに変換
    orgHeight, orgWidth = image.shape[:2]

    outputimage = cv2.resize(image_rgb, (1024, int(orgWidth/orgHeight*1024)))
    is_success, img_buffer = cv2.imencode(".png", outputimage)
    if is_success:
        # 画像をインメモリのバイナリストリームに流し込む
        io_buffer = io.BytesIO(img_buffer)
        # インメモリのバイナリストリームからBASE64エンコードに変換
        result_img = base64.b64encode(io_buffer.getvalue()).decode().replace("'", "")

    # tensorflowのバックエンドセッションをクリア
    backend.clear_session()
    # 結果を返却
    return (result_list, result_name, result_img)


def detect_who(model, face_image):
    # 予測
    predicted = model.predict(face_image)
    # 結果
    name = ""
    result = f"おばあちゃんの可能性:{predicted[0][0]*100:.3f}% / 佳瑩の可能性:{predicted[0][1]*100:.3f}%"
    name_number_label = np.argmax(predicted)
    if name_number_label == 0:
        name = "nainai"
    elif name_number_label == 1:
        name = "jia ying"
    return (name, result)