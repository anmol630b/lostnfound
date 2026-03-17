content = open('accounts/views.py').read()

old = "    return render(request, 'accounts/register.html', {'form': form})"
new = """    benefits = [
        'Post unlimited lost & found items',
        'Upload photos of items',
        'WhatsApp & email contact',
        'Submit ownership claims',
        'Get notified when someone claims your item',
    ]
    return render(request, 'accounts/register.html', {'form': form, 'benefits': benefits})"""

if old in content:
    content = content.replace(old, new)
    open('accounts/views.py', 'w').write(content)
    print('Done!')
else:
    print('Not found')
