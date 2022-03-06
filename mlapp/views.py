import joblib
import numpy as np

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView
from django.shortcuts import render, redirect

from .forms import LoginForm, InputForm
from .models import Customer


ml_model = joblib.load('ml_model/ml_model.pkl')


class Login(LoginView):
    form_class = LoginForm
    template_name = 'mlapp/templates/login.html'


class Logout(LogoutView):
    template_name = 'mlapp/templates/login.html'


def index(request):
    return render(request, 'mlapp/templates/index.html')


def input_form(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('result')
    else:
        form = InputForm()
        return render(request, 'mlapp/templates/input_form.html', {'form': form})


def result(request):
    data = Customer.objects.order_by('id').reverse().values_list(
        # モデルを学習させた際のカラムの順番
        'limited_balance', 'education', 'marriage', 'age'
    )

    # 推論の実行
    x = np.array([data[0]])
    y = ml_model.predict(x)
    y_proba = ml_model.predict_proba(x) * 100  # 予測確率 * 100
    y, y_proba = y[0], y_proba[0]  # それぞれの0番目を取り出す

    # 推論結果を保存
    customer = Customer.objects.order_by('id').reverse()[0]
    customer.proba = y_proba[y]
    customer.result = y
    customer.save()

    # 推論結果をHTMLに渡す
    return render(
        request,
        'mlapp/templates/result.html',
        {'y': y, 'y_proba': round(y_proba[y], 2)}
    )


class CustomerList(ListView):
    template_name = 'mlapp/templates/history.html'
    model = Customer
