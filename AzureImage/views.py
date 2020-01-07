from django.shortcuts import render
from django.views.generic import TemplateView
#from django.http.response import HttpResponse
import django as django
import tensorflow as tf
from AzureImage import path_setting
from .MLLib import img_face_dt
from .MLLib import img_data_gen
from .MLLib import img_model_gen
from . import ImgForm

class IndexPageView(TemplateView):
    template_name = 'index_page.html'
    #if not os.path.exists(path_setting.MODEL_FILE_PATH):
        #img_face_dt.createimgfile()
        #img_data_gen.scratchImage()
        #img_model_gen.createmodel()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["TfVersion"] = tf.__version__
        context["djVersion"] = django.get_version()
        return context


HtmlName = 'Img/learning.html'

class ImageLearningView(TemplateView):
    template_name = 'Img/learning.html'

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
       self.params['facelist'] = facelist
       # ページの描画指示
       return render(req, HtmlName, self.params)
