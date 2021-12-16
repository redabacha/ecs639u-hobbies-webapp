from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.http.response import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse
import json

from .forms import NewUserForm, UpdateUserForm
from .models import Hobby, User


def auth_check_api(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("profile"))
    else:
        return HttpResponse()


def auth_login_api(request):
    if request.method == "POST":
        body = json.loads(request.body)
        user = authenticate(request, email=body["email"], password=body["password"])

        if user is not None:
            login(request, user)
            return HttpResponsePermanentRedirect(reverse("profile"))

        return HttpResponseBadRequest()


def auth_logout_api(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect(reverse("login"))


def users_api(request):
    if request.method == "POST":
        user_form = NewUserForm(json.loads(request.body))

        if not user_form.is_valid():
            return JsonResponse({"errors": user_form.errors})

        User.objects.create_user(**user_form.cleaned_data)
        return HttpResponseRedirect(reverse("login"))


def user_api(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(User, id=user_id)
        return JsonResponse(user.to_dict())

    if request.method == "PUT":
        body = json.loads(request.body)
        user_form = UpdateUserForm(body, instance=get_object_or_404(User, id=user_id))

        if not user_form.is_valid():
            return JsonResponse({"errors": user_form.errors}, status=400)

        user = user_form.save(commit=False)

        for hobby_id in body["add_hobbies"]:
            hobby = get_object_or_404(Hobby, id=hobby_id)
            user.hobbies.add(hobby)

        for hobby_id in body["remove_hobbies"]:
            hobby = get_object_or_404(Hobby, id=hobby_id)
            user.hobbies.remove(hobby)

        user.save()

        return JsonResponse({"success": True})


def hobbies_api(request):
    if request.method == "POST":
        body = json.loads(request.body)
        new_hobby = Hobby.objects.create(name=body["name"])

        return JsonResponse({"id": new_hobby.id, "name": new_hobby.name})


def user_hobbies_api(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(User, id=user_id)
        user_hobbies = user.get_hobbies()

        return JsonResponse(
            {
                "hobbies": [hobby.to_dict() for hobby in user_hobbies],
                "other_hobbies": [
                    hobby.to_dict()
                    for hobby in Hobby.objects.all().difference(user_hobbies)
                ],
            }
        )


def user_similar_hobbies_api(request, user_id):
    if request.method == "GET":
        hobbies = get_object_or_404(User, id=user_id).hobbies.all()
        today = date.today()

        results = []

        for user in User.objects.all():
            if user.id == user_id or not user.birthday:
                continue

            current_hobbies = user.hobbies.all()
            common_hobbies = [hobby for hobby in hobbies if hobby in current_hobbies]

            result = user.to_dict()
            result["age"] = (
                today.year
                - user.birthday.year
                - ((today.month, today.day) < (user.birthday.month, user.birthday.day))
            )
            result["common_hobbies"] = [hobby.to_dict() for hobby in common_hobbies]

            results.append(result)

        results.sort(reverse=True, key=lambda result: len(result["common_hobbies"]))
        return JsonResponse({"results": results})
