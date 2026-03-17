content = open('templates/accounts/profile.html').read()
content = content.replace('height:180px;position:relative;overflow:hidden;', 'height:160px;position:relative;overflow:hidden;')
open('templates/accounts/profile.html', 'w').write(content)
print('Banner height reduced!')
