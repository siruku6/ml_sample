from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy

from .models import DiaryModel


class DiaryList(ListView):
    template_name = 'helloworldapp/templates/list.html'
    model = DiaryModel


class DiaryCreate(CreateView):
    template_name = 'helloworldapp/templates/create.html'
    model = DiaryModel
    fields = ('date', 'title', 'text')
    success_url = reverse_lazy('list')


class DiaryDetail(DetailView):
    template_name = 'helloworldapp/templates/detail.html'
    model = DiaryModel
