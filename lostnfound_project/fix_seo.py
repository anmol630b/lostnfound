content = open('templates/base.html').read()

old = '  <meta name="description" content="{{ SITE_DESCRIPTION }}">'
new = '''  <meta name="description" content="{{ SITE_DESCRIPTION }}">
  <meta name="keywords" content="lost and found, lost items, found items, help, community">
  <meta name="author" content="{{ SITE_NAME }}">
  <meta property="og:title" content="{% block og_title %}{{ SITE_NAME }} — {{ SITE_TAGLINE }}{% endblock %}">
  <meta property="og:description" content="{% block og_desc %}{{ SITE_DESCRIPTION }}{% endblock %}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{{ SITE_NAME }}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{{ SITE_NAME }}">
  <meta name="twitter:description" content="{{ SITE_DESCRIPTION }}">
  <meta name="theme-color" content="#2563eb">'''

if old in content:
    content = content.replace(old, new)
    print('SEO tags: added!')
else:
    print('SEO: already there or not found')

open('templates/base.html', 'w').write(content)
print('Done!')
