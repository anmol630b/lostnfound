from django.conf import settings


def site_info(request):
    try:
        from items.models import Item
        lost    = Item.objects.filter(item_type='lost',  status='active').count()
        found   = Item.objects.filter(item_type='found', status='active').count()
        resolved= Item.objects.filter(status='resolved').count()
    except:
        lost = found = resolved = 0

    from django.urls import reverse
    footer_links = [
        ('Home',         '/'),
        ('Browse Items', '/items/'),
        ('Post Lost',    '/items/post/lost/'),
        ('Post Found',   '/items/post/found/'),
        ('My Dashboard', '/items/my-items/'),
        ('Profile',      '/accounts/profile/'),
    ]
    footer_features = [
        'Real-time search',
        'WhatsApp contact',
        'Claim system',
        'Email notifications',
        'Dark mode',
        '100% free',
    ]

    return {
        'footer_stats':    {'lost': lost, 'found': found, 'resolved': resolved},
        'footer_links':    footer_links,
        'footer_features': footer_features,
        'SITE_NAME':        getattr(settings, 'SITE_NAME', 'LostNFound'),
        'SITE_TAGLINE':     getattr(settings, 'SITE_TAGLINE', 'Find What You Lost.'),
        'SITE_DESCRIPTION': getattr(settings, 'SITE_DESCRIPTION', ''),
    }
