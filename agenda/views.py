from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from .models import Agenda
from .forms import AgendaForm
from django.http import JsonResponse



@login_required
def criar_agenda(request):
    """Cria manualmente um novo evento na agenda."""
    initial_data = {}
    # Se o parâmetro data_evento vier na URL, já preenche o formulário
    if 'data_evento' in request.GET:
        initial_data['data_evento'] = request.GET['data_evento']

    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            agenda = form.save(commit=False)
            agenda.usuario = request.user
            agenda.save()
            return redirect('agenda:agenda_list')
    else:
        form = AgendaForm(initial=initial_data)

    return render(request, 'agenda_form.html', {'form': form})



@login_required
def editar_agenda(request, pk):
    """Edita um evento existente."""
    agenda = get_object_or_404(Agenda, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = AgendaForm(request.POST, instance=agenda)
        if form.is_valid():
            form.save()
            return redirect('agenda:agenda_calendario')
    else:
        form = AgendaForm(instance=agenda)
    return render(request, 'agenda_form.html', {'form': form, 'agenda': agenda})


@login_required
def deletar_agenda(request, pk):
    """Exclui um evento."""
    agenda = get_object_or_404(Agenda, pk=pk, usuario=request.user)
    agenda.delete()
    return redirect('agenda:agenda_calendario')


@login_required
def api_eventos(request):
    """Retorna os eventos da agenda no formato JSON para o FullCalendar."""
    eventos = Agenda.objects.filter(usuario=request.user)
    data = []
    for ag in eventos:
        data.append({
            'id': ag.id,
            'title': f"{ag.cliente.nome} - {ag.status}",
            'start': ag.data_evento.strftime('%Y-%m-%d'),
            'description': ag.descricao,
            'status': ag.status,
            'color': (
                '#ffcc00' if ag.status == 'pendente'
                else '#4caf50' if ag.status == 'confirmado'
                else '#f44336'
            ),
        })
    return JsonResponse(data, safe=False)

@login_required
def agenda_calendario(request):
    """Renderiza a agenda visual com FullCalendar."""
    return render(request, 'agenda_calendario.html')


@method_decorator(login_required, name='dispatch')
class AgendaView(DetailView):
    model = Agenda
    template_name = 'agenda_view.html'
    context_object_name = 'agenda'
