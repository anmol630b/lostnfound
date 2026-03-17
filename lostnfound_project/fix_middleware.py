content = open('lostnfound/settings.py').read()

old = "    'django.middleware.clickjacking.XFrameOptionsMiddleware',"
new = "    'django.middleware.clickjacking.XFrameOptionsMiddleware',\n    'items.middleware.LoginRequiredMiddleware',"

if 'LoginRequiredMiddleware' not in content:
    content = content.replace(old, new)
    open('lostnfound/settings.py', 'w').write(content)
    print('Middleware added!')
else:
    print('Already there!')
