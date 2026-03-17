content = open('lostnfound/settings.py').read()

old = "EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'"
new = """# ══ GMAIL SMTP SETUP ══════════════════════════════
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
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'"""

if old in content:
    content = content.replace(old, new)
    print('Gmail SMTP: configured!')
else:
    print('Email: already configured or not found')

open('lostnfound/settings.py', 'w').write(content)
print('Done!')
