from django.urls import path
from .views import DiaryList, DiaryCreate, DiaryDetail


urlpatterns = [
    path('', DiaryList.as_view(), name='list'),
    path('create/', DiaryCreate.as_view(), name='create'),
    path('detail/<int:pk>', DiaryDetail.as_view(), name='detail'),
]
