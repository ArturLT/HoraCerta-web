from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('auth/', include('finance.urls')),
    path('calendario/', include('agenda.urls')),
    path('aluguel', include('items.urls')),
]
