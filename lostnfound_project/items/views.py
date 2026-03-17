from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from .models import Item, ClaimRequest
from .forms import ItemForm, SearchForm, ClaimForm


# ── ERROR HANDLERS ────────────────────────────────────────────
def error_404(request, exception=None):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)

def error_403(request, exception=None):
    return render(request, '403.html', status=403)


# ── HOME ──────────────────────────────────────────────────────
def home_view(request):
    recent_lost  = Item.objects.filter(item_type='lost', status='active')[:6]
    recent_found = Item.objects.filter(item_type='found', status='active')[:6]
    context = {
        'recent_lost':    recent_lost,
        'recent_found':   recent_found,
        'total_lost':     Item.objects.filter(item_type='lost', status='active').count(),
        'total_found':    Item.objects.filter(item_type='found', status='active').count(),
        'total_resolved': Item.objects.filter(status='resolved').count(),
    }
    steps = [
        (1, '#2563eb', 'fa-paper-plane', 'Post Your Item',
         'Register free and post a lost or found item with description, photo, and location in under 2 minutes.'),
        (2, '#f59e0b', 'fa-search', 'Search & Match',
         'Browse or search by category and location. Find matching items posted by others near you.'),
        (3, '#10b981', 'fa-handshake', 'Connect & Reunite',
         'Contact via WhatsApp or email. Submit a claim, verify ownership, and get your item back safely.'),
    ]
    context['steps'] = steps
    return render(request, 'home.html', context)


# ── REAL-TIME SEARCH API ──────────────────────────────────────
@require_GET
def search_api(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'results': []})
    items = Item.objects.filter(
        Q(title__icontains=q) | Q(description__icontains=q),
        status='active'
    ).order_by('-date_posted')[:6]
    results = []
    for item in items:
        results.append({
            'id':       item.pk,
            'title':    item.title,
            'type':     item.item_type,
            'category': item.get_category_display(),
            'location': item.get_location_display(),
            'icon':     item.get_category_icon(),
            'url':      f'/items/{item.pk}/',
            'image':    item.image.url if item.image else None,
        })
    return JsonResponse({'results': results, 'count': len(results)})


# ── ITEM LIST ─────────────────────────────────────────────────
def item_list_view(request):
    form  = SearchForm(request.GET)
    items = Item.objects.filter(status='active')
    if form.is_valid():
        query     = form.cleaned_data.get('query')
        item_type = form.cleaned_data.get('item_type')
        category  = form.cleaned_data.get('category')
        location  = form.cleaned_data.get('location')
        if query:
            items = items.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if item_type: items = items.filter(item_type=item_type)
        if category:  items = items.filter(category=category)
        if location:  items = items.filter(location=location)
    paginator = Paginator(items, 9)
    page_obj  = paginator.get_page(request.GET.get('page'))
    return render(request, 'items/item_list.html', {
        'form': form, 'page_obj': page_obj, 'total_results': items.count()
    })


