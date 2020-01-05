#from django.shortcuts import render
from django.views.generic import TemplateView
#from django.http.response import HttpResponse
import django as django
import tensorflow as tf
from AzureImage import path_setting
from .MLLib import img_face_dt
from .MLLib import img_data_gen
from .MLLib import img_model_gen
import os

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
   # return HttpResponse('This is Azure Image test. django version' + django.get_version()+ ' ¥¥n tensorflow version:' + tf.__version__)
