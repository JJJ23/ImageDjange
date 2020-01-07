from django.urls import path
from . import views
from . import ImgDetectViews
from . import learningView

app_name = "AzureImage"
urlpatterns = [
    path('', views.IndexPageView.as_view()),
    path('detect', ImgDetectViews.ImageDetectView.as_view(), name='detect'),
    path('learning', learningView.ImageLearningView.as_view(), name='AzureImage/learningView'),
]
