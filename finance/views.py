from django.shortcuts import render, redirect
from .models import Item
from django.contrib.auth.decorators import login_required
from .forms import ItemForm
from .utils import get_period_dates, get_specific_month_dates
from datetime import datetime
from django.db.models import Sum
from django.http import JsonResponse


@login_required
def Dashboard(request):
    receitas_queryset = Item.objects.all().filter(tipo='receita')
    despesas_queryset = Item.objects.all().filter(tipo='despesa')

    total_receitas = receitas_queryset.aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = despesas_queryset.aggregate(Sum('valor'))['valor__sum'] or 0
    
    
    saldo = total_receitas - total_despesas

    context ={
        'receitas': total_receitas, 
        'despesas': total_despesas, 
        'saldo': saldo,
    }
    return render(request, 'finance/Dashboard.html', context)

@login_required
def total_despesas_receitas(request):
    total_receita = Item.objects.all().filter(tipo='receita')
    total_despesas = Item.objects.all().filter(tipo='despesa')

    soma_receita = total_receita.aggregate(Sum('total'))[total_receita]
    soma_despesas = total_despesas.aggregate(Sum('total'))[total_despesas]

    if request.method == "GET":
        return JsonResponse({'soma_receita': soma_receita, 'soma_despesas': soma_despesas})

@login_required
def Filtragem(request):
    usuario_logado = request.user
    base_queryset = Item.objects.filter(usuario=usuario_logado).order_by('data_transacao')
    
    view_filter = request.GET.get('view', 'meses')
    period_filter = request.GET.get('filter_month')

    data_inicio = None
    data_fim = None

    if not period_filter or period_filter == 'todos':
        itens_filtrados = base_queryset
    else:
        if period_filter:
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
   

    context = {
        'itens': itens_filtrados,
        'current_view': view_filter,
        'current_period': 'todos' or period_filter,
    }
    return render(request, 'finance/Receita_Despesas.html', context)


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

@login_required
def relario(request):
    usuario = request.user
    receitas = Item.objects.filter(tipo='receita', usuario=usuario)
    despesas = Item.objects.filter(tipo='despesa', usuario=usuario)

    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    data1, data2, labels = [], [], []

    mes = datetime.now().month + 1
    ano = datetime.now().year

    for _ in range(12):
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1

        r_total = receitas.filter(data_transacao__month=mes, data_transacao__year=ano).aggregate(Sum('valor'))['valor__sum'] or 0
        d_total = despesas.filter(data_transacao__month=mes, data_transacao__year=ano).aggregate(Sum('valor'))['valor__sum'] or 0

        labels.append(meses[mes - 1])
        data1.append(r_total)
        data2.append(d_total)

    return JsonResponse({
        'data1': data1[::-1],
        'data2': data2[::-1],
        'labels': labels[::-1]
    })

