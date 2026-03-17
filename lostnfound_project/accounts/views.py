from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from items.models import Item


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.first_name or user.username}! Account created.')
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = UserRegisterForm()
    benefits = [
        'Post unlimited lost & found items',
        'Upload photos of items',
        'WhatsApp & email contact',
        'Submit ownership claims',
        'Get notified when someone claims your item',
    ]
    return render(request, 'accounts/register.html', {'form': form, 'benefits': benefits})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    features = [
        ('fa-bolt',      '#fbbf24', 'Post items in under 2 minutes'),
        ('fa-whatsapp',  '#25d366', 'Connect instantly via WhatsApp'),
        ('fa-search',    '#60a5fa', 'Search by category & location'),
        ('fa-globe',     '#a78bfa', 'Open to everyone — 100% free'),
    ]
    return render(request, 'accounts/login.html', {'form': form, 'features': features})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been signed out.')
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    user_items = Item.objects.filter(posted_by=request.user)
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
    })
