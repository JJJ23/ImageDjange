from django.shortcuts import render
from django.views.generic import TemplateView
from . import ImgForm
from .MLLib import img_face_dt
from django.http.response import JsonResponse
HtmlName = 'Img/learning.html'


class ImageLearningView(TemplateView):
    template_name = HtmlName

    # コンストラクタ
    def __init__(self):
        self.params = {'faceList': [],
                       'form': ImgForm.ImageForm()}

    # GETリクエスト（detect.htmlを初期表示）
    def get(self, req):
        return render(req, HtmlName, self.params)

    # POSTリクエスト（detect.htmlに結果を表示）

    def post(self, req):
        # POSTされたフォームデータを取得
        form = ImgForm.ImageForm(req.POST, req.FILES)
        # フォームデータのエラーチェック
        if not form.is_valid():
            raise ValueError('invalid form')
        # フォームデータから画像ファイルを取得
        image = form.cleaned_data['image']
        label = form.cleaned_data['imageTag']
        # 画像ファイルを指定して顔分類
        face_list = img_face_dt.createimgfile(image)

        # ページの描画指示
        response = {}
        count = 0
        for face_image in face_list:
            key = f"タグ:{label} <br> {image.name} <br>  count:{count}"
            response[key] = face_image
            count += 1
        return JsonResponse(response, safe=False)

