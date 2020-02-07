from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostView.as_view(), name='posts_list'),
    path('upload_file/', views.UploadFile.as_view(), name='upload_file'),
]
