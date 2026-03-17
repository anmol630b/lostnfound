content = open('lostnfound/settings.py').read()
content = content.replace('DEBUG = True', 'DEBUG = False')
# ALLOWED_HOSTS bhi fix karo
if "ALLOWED_HOSTS = []" in content:
    content = content.replace("ALLOWED_HOSTS = []", "ALLOWED_HOSTS = ['127.0.0.1', 'localhost']")
open('lostnfound/settings.py', 'w').write(content)
print('Done!')
