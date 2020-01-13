from django import forms
from . import setting_models

class ImageForm(forms.Form):

    imageTag = forms.CharField(
        label='画像タグ', max_length=50,
        required=False, help_text='※任意'
    )
    image = forms.ImageField(label="判定する画像を選択してください",
                             error_messages={'missing': '画像ファイルが選択されていません。',
                                             'invalid': '分類する画像ファイルを選択してください。',
                                             'invalid_image': '画像ファイルではないようです。'})
    #modelName = forms.FilePathField(label='モデル')


class SettingForm(forms.ModelForm):
    # ModelFormクラスを継承。データベースに保存するには、Metaクラスが必要
    class Meta:
        # models.pyの使用したいクラス(Model)と、Fieldを記載
        model = setting_models.Setting
        fields = ('model_filePath', 'cascade_filePath', 'train_filePath')

"""class FileForm(forms.Form):

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )
    class Meta:
        model = Image
        fields = ('image',)
"""
