"""
Django settings for horacerta project.
"""

from pathlib import Path
import os

# ==============================
# 🔹 BASE DIR
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# 🔐 CONFIGURAÇÕES DE SEGURANÇA
# ==============================
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-3#x0in(s%3(4nuq*y(f^rdo0665(k+^pyy*ex6c57hgl6v$awz'
)

# DEBUG True para desenvolvimento local, False para produção
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "horacerta-web.onrender.com",
]

# Configuração de CSRF para produção
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
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve arquivos estáticos
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
# 💾 DATABASES
# ==============================
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

# Usa WhiteNoise apenas em produção
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ==============================
# 🆔 CAMPO PADRÃO DE CHAVE PRIMÁRIA
# ==============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
