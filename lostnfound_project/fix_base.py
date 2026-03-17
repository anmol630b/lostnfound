content = open('templates/base.html').read()

old = '    <!-- Mobile toggle -->\n    <div class="d-flex align-items-center gap-2 d-lg-none">\n      <button id="darkToggle" title="Toggle dark mode"></button>\n      <button class="navbar-toggler border-0 p-1" type="button" data-bs-toggle="collapse" data-bs-target="#nav">\n        <i class="fas fa-bars" style="color:var(--text2);font-size:1.1rem;"></i>\n      </button>\n    </div>'

new = '''    <!-- Mobile toggle -->
    <div class="d-flex align-items-center gap-2 d-lg-none">
      <button id="darkToggle" title="Toggle dark mode"></button>
      <button class="navbar-toggler border-0 p-1" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
        <i class="fas fa-bars" style="color:var(--text2);font-size:1.1rem;"></i>
      </button>
    </div>'''

if old in content:
    content = content.replace(old, new)
    print('Mobile toggle: OK')
else:
    print('Mobile toggle: not found, skipping')

old2 = '      <div class="d-flex align-items-center gap-3">\n        <!-- Dark toggle (desktop) -->\n        <button id="darkToggle" class="d-none d-lg-block" title="Toggle dark mode"></button>'

new2 = '''      <div class="d-flex align-items-center gap-3">
        <!-- Dark toggle (desktop) -->
        <button id="darkToggle" class="d-none d-lg-block" title="Toggle dark mode"></button>'''

if old2 in content:
    content = content.replace(old2, new2)
    print('Desktop toggle: OK')
else:
    print('Desktop toggle: not found, skipping')

open('templates/base.html', 'w').write(content)
print('Done!')
