"""
Django settings for horacerta project.
"""

from pathlib import Path
import os
import dj_database_url # Usado para parsear a DATABASE_URL do Render

# ==============================
# 🔹 BASE DIR
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# 🔐 CONFIGURAÇÕES DE SEGURANÇA
# ==============================
# OBTEM A SECRET KEY DAS VARIÁVEIS DE AMBIENTE. É CRÍTICO!
# OBTEM A SECRET KEY DO NOME DA VARIÁVEL DE AMBIENTE.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY') 

# DEBUG: True para local, False para produção.
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Se a chave secreta não estiver definida E DEBUG for False, falhe (Produção).
if not SECRET_KEY and not DEBUG:
    raise Exception("SECRET_KEY não definida em ambiente de produção (DEBUG=False).")

# Se a chave secreta não estiver definida E DEBUG for True, use uma chave de desenvolvimento.
elif not SECRET_KEY and DEBUG:
    # Apenas para desenvolvimento local. NÃO USE ESTE VALOR EM PRODUÇÃO!
    SECRET_KEY = 'django-insecure-chave-de-desenvolvimento-local'

# ALLOWED_HOSTS
# Em produção, ele permite requisições do seu domínio no Render.
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "horacerta-web.onrender.com",
]

# Configuração de CSRF para produção no Render
CSRF_TRUSTED_ORIGINS = [
    "https://horacerta-web.onrender.com",
    "https://*.onrender.com",
]

# ==============================
# 📦 INSTALLED APPS
# ==============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps do projeto
    'accounts',
    'agenda',
    'finance',
    'items',
    'clients',
    'itemAlugados',
    'chat',
]

# ==============================
# ⚙️ MIDDLEWARE
# ==============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Middleware para servir estáticos em produção
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==============================
# URLS E WSGI
# ==============================
ROOT_URLCONF = 'horacerta.urls'
WSGI_APPLICATION = 'horacerta.wsgi.application'

# ==============================
# 🧩 TEMPLATES
# ==============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==============================
# 💾 DATABASES - **CRÍTICO PARA O RENDER**
# ==============================
# Verifica se a DATABASE_URL está definida (Ambiente de Produção/Render)
if os.getenv("DATABASE_URL"):
    # Usa dj_database_url para configurar o PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600  # Opcional: tempo de vida máximo da conexão
        )
    }
else:
    # Configuração de fallback para desenvolvimento local (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==============================
# 🔑 AUTENTICAÇÃO
# ==============================
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailOrNomeBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'accounts.User'

# ==============================
# 🌍 INTERNACIONALIZAÇÃO
# ==============================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ==============================
# 🖼️ ARQUIVOS ESTÁTICOS
# ==============================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Usa WhiteNoise apenas em produção (quando DEBUG é False)
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ==============================
# 🆔 CAMPO PADRÃO DE CHAVE PRIMÁRIA
# ==============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'