# ── ITEM DETAIL ───────────────────────────────────────────────
def item_detail_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.views_count += 1
    item.save(update_fields=['views_count'])

    # Similar items — same category or location, exclude current
    similar = Item.objects.filter(
        status='active',
        item_type=item.item_type
    ).filter(
        Q(category=item.category) | Q(location=item.location)
    ).exclude(pk=pk)[:4]

    user_has_claimed = False
    if request.user.is_authenticated:
        user_has_claimed = item.claims.filter(claimant=request.user).exists()

    # Share URLs
    current_url = request.build_absolute_uri()
    import urllib.parse
    whatsapp_share = f"https://wa.me/?text={urllib.parse.quote(f'Check this {item.item_type} item: {item.title} — {current_url}')}"
    twitter_share  = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(f'{item.item_type.upper()}: {item.title}')}&url={urllib.parse.quote(current_url)}"
    facebook_share = f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(current_url)}"

    # Meta info for template
    location_str = item.get_location_display()
    if item.location_detail:
        location_str += f' — {item.location_detail}'

    meta_info = [
        ('fa-tag',          'Category',   item.get_category_display(),                          '#2563eb'),
        ('fa-map-marker-alt','Location',  location_str,                                          '#ef4444'),
        ('fa-calendar',     'Date',       str(item.date_lost_found),                             '#10b981'),
        ('fa-user',         'Posted By',  item.posted_by.get_full_name() or item.posted_by.username, '#f59e0b'),
        ('fa-clock',        'Posted On',  item.date_posted.strftime('%d %b %Y'),                 '#6b7280'),
    ]

    return render(request, 'items/item_detail.html', {
        'item':             item,
        'user_has_claimed': user_has_claimed,
        'claims_count':     item.claims.count(),
        'whatsapp_link':    item.get_whatsapp_link(),
        'meta_info':        meta_info,
        'similar':          similar,
        'whatsapp_share':   whatsapp_share,
        'twitter_share':    twitter_share,
        'facebook_share':   facebook_share,
        'current_url':      current_url,
    })


