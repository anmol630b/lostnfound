content = open('lostnfound/urls.py').read()

old = 'from django.contrib import admin'
new = 'from django.contrib import admin\nimport lostnfound.admin  # noqa: custom admin branding'

if 'import lostnfound.admin' not in content:
    content = content.replace(old, new)
    open('lostnfound/urls.py', 'w').write(content)
    print('Admin import: added!')
else:
    print('Admin import: already there')
