import os

# Create custom admin template to inject CSS
os.makedirs('templates/admin', exist_ok=True)

content = '''{% extends "admin/base.html" %}
{% load static %}

{% block extrahead %}
{{ block.super }}
<link rel="stylesheet" href="{% static 'css/admin_custom.css' %}">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
{% endblock %}
'''

open('templates/admin/base_site.html', 'w').write(content)
print('Admin base_site.html created!')
