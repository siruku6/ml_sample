from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('live', views.live(), name="live"),
    path('start_webcam/', views.start_webcam, name='predict'),
]

urlpatterns += staticfiles_urlpatterns()
