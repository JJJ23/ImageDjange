from django import forms


class ImageForm(forms.Form):

    imageTag = forms.CharField(
        label='タグ', max_length=50,
        required=False, help_text='※任意'
    )
    image = forms.ImageField(label="判定する画像を選択してください",
                             error_messages={'missing' : '画像ファイルが選択されていません。',
                                             'invalid' : '分類する画像ファイルを選択してください。',
                                             'invalid_image' : '画像ファイルではないようです。'})


"""class FileForm(forms.Form):

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )
    class Meta:
        model = Image
        fields = ('image',)
"""
