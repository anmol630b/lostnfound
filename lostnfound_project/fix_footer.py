content = open('templates/base.html').read()

new_footer = '''  <!-- FOOTER -->
  <footer style="background:#0a0f1e;color:rgba(255,255,255,0.5);margin-top:auto;">

    <!-- Main footer -->
    <div class="container" style="padding:48px 0 32px;">
      <div class="row g-4">

        <!-- Brand -->
        <div class="col-12 col-md-4">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
            <div style="width:36px;height:36px;background:linear-gradient(135deg,#2563eb,#1d4ed8);border-radius:10px;display:flex;align-items:center;justify-content:center;">
              <i class="fas fa-search-location" style="color:white;font-size:0.85rem;"></i>
            </div>
            <span style="font-family:'Sora',sans-serif;font-weight:800;font-size:1.1rem;color:white;">{{ SITE_NAME }}</span>
          </div>
          <p style="font-size:0.85rem;line-height:1.8;color:rgba(255,255,255,0.4);max-width:260px;margin-bottom:20px;">
            {{ SITE_TAGLINE }}
          </p>
          <div style="display:flex;gap:10px;">
            <div style="width:34px;height:34px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);border-radius:9px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:all 0.2s;" onmouseover="this.style.background='rgba(37,99,235,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.06)'">
              <i class="fab fa-github" style="color:rgba(255,255,255,0.6);font-size:0.85rem;"></i>
            </div>
            <div style="width:34px;height:34px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);border-radius:9px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:all 0.2s;" onmouseover="this.style.background='rgba(37,99,235,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.06)'">
              <i class="fab fa-twitter" style="color:rgba(255,255,255,0.6);font-size:0.85rem;"></i>
            </div>
          </div>
        </div>

        <!-- Quick Links -->
        <div class="col-6 col-md-2">
          <div style="font-size:0.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:16px;">Navigate</div>
          {% for label, url in footer_links %}
          <a href="{{ url }}" style="display:block;font-size:0.85rem;color:rgba(255,255,255,0.45);text-decoration:none;margin-bottom:10px;transition:color 0.2s;" onmouseover="this.style.color='white'" onmouseout="this.style.color='rgba(255,255,255,0.45)'">
            {{ label }}
          </a>
          {% endfor %}
        </div>

        <!-- Features -->
        <div class="col-6 col-md-3">
          <div style="font-size:0.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:16px;">Features</div>
          {% for feat in footer_features %}
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
            <i class="fas fa-check-circle" style="color:#34d399;font-size:0.7rem;flex-shrink:0;"></i>
            <span style="font-size:0.85rem;color:rgba(255,255,255,0.45);">{{ feat }}</span>
          </div>
          {% endfor %}
        </div>

        <!-- Stats -->
        <div class="col-12 col-md-3">
          <div style="font-size:0.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:16px;">Live Stats</div>
          <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:16px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:14px;padding-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.07);">
              <div style="text-align:center;">
                <div style="font-family:'Sora',sans-serif;font-size:1.4rem;font-weight:800;color:white;">{{ footer_stats.lost }}</div>
                <div style="font-size:0.65rem;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.5px;margin-top:2px;">Lost</div>
              </div>
              <div style="text-align:center;">
                <div style="font-family:'Sora',sans-serif;font-size:1.4rem;font-weight:800;color:white;">{{ footer_stats.found }}</div>
                <div style="font-size:0.65rem;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.5px;margin-top:2px;">Found</div>
              </div>
              <div style="text-align:center;">
                <div style="font-family:'Sora',sans-serif;font-size:1.4rem;font-weight:800;color:#34d399;">{{ footer_stats.resolved }}</div>
                <div style="font-size:0.65rem;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.5px;margin-top:2px;">Reunited</div>
              </div>
            </div>
            <div style="font-size:0.75rem;color:rgba(255,255,255,0.3);text-align:center;">
              <i class="fas fa-circle" style="color:#34d399;font-size:0.5rem;margin-right:5px;animation:pulse 2s infinite;"></i>
              Updated in real-time
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Bottom bar -->
    <div style="border-top:1px solid rgba(255,255,255,0.06);">
      <div class="container" style="padding:16px 0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;">
        <div style="font-size:0.78rem;color:rgba(255,255,255,0.25);">
          © 2025 {{ SITE_NAME }}. Built with <i class="fas fa-heart" style="color:#ef4444;font-size:0.7rem;"></i> using Django & Bootstrap 5.
        </div>
        <div style="font-size:0.75rem;color:rgba(255,255,255,0.2);">
          Free for everyone · No ads · Open community
        </div>
      </div>
    </div>

  </footer>'''

# Find and replace old footer
import re
# Remove old footer
content = re.sub(r'<!-- FOOTER -->.*?</footer>', '', content, flags=re.DOTALL)
# Add before </body>
content = content.replace('</body>', new_footer + '\n</body>')
open('templates/base.html', 'w').write(content)
print('Footer updated!')
