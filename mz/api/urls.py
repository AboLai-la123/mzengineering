from django.urls import path
from . import views

app_name = "App"

urlpatterns = [
    path('login',views.login,name='loginApi'),
    path('home', views.home.as_view(), name='homeApi'),
    path('csrfmiddlewaretoken',views.csrfmiddlewaretoken,name='csrfmiddlewaretoken'),
    path('check-data', views.checkData, name='checkData'),
    path('get-data', views.getData.as_view(), name='getData'),
]