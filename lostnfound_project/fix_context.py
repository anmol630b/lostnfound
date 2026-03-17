content = open('lostnfound/context_processors.py').read()

old = "def site_info(request):\n    return {"
new = """def site_info(request):
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

    return {"""

new2 = """        'footer_stats':    {'lost': lost, 'found': found, 'resolved': resolved},
        'footer_links':    footer_links,
        'footer_features': footer_features,"""

if old in content:
    content = content.replace(old, new)
    # Add footer data to return dict
    content = content.replace(
        "        'SITE_NAME':",
        new2 + "\n        'SITE_NAME':"
    )
    open('lostnfound/context_processors.py', 'w').write(content)
    print('Context processor updated!')
else:
    print('Pattern not found - check manually')
