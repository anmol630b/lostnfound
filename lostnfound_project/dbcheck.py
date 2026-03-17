import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostnfound.settings')
django.setup()

from django.db import connection
from items.models import Item, ClaimRequest
from accounts.models import UserProfile
from django.contrib.auth.models import User

print('\n' + '='*55)
print('   DATABASE CONNECTION CHECK')
print('='*55)

# Tables
tables = connection.introspection.table_names()
required = {
    'auth_user':              'Users table',
    'accounts_userprofile':   'User Profiles',
    'items_item':             'Items table',
    'items_claimrequest':     'Claims table',
    'django_session':         'Sessions',
    'django_admin_log':       'Admin logs',
}
print('\n--- Tables ---')
for table, label in required.items():
    status = 'OK  ' if table in tables else 'MISS'
    print(f'  [{status}] {label:25s} ({table})')

# Columns check
print('\n--- Item Model Columns ---')
with connection.cursor() as cur:
    cur.execute("PRAGMA table_info(items_item)")
    cols = [row[1] for row in cur.fetchall()]
    needed = ['id','title','description','category','item_type','location',
              'location_detail','date_lost_found','date_posted','image',
              'status','posted_by_id','contact_email','contact_phone','views_count']
    for c in needed:
        status = 'OK  ' if c in cols else 'MISS'
        print(f'  [{status}] {c}')

print('\n--- Profile Model Columns ---')
with connection.cursor() as cur:
    cur.execute("PRAGMA table_info(accounts_userprofile)")
    cols = [row[1] for row in cur.fetchall()]
    needed = ['id','user_id','phone','city','profile_picture','bio','is_verified']
    for c in needed:
        status = 'OK  ' if c in cols else 'MISS'
        print(f'  [{status}] {c}')

print('\n--- Claims Model Columns ---')
with connection.cursor() as cur:
    cur.execute("PRAGMA table_info(items_claimrequest)")
    cols = [row[1] for row in cur.fetchall()]
    needed = ['id','item_id','claimant_id','message','contact_phone','contact_email','created_at','status']
    for c in needed:
        status = 'OK  ' if c in cols else 'MISS'
        print(f'  [{status}] {c}')

# Counts
print('\n--- Record Counts ---')
print(f'  Users     : {User.objects.count()}')
print(f'  Profiles  : {UserProfile.objects.count()}')
print(f'  Items     : {Item.objects.count()}')
print(f'  Claims    : {ClaimRequest.objects.count()}')

# Foreign key check
print('\n--- Relations Check ---')
try:
    users = User.objects.select_related('profile').all()
    for u in users:
        _ = u.profile
    print(f'  [OK  ] User -> Profile (OneToOne)')
except Exception as e:
    print(f'  [FAIL] User -> Profile: {e}')

try:
    items = Item.objects.select_related('posted_by').all()
    print(f'  [OK  ] Item -> User (ForeignKey)')
except Exception as e:
    print(f'  [FAIL] Item -> User: {e}')

try:
    claims = ClaimRequest.objects.select_related('item','claimant').all()
    print(f'  [OK  ] Claim -> Item + User (ForeignKey)')
except Exception as e:
    print(f'  [FAIL] Claim -> Item: {e}')

# Migration status
print('\n--- Migration Status ---')
from django.db.migrations.executor import MigrationExecutor
executor = MigrationExecutor(connection)
plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
if plan:
    print(f'  [WARN] {len(plan)} unapplied migrations!')
    for migration, _ in plan:
        print(f'    -- {migration}')
else:
    print(f'  [OK  ] All migrations applied')

# Signal check
print('\n--- Signal Check (Auto Profile) ---')
from django.contrib.auth.models import User
orphan = User.objects.filter(profile__isnull=True).count()
if orphan:
    print(f'  [WARN] {orphan} users without profiles — fixing...')
    from accounts.models import UserProfile
    for u in User.objects.filter(profile__isnull=True):
        UserProfile.objects.get_or_create(user=u)
        print(f'    -- Created profile for: {u.username}')
else:
    print(f'  [OK  ] All users have profiles')

print('\n' + '='*55)
print('   DATABASE CHECK COMPLETE')
print('='*55 + '\n')
