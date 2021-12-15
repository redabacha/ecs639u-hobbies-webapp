from django.shortcuts import render

# Create your views here.


def register(request):
    return render(request, 'hobbies/register.html')


def login(request):
    return render(request, 'hobbies/login.html')


def profile(request):
    return render(request, 'hobbies/profile.html')


def simmilar(request):
    return render(request, 'hobbies/simmilar.html')
