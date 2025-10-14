from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.listar_clientes, name='cliente_list'),
    path('novo/', views.criar_cliente, name='cliente_create'),
]
