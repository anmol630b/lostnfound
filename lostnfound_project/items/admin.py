from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from .models import Item, ClaimRequest


class ClaimInline(admin.TabularInline):
    model = ClaimRequest
    extra = 0
    readonly_fields = ['claimant', 'contact_email', 'contact_phone', 'message', 'created_at']
    fields = ['claimant', 'contact_email', 'contact_phone', 'status', 'created_at']
    can_delete = True


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'thumb', 'title', 'type_badge', 'cat_col',
        'loc_col', 'status_badge', 'owner_link',
        'claim_count', 'views_count', 'date_posted'
    ]
    list_filter   = ['item_type', 'status', 'category', 'location', 'date_posted']
    search_fields = ['title', 'description', 'posted_by__username', 'contact_email']
    list_per_page = 20
    date_hierarchy = 'date_posted'
    ordering      = ['-date_posted']
    inlines       = [ClaimInline]
    save_on_top   = True
    readonly_fields = ['views_count', 'date_posted', 'img_preview', 'wa_link']

    fieldsets = (
        ('Item Info',    {'fields': ('title', 'description', 'category', 'item_type', 'status')}),
        ('Location',     {'fields': ('location', 'location_detail', 'date_lost_found')}),
        ('Image',        {'fields': ('image', 'img_preview'), 'classes': ('collapse',)}),
        ('Contact',      {'fields': ('contact_email', 'contact_phone', 'wa_link')}),
        ('Meta',         {'fields': ('posted_by', 'date_posted', 'views_count'), 'classes': ('collapse',)}),
    )

    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{0}" style="width:44px;height:44px;object-fit:cover;border-radius:8px;" />',
                obj.image.url
            )
        icons = {'electronics':'📱','books':'📚','id_cards':'🪪','keys':'🔑',
                 'bags':'🎒','clothing':'👕','jewelry':'💍','wallet':'👛',
                 'pets':'🐾','vehicles':'🚗','sports':'⚽','toys':'🎮','other':'📦'}
        return mark_safe(
            '<div style="width:44px;height:44px;background:#e0e7ff;border-radius:8px;'
            'display:flex;align-items:center;justify-content:center;font-size:1.2rem;">'
            + icons.get(obj.category, '📦') + '</div>'
        )
    thumb.short_description = ''

    def type_badge(self, obj):
        if obj.item_type == 'lost':
            return mark_safe('<span style="background:#fee2e2;color:#dc2626;padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;">LOST</span>')
        return mark_safe('<span style="background:#dcfce7;color:#16a34a;padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;">FOUND</span>')
    type_badge.short_description = 'Type'

    def cat_col(self, obj):
        return obj.get_category_display()
    cat_col.short_description = 'Category'

    def loc_col(self, obj):
        return obj.get_location_display()
    loc_col.short_description = 'Location'

    def status_badge(self, obj):
        styles = {
            'active':   'background:#dbeafe;color:#2563eb;',
            'resolved': 'background:#dcfce7;color:#16a34a;',
            'claimed':  'background:#fef9c3;color:#ca8a04;',
        }
        s = styles.get(obj.status, 'background:#f3f4f6;color:#6b7280;')
        return format_html(
            '<span style="{0}padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;">{1}</span>',
            s, obj.status.upper()
        )
    status_badge.short_description = 'Status'

    def owner_link(self, obj):
        url  = reverse('admin:auth_user_change', args=[obj.posted_by.pk])
        name = obj.posted_by.get_full_name() or obj.posted_by.username
        return format_html('<a href="{0}" style="color:#2563eb;font-weight:600;">{1}</a>', url, name)
    owner_link.short_description = 'Posted By'

    def claim_count(self, obj):
        count = obj.claims.count()
        if count:
            return format_html(
                '<span style="background:#fef9c3;color:#ca8a04;padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;">🙋 {0}</span>',
                count
            )
        return mark_safe('<span style="color:#94a3b8;">—</span>')
    claim_count.short_description = 'Claims'

    def img_preview(self, obj):
        if obj.image:
            return format_html('<img src="{0}" style="max-width:260px;border-radius:10px;" />', obj.image.url)
        return '—'
    img_preview.short_description = 'Preview'

    def wa_link(self, obj):
        link = obj.get_whatsapp_link()
        if link:
            return format_html('<a href="{0}" target="_blank" style="color:#25d366;font-weight:600;">Open WhatsApp</a>', link)
        return '—'
    wa_link.short_description = 'WhatsApp'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('posted_by').prefetch_related('claims')


@admin.register(ClaimRequest)
class ClaimAdmin(admin.ModelAdmin):
    list_display  = [
        'item_col', 'itype_col', 'user_col',
        'contact_email', 'contact_phone',
        'status_col', 'msg_col', 'created_at'
    ]
    list_filter   = ['status', 'item__item_type', 'created_at']
    search_fields = ['item__title', 'claimant__username', 'contact_email']
    list_per_page = 25
    ordering      = ['-created_at']
    date_hierarchy = 'created_at'
    save_on_top   = True
    readonly_fields = ['item', 'claimant', 'message', 'contact_email', 'contact_phone', 'created_at']

    fieldsets = (
        ('Claim', {'fields': ('item', 'claimant', 'status')}),
        ('Message', {'fields': ('message',)}),
        ('Contact', {'fields': ('contact_email', 'contact_phone', 'created_at')}),
    )

    def item_col(self, obj):
        url = reverse('admin:items_item_change', args=[obj.item.pk])
        return format_html('<a href="{0}" style="color:#2563eb;font-weight:600;">{1}</a>', url, obj.item.title[:38])
    item_col.short_description = 'Item'

    def itype_col(self, obj):
        if obj.item.item_type == 'lost':
            return mark_safe('<span style="background:#fee2e2;color:#dc2626;padding:2px 8px;border-radius:20px;font-size:0.7rem;font-weight:700;">LOST</span>')
        return mark_safe('<span style="background:#dcfce7;color:#16a34a;padding:2px 8px;border-radius:20px;font-size:0.7rem;font-weight:700;">FOUND</span>')
    itype_col.short_description = 'Type'

    def user_col(self, obj):
        url  = reverse('admin:auth_user_change', args=[obj.claimant.pk])
        name = obj.claimant.get_full_name() or obj.claimant.username
        return format_html('<a href="{0}" style="color:#2563eb;font-weight:600;">{1}</a>', url, name)
    user_col.short_description = 'Claimant'

    def status_col(self, obj):
        styles = {
            'pending':  'background:#fef9c3;color:#ca8a04;',
            'approved': 'background:#dcfce7;color:#16a34a;',
            'rejected': 'background:#fee2e2;color:#dc2626;',
        }
        s = styles.get(obj.status, 'background:#f3f4f6;color:#6b7280;')
        return format_html(
            '<span style="{0}padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;">{1}</span>',
            s, obj.status.upper()
        )
    status_col.short_description = 'Status'

    def msg_col(self, obj):
        msg = obj.message[:55] + '...' if len(obj.message) > 55 else obj.message
        return format_html('<span style="color:#475569;font-size:0.82rem;">{0}</span>', msg)
    msg_col.short_description = 'Message'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('item', 'claimant')
