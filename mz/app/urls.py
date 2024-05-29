from django.urls import path
from . import views

app_name = "App"

urlpatterns = [
    path('',views.home,name='home'),
    path('subscribers',views.subscribers,name='subscribers'),
    path('delete/<orderNum>',views.delete,name='delete'),
    path('export/<orderNum>',views.export,name='export'),
    path('operations',views.operations,name='operations'),
    path('projects',views.projects,name='projects'),
    path('logout',views.logout,name='logout'),
    path('login',views.login,name='login'),
    path('settings',views.still,name='still'),
    path('export/<fileName>',views.export,name='export'),
]