content = open('items/views.py').read()

old = "    return render(request, 'home.html', context)"

new = """    steps = [
        (1, '#2563eb', 'fa-paper-plane', 'Post Your Item',
         'Register free and post a lost or found item with description, photo, and location in under 2 minutes.'),
        (2, '#f59e0b', 'fa-search', 'Search & Match',
         'Browse or search by category and location. Find matching items posted by others near you.'),
        (3, '#10b981', 'fa-handshake', 'Connect & Reunite',
         'Contact via WhatsApp or email. Submit a claim, verify ownership, and get your item back safely.'),
    ]
    context['steps'] = steps
    return render(request, 'home.html', context)"""

if "    return render(request, 'home.html', context)" in content:
    content = content.replace(old, new)
    open('items/views.py', 'w').write(content)
    print('Done!')
else:
    print('Not found')
