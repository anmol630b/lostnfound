content = open('templates/accounts/profile.html').read()

old = '  <!-- Avatar + Name -->\n  <div style="display:flex;align-items:flex-end;gap:20px;margin-top:-50px;margin-bottom:24px;flex-wrap:wrap;">'

new = '  <!-- Avatar + Name -->\n  <div style="display:flex;align-items:flex-end;gap:20px;margin-top:-45px;padding-top:0;margin-bottom:24px;flex-wrap:wrap;overflow:visible;">'

if old in content:
    content = content.replace(old, new)
    print('Fixed!')
else:
    # Try alternate fix
    content = content.replace('margin-top:-50px;margin-bottom:24px;flex-wrap:wrap;">', 'margin-top:-40px;margin-bottom:24px;flex-wrap:wrap;overflow:visible;">')
    print('Alternate fix applied!')

open('templates/accounts/profile.html', 'w').write(content)
