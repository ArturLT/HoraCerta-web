# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import json

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

@csrf_exempt
def chatbot_response(request):
    if request.method != 'POST':
        return JsonResponse({'resposta': 'Método não permitido.'}, status=405)

    # 1) Ler o corpo da requisição e decodificar corretamente
    try:
        data = json.loads(request.body.decode('utf-8', errors='replace'))
    except Exception:
        return JsonResponse({'resposta': 'Erro: formato inválido de requisição.'}, status=400)

    pergunta = (data.get('mensagem', '') or '').strip()
    if not pergunta:
        return JsonResponse({'resposta': 'Por favor, digite uma pergunta.'}, status=400)

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente amigável sobre finanças."},
                {"role": "user", "content": pergunta},
            ],
            extra_headers={  # ✅ Só uma vez, e sem acentos
                "HTTP-Referer": "http://127.0.0.1:8000",
                "X-Title": "Sistema de Gestao Financeira",
            },
        )

        resposta = completion.choices[0].message.content
        resposta = str(resposta).strip()

    except Exception as e:
        print("Erro no chatbot:", repr(e))
        resposta = "Erro de conexão com o servidor da IA."

    # 3) Retornar JSON sem escapar acentos/emojis
    response = JsonResponse(
        {'resposta': resposta},
        json_dumps_params={'ensure_ascii': False}
    )
    response["Content-Type"] = "application/json; charset=utf-8"
    return response
