from django.shortcuts import render, redirect
from .models import Item
from django.contrib.auth.decorators import login_required
from .forms import ItemForm
from .utils import get_period_dates, get_specific_month_dates
from datetime import date
from django.db.models import Sum, DecimalField 

@login_required
def index(request):
    usuario_logado = request.user
    base_queryset = Item.objects.filter(usuario=usuario_logado).order_by('-data_transacao')
    
    view_filter = request.GET.get('view', 'mensal')
    period_filter = request.GET.get('filter_month')

    data_inicio = None
    data_fim = None

    if period_filter and period_filter != 'todos':
        data_inicio, data_fim = get_specific_month_dates(period_filter)
    if data_inicio is None:
        data_inicio, data_fim = get_period_dates(view_filter)
    if data_inicio and data_fim:
        itens_filtrados = base_queryset.filter(
            data_transacao__gte=data_inicio, 
            data_transacao__lte=data_fim
        )
    else:
        itens_filtrados = base_queryset
    
    receitas_queryset = itens_filtrados.filter(tipo='receita')
    despesas_queryset = itens_filtrados.filter(tipo='despesa')

    total_receitas = receitas_queryset.aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = despesas_queryset.aggregate(Sum('valor'))['valor__sum'] or 0
    
    saldo = total_receitas - total_despesas

    context = {
        'itens': itens_filtrados,
        'receitas': total_receitas, 
        'despesas': total_despesas, 
        'saldo': saldo,
        'current_view': view_filter,
        'current_period': period_filter or 'todos',
    }
    return render(request, 'finance/dashboard.html', context)


@login_required
def item_create(request):
    # (Permanece igual)
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            novo_item = form.save(commit=False)
            novo_item.usuario = request.user
            novo_item.save()
            return redirect('finance:finance_list') 
    else:
        form = ItemForm()
    
    return render(request, 'finance/item_create.html', {'form': form})