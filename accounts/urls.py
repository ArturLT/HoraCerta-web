from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
]