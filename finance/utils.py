from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

def get_period_dates(view_filter, data_hoje=None):
    """
    Retorna a data de início e fim do período selecionado.
    """
    if data_hoje is None:
        data_hoje = date.today()
        
    data_inicio = data_hoje
    data_fim = data_hoje # Data de fim padrão é hoje
    
    if view_filter == 'semanal':
        # Começa no dia de hoje menos 7 dias
        data_inicio = data_hoje - timedelta(days=7)
        
    elif view_filter == 'mensal':
        # Começa no primeiro dia do mês atual
        data_inicio = data_hoje.replace(day=1)
        
    elif view_filter == 'anual':
        # Começa no primeiro dia do ano atual
        data_inicio = data_hoje.replace(day=1, month=1)
        
    # Se o filtro não for reconhecido, retorna o mês atual por padrão
    else:
        data_inicio = data_hoje.replace(day=1)

    return data_inicio, data_fim

def get_specific_month_dates(period_filter):
    """
    Retorna o início e o fim de um mês específico (formato MM-YYYY).
    """
    try:
        mes, ano = map(int, period_filter.split('-'))
        periodo_inicio = date(ano, mes, 1)
        # Calcula o último dia do mês
        periodo_fim = periodo_inicio + relativedelta(months=+1) - timedelta(days=1)
        return periodo_inicio, periodo_fim
    except (ValueError, AttributeError):
        # Retorna None se o formato for inválido
        return None, None