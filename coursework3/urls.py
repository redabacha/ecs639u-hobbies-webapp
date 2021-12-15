"""coursework3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from hobbies.api import users_api, user_auth_api, check_auth, user_api, hobbies_api, users_hobbies_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hobbies.urls')),
    path('create_user/', users_api, name="users api"),
    path('authenticate_user/', user_auth_api, name="user auth api"),
    path('check_auth/', check_auth, name="check auth"),
    path('api/user/<int:user_id>/', user_api, name="user api"),
    path('api/hobbies/<int:user_id>/', hobbies_api, name="hobbies api"),
    path('api/users_hobbies/<int:user_id>/',
         users_hobbies_api, name="users hobbies api"),
]
