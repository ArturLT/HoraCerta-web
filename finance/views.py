from django.shortcuts import render
from .models import Item
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    
    usuario_logado = request.user
    
    itens_do_usuario = Item.objects.filter(usuario=usuario_logado)
    
    context = {
        'itens': itens_do_usuario,
    }
    return render(request, 'finance/dashboard.html', context)