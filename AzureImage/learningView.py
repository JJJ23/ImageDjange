from django.shortcuts import render
from django.views.generic import TemplateView
from .ImgForm import SettingForm
from .ImgForm import ImageForm
from .MLLib import img_face_dt
from django.http.response import JsonResponse
from .setting_models import Setting

HtmlName = 'Img/learning.html'


class ImageLearningView(TemplateView):
    template_name = HtmlName
    setting_class = SettingForm
    image_class = ImageForm

    # コンストラクタ
    def __init__(self):
        self.params = {'image_form': ImageForm(),
                       'setting_form': SettingForm()}

    def update_setting(request):
        form = SettingForm(request.POST)
        #form.save()
        form.save()
        response = {}
        response['result'] = "OK"
        return JsonResponse(response, safe=False)

    def form_valid(self, form_class):
        SettingForm.save()

    # GETリクエスト（detect.htmlを初期表示）
    def get(self, req):
        db = Setting.objects.all()
        print(db)
        print(self.params.keys())
        return render(req, HtmlName, self.params)

    # POSTリクエスト（detect.htmlに結果を表示）
    def post(self, req):
        # POSTされたフォームデータを取得
        form = ImageForm(req.POST, req.FILES)
        #setting_form = ImgForm.SettingForm(req.POST)
        # フォームデータのエラーチェック
        if not form.is_valid():
            raise ValueError('invalid form')
        # フォームデータから画像ファイルを取得
        image_filed = form.cleaned_data['image']
        label = form.cleaned_data['imageTag']
        if label == "1":
            cap = img_face_dt.get_imageCaptrue()
        # 画像ファイルを指定して顔分類
        input_image, face_list = img_face_dt.createimgfile(image_filed)
        # ページの描画指示
        response = {}
        count = 1
        key = f"入力画像:{image_filed.name}"
        response[key] = input_image
        if len(face_list) == 0:
            face_list.append("")

        for face_image in face_list:
            if not face_image:
                key = f"タグ:{label} <br> {image_filed.name} <br>  not found face"
            else:
                key = f"タグ:{label} <br> {image_filed.name} <br>  count:{count}"
                count += 1
            response[key] = face_image

        return JsonResponse(response, safe=False)

