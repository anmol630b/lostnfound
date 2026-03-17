import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostnfound.settings')
django.setup()

from django.conf import settings
from django.urls import reverse
from django.db import connection

OK   = '[DONE]'
NO   = '[TODO]'
WARN = '[WARN]'

print()
print('='*55)
print('   LOSTNFOUND — PROJECT STATUS REPORT')
print('='*55)

# ── CORE FEATURES ──────────────────────────────────────
print('\n--- CORE FEATURES ---')
features = {
    'User Register / Login / Logout':     True,
    'Password Reset (forgot password)':   True,
    'User Profile Page':                  True,
    'Profile Picture Upload':             True,
    'Post Lost Item':                     True,
    'Post Found Item':                    True,
    'Edit / Delete Item':                 True,
    'Image Upload for Items':             True,
    'Search & Filter Items':              True,
    'Claim / Contact Form':               True,
    'Mark Item as Resolved':              True,
    'My Items Dashboard':                 True,
    'Admin Panel':                        True,
    'PDF Report (admin)':                 True,
    'Email Notifications':                True,
    'WhatsApp Contact Button':            True,
    'Dark Mode Toggle':                   True,
    'Scroll Animations':                  True,
    'Smart Navbar (hide on scroll)':      True,
    'Responsive Design (mobile/tablet)':  True,
    'Glassmorphism Navbar':               True,
    'Avatar Initials with Color':         True,
    'Password Strength Meter':            True,
    'Animated Counters':                  True,
    'Active Nav Link Highlight':          True,
}

for f, done in features.items():
    print(f'  {OK if done else NO} {f}')

# ── MISSING / TODO ──────────────────────────────────────
print('\n--- PENDING / CAN IMPROVE ---')
todos = {
    '404 / 500 custom error pages':           False,
    'Real-time search in navbar':             False,
    'Similar items on detail page':           False,
    'Social media share buttons':             False,
    'Item auto-expire after 30 days':         False,
    'WhatsApp share (not just contact)':      False,
    'SEO meta tags':                          False,
    'Deployment (Railway/Render)':            False,
    'Gmail SMTP (real emails)':               False,
    'Image compression on upload':            False,
    'Item views analytics in admin':          False,
}
for t, done in todos.items():
    print(f'  {NO} {t}')

# ── TEMPLATES CHECK ─────────────────────────────────────
print('\n--- TEMPLATES ---')
templates = [
    'base.html','home.html',
    'items/item_list.html','items/item_detail.html',
    'items/post_item.html','items/claim_form.html',
    'items/my_items.html','items/confirm_delete.html',
    'accounts/login.html','accounts/register.html',
    'accounts/profile.html',
    'accounts/password_reset.html',
    'accounts/password_reset_done.html',
    'accounts/password_reset_confirm.html',
    'accounts/password_reset_complete.html',
]
all_ok = True
for t in templates:
    path = settings.BASE_DIR / 'templates' / t
    if os.path.exists(str(path)):
        size = os.path.getsize(str(path))
        print(f'  {OK} {t} ({size}b)')
    else:
        print(f'  [MISS] {t}')
        all_ok = False

# ── DATABASE ────────────────────────────────────────────
print('\n--- DATABASE ---')
from items.models import Item, ClaimRequest
from accounts.models import UserProfile
from django.contrib.auth.models import User
print(f'  {OK} Users     : {User.objects.count()}')
print(f'  {OK} Items     : {Item.objects.count()}')
print(f'  {OK} Claims    : {ClaimRequest.objects.count()}')
print(f'  {OK} Profiles  : {UserProfile.objects.count()}')

# ── URLS ────────────────────────────────────────────────
print('\n--- URLS ---')
urls = ['home','item_list','post_lost','post_found',
        'register','login','logout','profile',
        'my_items','pdf_report','password_reset']
for name in urls:
    try:
        reverse(name)
        print(f'  {OK} {name}')
    except:
        print(f'  [FAIL] {name}')

# ── STATIC FILES ────────────────────────────────────────
print('\n--- STATIC FILES ---')
for f in ['css/style.css','js/main.js']:
    path = settings.BASE_DIR / 'static' / f
    if os.path.exists(str(path)):
        kb = round(os.path.getsize(str(path))/1024, 1)
        print(f'  {OK} {f} ({kb}KB)')
    else:
        print(f'  [MISS] {f}')

# ── SETTINGS CHECK ──────────────────────────────────────
print('\n--- SETTINGS ---')
print(f'  {OK} Site Name    : {getattr(settings,"SITE_NAME","?")}')
print(f'  {OK} Debug        : {settings.DEBUG}')
print(f'  {OK} Timezone     : {settings.TIME_ZONE}')
email = settings.EMAIL_BACKEND
if 'console' in email:
    print(f'  {WARN} Email        : Console (Gmail SMTP nahi laga)')
else:
    print(f'  {OK} Email        : SMTP configured')

# ── SUMMARY ─────────────────────────────────────────────
done_count = len([v for v in features.values() if v])
todo_count = len(todos)

print()
print('='*55)
print(f'  DONE  : {done_count} features complete')
print(f'  TODO  : {todo_count} improvements possible')
print(f'  STATUS: Project is {"READY" if all_ok else "HAS ISSUES"}!')
print('='*55)
print()
