from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone', 'email', 'usuario')
    list_filter = ('usuario',)
    search_fields = ('nome', 'cpf', 'telefone', 'email')
    ordering = ('nome',)
    fieldsets = (
        (None, {
            'fields': ('usuario', 'nome', 'cpf', 'telefone', 'email', 'endereco')
        }),
    )