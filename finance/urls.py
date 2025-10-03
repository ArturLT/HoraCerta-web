from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.Filtragem, name='finance_list'), 
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('create/', views.item_create, name='item_create'),
    path('relatorio/', views.relario, name='relatorio'),
    path('total_faturado/', views.total_despesas_receitas, name='relatorio_produtos'),
]