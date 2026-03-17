content = open('accounts/views.py').read()

old = '''    user_items = Item.objects.filter(posted_by=request.user)

    return render(request, 'accounts/profile.html', {
        'u_form':        u_form,
        'p_form':        p_form,
        'items_count':   user_items.count(),
        'lost_count':    user_items.filter(item_type='lost').count(),
        'found_count':   user_items.filter(item_type='found').count(),
        'resolved_count':user_items.filter(status='resolved').count(),
        'claims_count':  request.user.claims.count(),
        'my_lost':       user_items.filter(item_type='lost').order_by('-date_posted'),
        'my_found':      user_items.filter(item_type='found').order_by('-date_posted'),
        'my_claims':     request.user.claims.select_related('item').order_by('-created_at'),
    })'''

new = '''    user_items = Item.objects.filter(posted_by=request.user)
    lost_count     = user_items.filter(item_type='lost').count()
    found_count    = user_items.filter(item_type='found').count()
    resolved_count = user_items.filter(status='resolved').count()
    claims_count   = request.user.claims.count()

    stats = [
        ("Lost Posted",  lost_count,     "#ef4444"),
        ("Found Posted", found_count,    "#10b981"),
        ("Claims Made",  claims_count,   "#f59e0b"),
        ("Resolved",     resolved_count, "#2563eb"),
    ]

    u = request.user
    account_info = [
        ("Username",    "@" + u.username,                          "fa-at",       "#2563eb"),
        ("Email",       u.email or "Not set",                      "fa-envelope", "#6b7280"),
        ("Member Since",u.date_joined.strftime("%d %b %Y"),        "fa-calendar", "#f59e0b"),
        ("Last Login",  u.last_login.strftime("%d %b %Y") if u.last_login else "—", "fa-clock", "#10b981"),
        ("Status",      "Verified ✓" if hasattr(u,"profile") and u.profile.is_verified else "Active", "fa-circle", "#10b981"),
    ]

    return render(request, 'accounts/profile.html', {
        'u_form':       u_form,
        'p_form':       p_form,
        'stats':        stats,
        'account_info': account_info,
    })'''

if old in content:
    content = content.replace(old, new)
    print('Profile view updated!')
else:
    print('Pattern not found exactly - applying fallback...')
    # Fallback - just add stats
    content = content.replace(
        "from .forms import UserRegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm",
        "from .forms import UserRegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm\nfrom items.models import Item"
    )
    print('Import added - please check manually')

open('accounts/views.py', 'w').write(content)
