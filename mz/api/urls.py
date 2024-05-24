from django.urls import path
from . import views

app_name = "App"

urlpatterns = [
    path('login',views.login,name='loginApi'),
    path('home', views.home.as_view(), name='homeApi'),
]