"""
Django settings for horacerta project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# 🔐 Configurações de Segurança
# ==============================

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-3#x0in(s%3(4nuq*y(f^rdo0665(k+^pyy*ex6c57hgl6v$awz')

# DEBUG = True (local) / False (produção)
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Em produção, defina no Fly.io a variável de ambiente:
# fly secrets set DEBUG=False
ALLOWED_HOSTS = [
    "horacerta-web.onrender.com",
    "127.0.0.1",
    "localhost",
]

CSRF_TRUSTED_ORIGINS = [
    "https://horacerta-web.onrender.com",
]

# ==============================
# 📦 Aplicações
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
# ⚙️ Middleware
# ==============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # necessário para servir estáticos no Fly.io
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Serve arquivos estáticos com cache e compressão
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ROOT_URLCONF = 'horacerta.urls'

# ==============================
# 🧩 Templates
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

WSGI_APPLICATION = 'horacerta.wsgi.application'

# ==============================
# 💾 Banco de Dados
# ==============================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==============================
# 🔑 Autenticação
# ==============================

AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailOrNomeBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'accounts.User'

# ==============================
# 🌍 Internacionalização
# ==============================

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==============================
# 🖼️ Arquivos Estáticos
# ==============================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# ==============================
# 🆔 Campo padrão de chave primária
# ==============================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
