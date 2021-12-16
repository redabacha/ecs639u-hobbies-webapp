from django.shortcuts import render


def register(request):
    return render(request, "hobbies/register.html")


def login(request):
    return render(request, "hobbies/login.html")


def profile(request):
    return render(request, "hobbies/profile.html")


def similar(request):
    return render(request, "hobbies/similar.html")
