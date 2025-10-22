from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.Filtragem, name='finance_list'), 
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('create/', views.item_create, name='item_create'),
    path('relatorio/', views.relario, name='relatorio'),
    path('total_faturado/', views.total_despesas_receitas, name='relatorio_produtos'),
    path('delete/<int:pk>/', views.item_delete, name='item_delete'),
    path('item/<int:pk>/delete-ajax/', views.item_delete_ajax, name='item_delete_ajax'),
    path('item/<int:pk>/edit/', views.item_edit, name='item_edit'),
]