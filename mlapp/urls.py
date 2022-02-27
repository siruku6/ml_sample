from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConsumerList.as_view(), name='index'),
    path('input_form', views.input_form, name='mlapp/input_form'),
]
