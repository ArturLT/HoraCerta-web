from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path('criar/', views.criar_agenda, name='criar_agenda'),
    path('editar/<int:pk>/', views.editar_agenda, name='editar_agenda'),
    path('deletar/<int:pk>/', views.deletar_agenda, name='deletar_agenda'),
    path('calendario/', views.agenda_calendario, name='agenda_calendario'),  # Novo
    path('api/eventos/', views.api_eventos, name='api_eventos'),  # API JSON
    path('visualizar/<int:pk>/', views.AgendaView.as_view(), name='visualizar_agenda'),
]
    