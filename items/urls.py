from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.aluguel_list, name='aluguel_list'),
    path('create/', views.criar_item, name='criar_item'),
    path('edit/<int:pk>/', views.editar_item, name='editar_item'),
    path('delete/<int:pk>/', views.item_delete, name='item_delete'),
]
