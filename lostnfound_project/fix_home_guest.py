content = open('templates/home.html').read()

# Update browse button for guests
old = '          <a href="{% url \'item_list\' %}" class="btn btn-outline-white">\n            <i class="fas fa-search me-2"></i>Browse Items\n          </a>'

new = """          {% if user.is_authenticated %}
          <a href="{% url 'item_list' %}" class="btn btn-outline-white">
            <i class="fas fa-search me-2"></i>Browse Items
          </a>
          {% else %}
          <a href="{% url 'register' %}" class="btn btn-outline-white">
            <i class="fas fa-search me-2"></i>Browse Items
          </a>
          {% endif %}"""

if old in content:
    content = content.replace(old, new)
    open('templates/home.html', 'w').write(content)
    print('Done!')
else:
    print('Check manually')
