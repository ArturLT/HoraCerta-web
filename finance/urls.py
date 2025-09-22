from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.index, name='finance_list'), 
    path('create/', views.item_create, name='item_create'),
   # path('adicionar/', views.item_create, name='item_create'), 
]