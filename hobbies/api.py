from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Hobby, User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


import json


@csrf_exempt
def user_auth_api(request):

    if request.method == "POST":
        body = json.loads(request.body)
        email = body['email']
        password = body['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponsePermanentRedirect(reverse('profile'))
        else:
            return HttpResponseBadRequest()


def users_api(request):
    if request.method == "POST":
        body = json.loads(request.body)
        username = body['username']
        email = body['email']
        password = body['password']

        for user in User.objects.all():
            if user.username == username:
                return JsonResponse({'status': '1'})
        for user in User.objects.all():
            if user.email == email:
                return JsonResponse({'status': '2'})

        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.save()
        return HttpResponseRedirect(reverse('login'))


def check_auth(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("profile"))
    else:
        return HttpResponse()


def user_api(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(User, id=user_id)
        return JsonResponse(user.to_dict())
    if request.method == "PUT":
        user = get_object_or_404(User, id=user_id)
        body = json.loads(request.body)
        user.username = body['name']
        user.email = body['email']
        user.city = body['city']
        user.birthday = body['date']
        user.img = body['url']
        add = body['add']
        for hobby_id in add:
            hobby = get_object_or_404(Hobby, id=hobby_id)
            user.hobbies.add(hobby)
        remove = body['remove']
        for hobby_id in remove:
            hobby = get_object_or_404(Hobby, id=hobby_id)
            user.hobbies.remove(hobby)
        user.save()
        return JsonResponse({})
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect(reverse('login'))


def hobbies_api(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(User, id=user_id)
        return JsonResponse({
            'hobbies': [
                hobby.to_dict()
                for hobby in user.getHobbies()
            ],
            'all_hobbies_outside': [
                hobby.to_dict()
                for hobby in list(set(Hobby.objects.all()).difference(user.getHobbies()))
            ],
        })
    if request.method == "POST":
        body = json.loads(request.body)
        newHobby = Hobby.objects.create(
            name=body["name"])
        newHobby.save()
        return JsonResponse({'id': newHobby.id})