# ── POST ITEM ─────────────────────────────────────────────────
@login_required
def post_item_view(request, item_type=None):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.posted_by = request.user
            if not item.contact_email:
                item.contact_email = request.user.email
            item.save()
            try:
                send_mail(
                    subject=f'[LostNFound] Your {item.item_type} item posted',
                    message=(
                        f'Hello {request.user.first_name or request.user.username},\n\n'
                        f'Your {item.item_type} item "{item.title}" has been posted.\n'
                        f'Location: {item.get_location_display()}\n'
                        f'Date: {item.date_lost_found}\n\n'
                        f'— LostNFound Team'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, f'Item "{item.title}" posted successfully!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(initial={'item_type': item_type} if item_type else {})
    return render(request, 'items/post_item.html', {
        'form':       form,
        'item_type':  item_type,
        'page_title': f'Post {"Lost" if item_type == "lost" else "Found" if item_type == "found" else ""} Item',
    })


# ── EDIT ITEM ─────────────────────────────────────────────────
@login_required
def edit_item_view(request, pk):
    item = get_object_or_404(Item, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'items/post_item.html', {
        'form': form, 'item': item, 'page_title': 'Edit Item'
    })


# ── DELETE ITEM ───────────────────────────────────────────────
@login_required
def delete_item_view(request, pk):
    item = get_object_or_404(Item, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        title = item.title
        item.delete()
        messages.success(request, f'Item "{title}" deleted.')
        return redirect('my_items')
    return render(request, 'items/confirm_delete.html', {'item': item})


# ── CLAIM ITEM ────────────────────────────────────────────────
@login_required
def claim_item_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.posted_by == request.user:
        messages.error(request, 'You cannot claim your own item.')
        return redirect('item_detail', pk=pk)
    if item.status != 'active':
        messages.warning(request, 'This item is no longer available.')
        return redirect('item_detail', pk=pk)
    if ClaimRequest.objects.filter(item=item, claimant=request.user).exists():
        messages.warning(request, 'You already submitted a claim.')
        return redirect('item_detail', pk=pk)
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item     = item
            claim.claimant = request.user
            claim.save()
            try:
                send_mail(
                    subject=f'[LostNFound] New Claim for: {item.title}',
                    message=(
                        f'Hello {item.posted_by.first_name or item.posted_by.username},\n\n'
                        f'{request.user.get_full_name() or request.user.username} claimed your item "{item.title}".\n\n'
                        f'Contact: {claim.contact_email} | {claim.contact_phone}\n\n'
                        f'Message: {claim.message}\n\n'
                        f'— LostNFound Team'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[item.posted_by.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, 'Claim submitted! Owner will be notified.')
            return redirect('item_detail', pk=pk)
    else:
        form = ClaimForm(initial={'contact_email': request.user.email})
    return render(request, 'items/claim_form.html', {'form': form, 'item': item})


# ── MY ITEMS ──────────────────────────────────────────────────
@login_required
def my_items_view(request):
    return render(request, 'items/my_items.html', {
        'my_lost':   Item.objects.filter(posted_by=request.user, item_type='lost'),
        'my_found':  Item.objects.filter(posted_by=request.user, item_type='found'),
        'my_claims': ClaimRequest.objects.filter(claimant=request.user).select_related('item'),
    })


# ── MARK RESOLVED ─────────────────────────────────────────────
@login_required
def mark_resolved_view(request, pk):
    item = get_object_or_404(Item, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        item.status = 'resolved'
        item.save()
        messages.success(request, f'"{item.title}" marked as resolved!')
    return redirect('item_detail', pk=pk)


# ── PDF REPORT ────────────────────────────────────────────────
@user_passes_test(lambda u: u.is_staff)
def pdf_report_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="lostnfound_report_{timezone.now().strftime("%Y%m%d")}.pdf"'
    doc    = SimpleDocTemplate(response, pagesize=A4,
                               rightMargin=0.5*inch, leftMargin=0.5*inch,
                               topMargin=0.75*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story  = []
    title_style = ParagraphStyle('t', parent=styles['Title'], fontSize=20,
                                 textColor=colors.HexColor('#1a237e'), spaceAfter=6)
    sub_style   = ParagraphStyle('s', parent=styles['Normal'], fontSize=11,
                                 textColor=colors.grey, spaceAfter=20)
    story.append(Paragraph('Lost & Found Report', title_style))
    story.append(Paragraph(f'Generated: {timezone.now().strftime("%d %B %Y, %I:%M %p")}', sub_style))
    summary_data = [
        ['Total', 'Lost', 'Found', 'Active', 'Resolved'],
        [str(Item.objects.count()),
         str(Item.objects.filter(item_type='lost').count()),
         str(Item.objects.filter(item_type='found').count()),
         str(Item.objects.filter(status='active').count()),
         str(Item.objects.filter(status='resolved').count())],
    ]
    t = Table(summary_data, colWidths=[1.4*inch]*5)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 11),
        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#e8eaf6'), colors.white]),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#9fa8da')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    for itype, color_hex, bg_hex, grid_hex in [
        ('lost',  '#c62828', '#ffebee', '#ef9a9a'),
        ('found', '#1b5e20', '#e8f5e9', '#a5d6a7'),
    ]:
        story.append(Paragraph(
            f'Active {itype.capitalize()} Items',
            ParagraphStyle(f'h{itype}', parent=styles['Heading2'],
                           textColor=colors.HexColor(color_hex), fontSize=14, spaceAfter=8)
        ))
        items = Item.objects.filter(item_type=itype, status='active')
        if items.exists():
            data = [['#', 'Title', 'Category', 'Location', 'Date', 'Posted By']]
            for i, item in enumerate(items, 1):
                data.append([str(i), item.title[:28], item.get_category_display()[:18],
                             item.get_location_display()[:18],
                             item.date_lost_found.strftime('%d/%m/%Y'),
                             item.posted_by.get_full_name() or item.posted_by.username])
            tbl = Table(data, colWidths=[0.3*inch, 1.9*inch, 1.3*inch, 1.3*inch, 0.9*inch, 1.2*inch])
            tbl.setStyle(TableStyle([
                ('BACKGROUND',    (0,0), (-1,0), colors.HexColor(color_hex)),
                ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
                ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE',      (0,0), (-1,-1), 8),
                ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.HexColor(bg_hex), colors.white]),
                ('GRID',          (0,0), (-1,-1), 0.3, colors.HexColor(grid_hex)),
                ('TOPPADDING',    (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(tbl)
        else:
            story.append(Paragraph(f'No active {itype} items.', styles['Normal']))
        story.append(Spacer(1, 18))
    doc.build(story)
    return response

def custom_404(request, exception=None):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)
