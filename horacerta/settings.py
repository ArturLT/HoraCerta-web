"""
Django settings para horacerta - pronto para deploy no Railway
"""

from pathlib import Path
import os
import sys
import dj_database_url
import logging

# ==============================
# 🔹 BASE DIR
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# 🔐 SEGURANÇA
# ==============================
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '!!7#s1d5dj9fhlk^v6wyx81p2e@@o2#d0_zn(u^1j*=&^$r=ri')
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

# ==============================
# 🌐 HOSTS E CSRF
# ==============================
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    "https://horacerta-web-production.up.railway.app",
]

# ==============================
# 📦 APLICATIVOS INSTALADOS
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
    'whitenoise.middleware.WhiteNoiseMiddleware',  # serve arquivos estáticos em produção
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==============================
# 🔗 URLs e WSGI
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
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==============================
# 💾 BANCO DE DADOS (Railway)
# ==============================
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
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

# WhiteNoise - produção
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ==============================
# 🆔 PADRÃO PRIMARY KEY
# ==============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================
# ⚠️ LOGGING (debug em produção)
# ==============================
if not DEBUG:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(asctime)s %(message)s",
    )
    logging.info("🚀 Django rodando em produção (DEBUG=False)")
    logging.info(f"ALLOWED_HOSTS={ALLOWED_HOSTS}")
    logging.info(f"CSRF_TRUSTED_ORIGINS={CSRF_TRUSTED_ORIGINS}")

# ==============================
# 🧹 COLETA AUTOMÁTICA DE STATICFILES (Railway)
# ==============================
if 'collectstatic' in sys.argv:
    print("👉 Coletando arquivos estáticos...")
