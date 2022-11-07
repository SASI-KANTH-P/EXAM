from django.urls import path


from .views import *

urlpatterns = [
    path('login',loginUser,name="loginUser"),
    path('register',registerUser,name="registerUser"),
    path('logout',logoutUser,name="logoutUser"),
]
