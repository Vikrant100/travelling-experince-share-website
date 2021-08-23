from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('home', views.HomeView.as_view(), name='all'),
    path('register/', views.register, name='register'),
]
