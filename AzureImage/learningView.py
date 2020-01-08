from django.shortcuts import render
from django.views.generic import TemplateView
from . import ImgForm
from .MLLib import img_face_dt
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
       # 画像ファイルを指定して顔分類
       facelist = img_face_dt.createimgfile(image)
       # result = img_model_gen.createmodel()
       # 顔分類の結果を格納
       self.params['faceList'] = facelist
       # ページの描画指示
       return render(req, HtmlName, self.params)
