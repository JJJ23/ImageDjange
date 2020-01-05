from django.urls import path
from . import views
from . import ImgViews

urlpatterns = [
    path('', views.IndexPageView.as_view()),
    path('image/',ImgViews.ImageView.as_view(), name='index'),
]
