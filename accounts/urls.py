from django.urls import path, include
from . import views

urlpatterns = [
    path('perfil/', views.index, name='accounts_index'),
]
