from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input_form', views.input_form, name='mlapp/input_form'),
    path('result/', views.result, name='result'),
    path('history/', views.CustomerList.as_view(), name='history'),
    path('login/', views.Login.as_view(), name='login'),
]
