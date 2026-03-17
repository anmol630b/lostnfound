content = open('accounts/views.py').read()

old = "    return render(request, 'accounts/login.html', {'form': form})"
new = """    features = [
        ('fa-bolt',      '#fbbf24', 'Post items in under 2 minutes'),
        ('fa-whatsapp',  '#25d366', 'Connect instantly via WhatsApp'),
        ('fa-search',    '#60a5fa', 'Search by category & location'),
        ('fa-globe',     '#a78bfa', 'Open to everyone — 100% free'),
    ]
    return render(request, 'accounts/login.html', {'form': form, 'features': features})"""

if old in content:
    content = content.replace(old, new)
    open('accounts/views.py', 'w').write(content)
    print('Done!')
else:
    print('Not found')
