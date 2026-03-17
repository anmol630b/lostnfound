from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-lostnfound-general-public-portal-2024-xyz'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'items.apps.ItemsConfig',
    'accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'items.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'lostnfound.urls'

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
                'lostnfound.context_processors.site_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'lostnfound.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ══ GMAIL SMTP SETUP ══════════════════════════════
# Step 1: Gmail > myaccount.google.com > Security
# Step 2: 2-Step Verification ON karo
# Step 3: App Passwords > Generate 16-char password
# Step 4: Neeche apna email aur password daalo
# ═════════════════════════════════════════════════
EMAIL_BACKEND    = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST       = 'smtp.gmail.com'
EMAIL_PORT       = 587
EMAIL_USE_TLS    = True
EMAIL_HOST_USER  = 'your_gmail@gmail.com'      # <-- CHANGE THIS
EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx xxxx'    # <-- CHANGE THIS (App Password)
# To use console backend during development, comment above and uncomment below:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'LostNFound <noreply@lostnfound.com>'

# ── Site Info ──────────────────────────
SITE_NAME        = 'LostNFound'
SITE_TAGLINE     = 'Find What You Lost. Return What You Found.'
SITE_DESCRIPTION = 'A free community platform to post lost and found items. Help others and get help when you need it most.'

# Admin Custom CSS
ADMIN_EXTRA_CSS = 'css/admin_custom.css'
