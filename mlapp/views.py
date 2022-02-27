from django.views.generic import ListView
from django.shortcuts import render, redirect
from .forms import InputForm
from .models import Customer


class ConsumerList(ListView):
    template_name = 'mlapp/templates/index.html'
    model = Customer


def input_form(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = InputForm()
        return render(request, 'mlapp/templates/input_form.html', {'form': form})
