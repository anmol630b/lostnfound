content = open('items/views.py').read()

old = "    return render(request, 'items/item_detail.html', {"

new = """    # Meta info for template
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

    return render(request, 'items/item_detail.html', {"""

if old in content:
    content = content.replace(old, new)
    # Add meta_info to context
    content = content.replace(
        "        'whatsapp_link':    item.get_whatsapp_link(),",
        "        'whatsapp_link':    item.get_whatsapp_link(),\n        'meta_info':        meta_info,"
    )
    open('items/views.py', 'w').write(content)
    print('Done!')
else:
    print('Pattern not found')
