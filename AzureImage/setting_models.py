from django.db import models
from . import path_setting


class Setting(models.Model):
 #   model_filePath = models.FilePathField(verbose_name="モデルパス指定", path=path_setting.MODEL_FILE_PATH)
 #   cascade_filePath = models.FilePathField(verbose_name="特徴抽出CASCADE", path=path_setting.CASCADE_FILE_PATH)
 #   train_filePath = models.FilePathField(verbose_name="学習用フォルダ指定", path=path_setting.TRAIN_IMAGE_DIR)
    model_filePath = models.FilePathField(verbose_name="モデルパス指定", path=path_setting.OUTPUT_MODEL_DIR)
    cascade_filePath = models.FilePathField(verbose_name="特徴抽出CASCADE", path=path_setting.OUTPUT_MODEL_DIR)
    train_filePath = models.CharField(verbose_name="学習用フォルダ指定", max_length=100)
