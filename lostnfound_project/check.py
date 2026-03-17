import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostnfound.settings')
django.setup()

OK   = 'OK  '
FAIL = 'FAIL'
WARN = 'WARN'

print()
print('='*50)
print('   LOSTNFOUND — COMPLETE FINAL TEST')
print('='*50)

errors = []

# 1. Settings
from django.conf import settings
print(f'\n[{OK}] Django {django.__version__}')
print(f'[{OK}] Site: {getattr(settings, "SITE_NAME","NOT SET")}')
print(f'[{OK}] Email: {settings.EMAIL_BACKEND.split(".")[-1]}')

# 2. Database
from items.models import Item, ClaimRequest
from accounts.models import UserProfile
from django.contrib.auth.models import User
print(f'\n[{OK}] Users     : {User.objects.count()}')
print(f'[{OK}] Profiles  : {UserProfile.objects.count()}')
print(f'[{OK}] Items     : {Item.objects.count()}')
print(f'[{OK}] Claims    : {ClaimRequest.objects.count()}')

# 3. Profile fields
profile_fields = [f.name for f in UserProfile._meta.get_fields()]
print('\n--- Profile Fields ---')
for f in ['user','phone','city','profile_picture','bio','is_verified']:
    status = OK if f in profile_fields else FAIL
    if status == FAIL: errors.append(f'Profile field missing: {f}')
    print(f'  [{status}] {f}')

# 4. Item fields
item_fields = [f.name for f in Item._meta.get_fields()]
print('\n--- Item Fields ---')
for f in ['title','description','category','item_type','location',
          'location_detail','date_lost_found','image','status',
          'posted_by','contact_email','contact_phone','views_count']:
    status = OK if f in item_fields else FAIL
    if status == FAIL: errors.append(f'Item field missing: {f}')
    print(f'  [{status}] {f}')

# 5. Templates
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
print(f'\n--- Templates ---')
for t in templates:
    path = settings.BASE_DIR / 'templates' / t
    if os.path.exists(str(path)):
        size = os.path.getsize(str(path))
        if size < 100:
            print(f'  [WARN] {t} — only {size} bytes, might be empty!')
            errors.append(f'Empty template: {t}')
        else:
            print(f'  [{OK}] {t} ({size} bytes)')
    else:
        print(f'  [{FAIL}] {t} — MISSING')
        errors.append(f'Missing template: {t}')

# 6. Static files
print('\n--- Static Files ---')
for f in ['css/style.css', 'js/main.js']:
    path = settings.BASE_DIR / 'static' / f
    if os.path.exists(str(path)):
        size = os.path.getsize(str(path))
        print(f'  [{OK}] {f} ({size} bytes)')
    else:
        print(f'  [{FAIL}] {f} — MISSING')
        errors.append(f'Missing static: {f}')

# 7. URLs
from django.urls import reverse
print('\n--- URLs ---')
for name in ['home','item_list','post_lost','post_found',
             'register','login','logout','profile',
             'my_items','pdf_report','password_reset']:
    try:
        url = reverse(name)
        print(f'  [{OK}] {name:25s} -> {url}')
    except Exception as e:
        print(f'  [{FAIL}] {name:25s} -> {e}')
        errors.append(f'Broken URL: {name}')

# 8. Database tables
from django.db import connection
tables = connection.introspection.table_names()
print('\n--- Database Tables ---')
for t in ['items_item','items_claimrequest','accounts_userprofile','auth_user']:
    status = OK if t in tables else FAIL
    if status == FAIL: errors.append(f'Missing table: {t}')
    print(f'  [{status}] {t}')

# 9. Superuser
print('\n--- Admin Users ---')
admins = User.objects.filter(is_superuser=True)
if admins.exists():
    for a in admins:
        print(f'  [{OK}] {a.username} ({a.email})')
else:
    print(f'  [{WARN}] No superuser! Run: python manage.py createsuperuser')

# Final result
print()
print('='*50)
if errors:
    print(f'  ISSUES FOUND: {len(errors)}')
    for e in errors:
        print(f'  -- {e}')
else:
    print('  ALL CHECKS PASSED — PROJECT IS READY!')
print('='*50)
