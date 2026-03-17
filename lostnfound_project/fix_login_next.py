content = open('templates/accounts/login.html').read()

old = "    <div style=\"font-size:0.72rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--blue);margin-bottom:8px;\">Welcome back</div>"

new = """    {% if request.GET.next %}
    <div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.2);border-radius:12px;padding:12px 16px;margin-bottom:20px;display:flex;align-items:center;gap:12px;">
      <div style="width:36px;height:36px;background:rgba(245,158,11,0.15);border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
        <i class="fas fa-lock" style="color:var(--gold);font-size:0.9rem;"></i>
      </div>
      <div>
        <div style="font-size:0.82rem;font-weight:700;color:var(--text);">Sign in required</div>
        <div style="font-size:0.75rem;color:var(--text3);margin-top:2px;">Please login to access this page.</div>
      </div>
    </div>
    {% endif %}
    <div style="font-size:0.72rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--blue);margin-bottom:8px;">Welcome back</div>"""

if old in content:
    content = content.replace(old, new)
    open('templates/accounts/login.html', 'w').write(content)
    print('Done!')
else:
    print('Not found')
