from django.shortcuts import render


def hellofunction(request):
    return render(request, 'ml_sample/helloworldapp/templates/hello.html')
