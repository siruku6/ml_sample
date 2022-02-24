from django.db import models
from django.utils import timezone


class DiaryModel(models.Model):
    date = models.DateField('日付', default=timezone.now)
    title = models.CharField('タイトル', max_length=100)
    text = models.TextField('本文')

    def __str__(self):
        return self.title
