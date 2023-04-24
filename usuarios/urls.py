from django.urls import path
from . import views

urlpatterns = [
  path('cadastro/', views.cadastro, name="cadastro"),
  path('login/', views.user_login, name="user_login"),
  path('exit/', views.exit, name="exit")
]