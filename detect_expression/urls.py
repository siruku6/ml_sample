from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='face_index'),
    path('start_webcam/', views.start_webcam, name='detect_face'),
]

urlpatterns += staticfiles_urlpatterns()
