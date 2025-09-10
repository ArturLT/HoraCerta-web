from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('perfil/', include('accounts.urls')),
    path('calendario/', include('agenda.urls'))
]
