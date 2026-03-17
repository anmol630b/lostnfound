content = open('templates/base.html').read()

# Add desktop search before dark toggle
old = '        <!-- Dark toggle (desktop) -->\n        <button id="darkToggle" class="d-none d-lg-block" title="Toggle dark mode"></button>'
new = '''        <!-- Desktop Search -->
        <div class="search-wrap d-none d-lg-flex align-items-center">
          <span class="search-icon"><i class="fas fa-search"></i></span>
          <input type="text" id="navSearch" placeholder="Search items..." autocomplete="off">
          <div id="searchDrop" class="search-dropdown"></div>
        </div>
        <!-- Dark toggle (desktop) -->
        <button id="darkToggle" class="d-none d-lg-block" title="Toggle dark mode"></button>'''

if old in content:
    content = content.replace(old, new)
    print('Desktop search: added!')
else:
    print('Desktop search: already there or not found')

open('templates/base.html', 'w').write(content)
print('Done!')
