from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login, name="login"),
    path('profile/', views.profile, name="profile"),
    path('simmilar/', views.simmilar, name="simmilar")

]
