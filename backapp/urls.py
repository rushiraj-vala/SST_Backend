from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_view),
    path('upload/', views.uploadImage),
    path('imageList/', views.listImages),
    path('reRecognize/', views.reRecognizeImage),
]
