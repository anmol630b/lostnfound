content = open('templates/base.html').read()

# Remove admin panel and PDF report links from navbar dropdown
old = '''            {% if user.is_staff %}
            <li><hr style="border-color:var(--border);margin:4px 0;"></li>
            <li><a class="dropdown-item rounded-2 py-2" href="/admin/" style="color:var(--blue);font-size:0.875rem;font-weight:600;"><i class="fas fa-shield-alt me-2" style="color:var(--blue);width:16px;"></i>Admin Panel</a></li>
            <li><a class="dropdown-item rounded-2 py-2" href="{% url 'pdf_report' %}" style="color:var(--lost);font-size:0.875rem;font-weight:600;"><i class="fas fa-file-pdf me-2" style="width:16px;"></i>Download Report</a></li>
            {% endif %}'''

new = ''

if old in content:
    content = content.replace(old, new)
    print('Admin link removed from navbar dropdown!')
else:
    print('Pattern not found - checking...')
    # Try to find and show what is there
    if 'is_staff' in content:
        print('is_staff found in template')
    if 'Admin Panel' in content:
        print('Admin Panel text found')

open('templates/base.html', 'w').write(content)
