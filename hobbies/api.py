from django.http import JsonResponse
from django.http.response import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404
from .models import Hobby, User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from datetime import date
import json


def user_auth_api(request):
    if request.method == "POST":
        body = json.loads(request.body)
        user = authenticate(request, email=body["email"], password=body["password"])
        if user is not None:
            login(request, user)
            return HttpResponsePermanentRedirect(reverse("profile"))
        else:
            return HttpResponseBadRequest()


def users_api(request):
    if request.method == "POST":
        body = json.loads(request.body)
        username = body["username"]
        email = body["email"]
        password = body["password"]

        for user in User.objects.all():
            if user.username == username:
                return JsonResponse({"status": "1"})
        for user in User.objects.all():
            if user.email == email:
                return JsonResponse({"status": "2"})

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.save()
        return HttpResponseRedirect(reverse("login"))


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
        user.username = body["name"]
        user.email = body["email"]
        user.city = body["city"]
        user.birthday = body["date"]
        user.img = body["url"]
        add = body["add"]
        for hobby_id in add:
            hobby = get_object_or_404(Hobby, id=hobby_id)
            user.hobbies.add(hobby)
        remove = body["remove"]
        for hobby_id in remove:
            hobby = get_object_or_404(Hobby, id=hobby_id)
            user.hobbies.remove(hobby)
        user.save()
        return JsonResponse({})
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect(reverse("login"))


def hobbies_api(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(User, id=user_id)
        return JsonResponse(
            {
                "hobbies": [hobby.to_dict() for hobby in user.getHobbies()],
                "all_hobbies_outside": [
                    hobby.to_dict()
                    for hobby in list(
                        set(Hobby.objects.all()).difference(user.getHobbies())
                    )
                ],
            }
        )
    if request.method == "POST":
        body = json.loads(request.body)
        newHobby = Hobby.objects.create(name=body["name"])
        newHobby.save()
        return JsonResponse({"id": newHobby.id})


def users_hobbies_api(request, user_id):
    users = []
    for user in User.objects.all():
        if user.id == user_id:
            continue
        mainUserHobbies = get_object_or_404(User, id=user_id).hobbies.all()
        currentUserHobbies = user.hobbies.all()
        common = [value for value in mainUserHobbies if value in currentUserHobbies]
        obj = user.to_dict()
        obj["common"] = len(common)
        obj["date"] = obj["date"].date()
        today = date.today()
        age = (
            today.year
            - obj["date"].year
            - ((today.month, today.day) < (obj["date"].month, obj["date"].day))
        )
        obj["age"] = age
        users.append(obj)
    users.sort(reverse=True, key=lambda list: list["common"])
    return JsonResponse({"users": [user for user in users]})
