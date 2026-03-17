from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['phone', 'city', 'bio', 'profile_picture', 'is_verified']


class CustomUserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = [
        'avatar_col', 'username', 'get_full_name', 'email',
        'city_col', 'items_col', 'is_staff', 'date_joined'
    ]
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['-date_joined']
    list_per_page = 20

    def avatar_col(self, obj):
        try:
            if obj.profile and obj.profile.profile_picture:
                return format_html(
                    '<img src="{0}" style="width:34px;height:34px;border-radius:50%;object-fit:cover;" />',
                    obj.profile.profile_picture.url
                )
        except Exception:
            pass
        name    = obj.get_full_name() or obj.username
        initial = name[0].upper() if name else 'U'
        palette = ['#2563eb','#7c3aed','#db2777','#dc2626','#059669','#d97706']
        color   = palette[ord(initial) % len(palette)]
        return format_html(
            '<div style="width:34px;height:34px;border-radius:50%;background:{0};'
            'display:inline-flex;align-items:center;justify-content:center;'
            'color:white;font-weight:700;font-size:0.8rem;">{1}</div>',
            color, initial
        )
    avatar_col.short_description = ''

    def city_col(self, obj):
        try:
            city = obj.profile.city
        except Exception:
            city = ''
        if city:
            return format_html('<span style="color:#475569;">📍 {0}</span>', city)
        return mark_safe('<span style="color:#94a3b8;">—</span>')
    city_col.short_description = 'City'

    def items_col(self, obj):
        count = obj.items.count()
        if count:
            url = reverse('admin:items_item_changelist') + '?posted_by__id=' + str(obj.pk)
            return format_html(
                '<a href="{0}" style="background:#dbeafe;color:#2563eb;padding:2px 8px;'
                'border-radius:20px;font-size:0.72rem;font-weight:700;'
                'text-decoration:none;">📦 {1}</a>',
                url, count
            )
        return mark_safe('<span style="color:#94a3b8;">0</span>')
    items_col.short_description = 'Items'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile').prefetch_related('items')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ['avatar_col', 'user_col', 'phone', 'city', 'verified_col', 'items_col']
    list_filter   = ['is_verified']
    search_fields = ['user__username', 'user__email', 'phone', 'city']
    list_per_page = 20
    readonly_fields = ['user', 'pic_preview']

    fieldsets = (
        ('User',    {'fields': ('user',)}),
        ('Details', {'fields': ('phone', 'city', 'bio')}),
        ('Picture', {'fields': ('profile_picture', 'pic_preview')}),
        ('Status',  {'fields': ('is_verified',)}),
    )

    def avatar_col(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{0}" style="width:34px;height:34px;border-radius:50%;object-fit:cover;" />',
                obj.profile_picture.url
            )
        name    = obj.user.get_full_name() or obj.user.username
        initial = name[0].upper() if name else 'U'
        palette = ['#2563eb','#7c3aed','#db2777','#059669','#d97706']
        color   = palette[ord(initial) % len(palette)]
        return format_html(
            '<div style="width:34px;height:34px;border-radius:50%;background:{0};'
            'display:inline-flex;align-items:center;justify-content:center;'
            'color:white;font-weight:700;font-size:0.8rem;">{1}</div>',
            color, initial
        )
    avatar_col.short_description = ''

    def user_col(self, obj):
        url  = reverse('admin:auth_user_change', args=[obj.user.pk])
        name = obj.user.get_full_name() or obj.user.username
        return format_html(
            '<a href="{0}" style="color:#2563eb;font-weight:600;">{1}</a>',
            url, name
        )
    user_col.short_description = 'User'

    def verified_col(self, obj):
        if obj.is_verified:
            return mark_safe(
                '<span style="background:#dcfce7;color:#16a34a;padding:2px 8px;'
                'border-radius:20px;font-size:0.72rem;font-weight:700;">✓ Yes</span>'
            )
        return mark_safe(
            '<span style="background:#f3f4f6;color:#9ca3af;padding:2px 8px;'
            'border-radius:20px;font-size:0.72rem;">No</span>'
        )
    verified_col.short_description = 'Verified'

    def items_col(self, obj):
        count = obj.user.items.count()
        return format_html(
            '<span style="font-weight:600;color:#2563eb;">{0}</span>', count
        )
    items_col.short_description = 'Items'

    def pic_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{0}" style="max-width:180px;border-radius:10px;" />',
                obj.profile_picture.url
            )
        return '—'
    pic_preview.short_description = 'Preview'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').prefetch_related('user__items')
