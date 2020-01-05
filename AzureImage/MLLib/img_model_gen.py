import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from keras.layers import Conv2D, Dense, Flatten, MaxPooling2D, Dropout
from keras.models import Sequential
# from keras.utils.vis_utils import plot_model
# tensorflowのkerasはimport時にpydot_ng,pydotplusをimportするように記述されているが，
# keras(ver=2.2.0)はimport時，pydotしかimportするようにしか記述されていないため下記とする
from tensorflow.python.keras.utils.vis_utils import plot_model
import keras
from .. import path_setting


def load_images(image_directory):
    x_data = []
    y_data = []
    labels = os.listdir(image_directory)
    numclass = 0
    for root in labels:
        if root.startswith('.'):
            continue
        image_file_list = []
        image_dir = os.path.join(image_directory, root)
        # 指定したディレクトリ内のファイル取得
        image_file_name_list = os.listdir(image_dir)

        print(f"対象画像ファイル数：{len(image_file_name_list)}")
        for image_file_name in image_file_name_list:
            # 画像ファイルパス
            image_file_path = os.path.join(image_dir, image_file_name)
            print(f"画像ファイルパス:{image_file_path}")
            # 画像読み込み
            image = cv2.imread(image_file_path)
            if image is None:
                print(f"画像ファイル[{image_file_name}]を読み込めません")
                continue
            image_file_list.append((image_file_name, image))
        print(f"読込画像ファイル数：{len(image_file_list)}")
        rgbimg,label = labeling_images(image_file_list, int(root))
        x_data.extend(rgbimg)
        y_data.extend(label)
        numclass += 1
    return numclass, np.array(x_data), np.array(y_data)


def labeling_images(image_file_list, dirs):
    x_data = []
    y_data = []
    for idx, (file_name, image) in enumerate(image_file_list):
        # 画像をBGR形式からRGB形式へ変換
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # 画像配列（RGB画像）
        x_data.append(image)
        # ラベル配列（ファイル名の先頭2文字をラベルとして利用する）
        y_data.append(dirs)
    #x_data = np.array(x_data)
    print(f"ラベリング画像数：{len(x_data)}")
    return x_data, y_data


# Outoput Model Only
OUTPUT_MODEL_ONLY = False


def createmodel():
    print("===================================================================")
    print("モデル学習 Keras 利用版")
    print("指定した画像ファイルをもとに学習を行いモデルを生成します。")
    print("===================================================================")

    # ディレクトリの作成
    if not os.path.isdir(path_setting.OUTPUT_MODEL_DIR):
        os.mkdir(path_setting.OUTPUT_MODEL_DIR)
    # ディレクトリ内のファイル削除
    path_setting.delete_dir(path_setting.OUTPUT_MODEL_DIR, False)

    batch_size = 32
    epochs = 10

    # 学習用の画像ファイルの読み込み
    num_classes, x_train, y_train = load_images(path_setting.SCRATCHIOUTPUT_IMAGE_DIR)

    #plt.imshow(x_train[0])
    #plt.show()
    print(y_train[0])

    # テスト用の画像ファイルの読み込み
    num_classes_test, x_test, y_test= load_images(path_setting.TEST_IMAGE_PATH)
    # 学習用の画像ファイルのラベル付け


    # plt.imshow(x_test[0])
    # plt.show()
    # print(y_test[0])

    # 画像とラベルそれぞれの次元数を確認
    print("x_train.shape:", x_train.shape)
    print("y_train.shape:", y_train.shape)
    print("x_test.shape:", x_test.shape)
    print("y_test.shape:", y_test.shape)

    # クラスラベルの1-hotベクトル化（線形分離しやすくする）
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    # 画像とラベルそれぞれの次元数を確認
    print("x_train.shape:", x_train.shape)
    print("y_train.shape:", y_train.shape)
    print("x_test.shape:", x_test.shape)
    print("y_test.shape:", y_test.shape)

    # モデルの定義
    model = Sequential()

    # 画像に対して空間的畳み込みを行い、2次元の畳み込みレイヤーを作成する
    # 下記であれば、32通りの3×3のフィルタを用いて32通りの出力をもとに活性化関数（ReLU）を利用して特徴量（重み）を計算
    # input_shape   入力データのサイズ 128 x 128 x 3(RGB)
    # filters       フィルタ(カーネル)の数（出力数の次元）
    # kernel_size   フィルタ(カーネル)のサイズ数．3x3とか5x5とか奇数正方にすることが一般的
    # strides       ストライドの幅(フィルタを動かすピクセル数)
    # padding       データの端の取り扱い方(入力データの周囲を0で埋める(ゼロパディング)ときは'same',ゼロパディングしないときは'valid')
    # activation    活性化関数
    model.add(Conv2D(input_shape=(128, 128, 3), filters=32, kernel_size=(3, 3),
                     strides=(1, 1), padding="same", activation='relu'))
    # 2x2の4つの領域に分割して各2x2の行列の最大値をとることで出力をダウンスケールする
    # パラメータはダウンスケールする係数を決定する2つの整数のタプル
    # 各領域内の位置の違いを無視するためモデルが小さな位置変化に対して頑健（robust）となる
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # 畳み込み2
    model.add(Conv2D(filters=32, kernel_size=(3, 3), strides=(1, 1),
                     padding="same", activation='relu'))
    # 出力のスケールダウン2
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # ドロップアウト1
    model.add(Dropout(0.01))

    # 畳み込み3
    model.add(Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1),
                     padding="same", activation='relu'))
    # 出力のスケールダウン3
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # ドロップアウト2
    model.add(Dropout(0.05))

    # 全結合層(プーリング層の出力は4次元テンソルであるため1次元のベクトルに変換)
    model.add(Flatten())

    # 予測用のレイヤー1
    model.add(Dense(512, activation='sigmoid'))

    # 予測用のレイヤー2
    model.add(Dense(128, activation='sigmoid'))

    # 予測用のレイヤー3
    model.add(Dense(num_classes, activation='softmax'))

    # コンパイル
    model.compile(optimizer='sgd',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # サマリーの出力
    model.summary()

    # モデルの可視化
    plot_model(model, to_file=path_setting.OUTPUT_MODEL_PLOT_FILE, show_shapes=True)

    if OUTPUT_MODEL_ONLY:
        # 学習
        model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs)
    else:
        # 学習+グラフ
        history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs,
                            verbose=1, validation_data=(x_test, y_test))
        for key in history.history.keys():
            print(key)

        # 汎化精度の評価・表示
        test_loss, test_acc = model.evaluate(x_test, y_test, batch_size=batch_size, verbose=0)
        print(f"validation loss:{test_loss}\r\nvalidation accuracy:{test_acc}")

        # acc（精度）, val_acc（バリデーションデータに対する精度）のプロット
        plt.plot(history.history["accuracy"], label="accuracy", ls="-", marker="o")
        plt.plot(history.history["val_accuracy"], label="val_accuracy", ls="-", marker="x")
        plt.title('model accuracy')
        plt.xlabel("epoch")
        plt.ylabel("accuracy")
        plt.legend(loc="best")
        plt.show()

        # 損失の履歴をプロット
        plt.plot(history.history['loss'], label="loss", ls="-", marker="o")
        plt.plot(history.history['val_loss'], label="val_loss", ls="-", marker="x")
        plt.title('model loss')
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.legend(loc='lower right')
        plt.show()

    # モデルを保存
    model.save(path_setting.MODEL_FILE_PATH)

    return 0
