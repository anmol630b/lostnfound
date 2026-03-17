/* ══════════════════════════════════════
   DARK MODE
══════════════════════════════════════ */
const toggle = document.getElementById('darkToggle');
const body   = document.body;
const KEY    = 'lnf_dark';

const applyDark = (on) => {
  body.classList.toggle('dark', on);
  if (toggle) toggle.classList.toggle('on', on);
  localStorage.setItem(KEY, on);
};
applyDark(localStorage.getItem(KEY) === 'true');
if (toggle) toggle.addEventListener('click', () => applyDark(!body.classList.contains('dark')));

/* ══════════════════════════════════════
   SMART NAVBAR — hide on scroll down, show on scroll up
══════════════════════════════════════ */
const navbar = document.getElementById('mainNavbar');
let lastScroll = 0;
let ticking = false;

window.addEventListener('scroll', () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      const current = window.scrollY;

      // Add scrolled class after 20px
      if (current > 20) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
        navbar.classList.remove('hidden');
      }

      // Hide on scroll down, show on scroll up
      if (current > 80) {
        if (current > lastScroll + 8) {
          navbar.classList.add('hidden');
        } else if (current < lastScroll - 4) {
          navbar.classList.remove('hidden');
        }
      }

      lastScroll = current <= 0 ? 0 : current;
      ticking = false;
    });
    ticking = true;
  }
});

/* ══════════════════════════════════════
   AUTO DISMISS ALERTS
══════════════════════════════════════ */
document.querySelectorAll('.alert.alert-dismissible').forEach(el => {
  setTimeout(() => {
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease, margin 0.5s ease';
    el.style.opacity = '0';
    el.style.transform = 'translateY(-10px)';
    el.style.marginTop = '-' + el.offsetHeight + 'px';
    setTimeout(() => el.remove(), 500);
  }, 4500);
});

/* ══════════════════════════════════════
   SCROLL ANIMATIONS
══════════════════════════════════════ */
const observer = new IntersectionObserver((entries) => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      setTimeout(() => e.target.classList.add('visible'), i * 90);
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.08 });
document.querySelectorAll('.animate-up').forEach(el => observer.observe(el));

/* ══════════════════════════════════════
   PASSWORD VISIBILITY
══════════════════════════════════════ */
document.querySelectorAll('[data-pwd]').forEach(btn => {
  btn.addEventListener('click', () => {
    const input = document.querySelector(btn.dataset.pwd);
    if (!input) return;
    const isText = input.type === 'text';
    input.type = isText ? 'password' : 'text';
    btn.querySelector('i').className = isText ? 'fas fa-eye' : 'fas fa-eye-slash';
  });
});

/* ══════════════════════════════════════
   PASSWORD STRENGTH
══════════════════════════════════════ */
const pwdInput  = document.querySelector('#id_password1');
const bar       = document.querySelector('.pwd-strength-bar');
const txt       = document.querySelector('.pwd-strength-text');

if (pwdInput && bar) {
  pwdInput.addEventListener('input', () => {
    const v = pwdInput.value;
    let s = 0;
    if (v.length >= 8)          s++;
    if (/[A-Z]/.test(v))        s++;
    if (/[0-9]/.test(v))        s++;
    if (/[^A-Za-z0-9]/.test(v)) s++;
    const c = ['','#ef4444','#f97316','#eab308','#10b981'];
    const l = ['','Weak','Fair','Good','Strong'];
    const p = ['0%','25%','50%','75%','100%'];
    bar.style.width      = p[s];
    bar.style.background = c[s];
    if (txt) txt.textContent = l[s];
  });
}

/* ══════════════════════════════════════
   ANIMATED COUNTERS
══════════════════════════════════════ */
const counterObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const el     = e.target;
      const target = parseInt(el.dataset.count);
      if (isNaN(target)) return;
      let current  = 0;
      const step   = Math.max(1, Math.ceil(target / 50));
      const timer  = setInterval(() => {
        current = Math.min(current + step, target);
        el.textContent = current.toLocaleString();
        if (current >= target) clearInterval(timer);
      }, 30);
      counterObs.unobserve(el);
    }
  });
}, { threshold: 0.5 });
document.querySelectorAll('[data-count]').forEach(el => counterObs.observe(el));

/* ══════════════════════════════════════
   PROFILE — Avatar initials color
══════════════════════════════════════ */
const avatarEl = document.querySelector('.avatar-initials');
if (avatarEl) {
  const colors = [
    '#2563eb','#7c3aed','#db2777','#dc2626',
    '#059669','#d97706','#0891b2','#65a30d'
  ];
  const name  = avatarEl.dataset.name || 'U';
  const index = name.charCodeAt(0) % colors.length;
  avatarEl.style.background = `linear-gradient(135deg, ${colors[index]}, ${colors[(index+2)%colors.length]})`;
}

/* ══════════════════════════════════════
   PROFILE PICTURE PREVIEW
══════════════════════════════════════ */
const picInput   = document.querySelector('#id_profile_picture');
const picPreview = document.querySelector('#profilePicPreview');
if (picInput && picPreview) {
  picInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (ev) => {
        picPreview.src = ev.target.result;
        picPreview.style.display = 'block';
        document.querySelector('.avatar-initials-profile') &&
          (document.querySelector('.avatar-initials-profile').style.display = 'none');
      };
      reader.readAsDataURL(file);
    }
  });
}

/* ══════════════════════════════════════
   ACTIVE NAV LINK
══════════════════════════════════════ */
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-link').forEach(link => {
  const href = link.getAttribute('href');
  if (href && href !== '/' && currentPath.startsWith(href)) {
    link.classList.add('active');
  } else if (href === '/' && currentPath === '/') {
    link.classList.add('active');
  }
});

/* ══════════════════════════════════════
   DROPDOWN POSITION FIX — mobile
══════════════════════════════════════ */
document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
  toggle.addEventListener('click', () => {
    const menu = toggle.nextElementSibling;
    if (!menu || !menu.classList.contains('dropdown-menu')) return;

    if (window.innerWidth < 992) {
      // On mobile, fix top position below navbar
      const navbarH = document.getElementById('mainNavbar').offsetHeight;
      menu.style.top = (navbarH + 8) + 'px';
    }
  });
});

/* Close dropdown when clicking outside */
document.addEventListener('click', (e) => {
  if (!e.target.closest('.dropdown')) {
    document.querySelectorAll('.dropdown-menu.show').forEach(m => {
      m.classList.remove('show');
    });
  }
});

/* ══════════════════════════════════════
   REAL-TIME SEARCH
══════════════════════════════════════ */
function initSearch(inputId, dropId) {
  const input = document.getElementById(inputId);
  const drop  = document.getElementById(dropId);
  if (!input || !drop) return;

  let timer = null;
  let lastQ = '';

  input.addEventListener('input', () => {
    const q = input.value.trim();
    if (q === lastQ) return;
    lastQ = q;
    clearTimeout(timer);

    if (q.length < 2) {
      drop.classList.remove('open');
      drop.innerHTML = '';
      return;
    }

    drop.classList.add('open');
    drop.innerHTML = '<div class="search-loading"><i class="fas fa-circle-notch fa-spin me-2"></i>Searching...</div>';

    timer = setTimeout(async () => {
      try {
        const res  = await fetch(`/items/search/?q=${encodeURIComponent(q)}`);
        const data = await res.json();

        if (!data.results.length) {
          drop.innerHTML = `<div class="search-no-results">
            <i class="fas fa-search-minus mb-2" style="font-size:1.5rem;color:var(--border);display:block;"></i>
            No results for "<strong>${q}</strong>"
          </div>`;
          return;
        }

        drop.innerHTML = data.results.map(item => `
          <a href="${item.url}" class="search-result-item">
            <div class="search-result-icon"
                 style="background:${item.type === 'lost' ? 'rgba(239,68,68,0.1)' : 'rgba(16,185,129,0.1)'}">
              <i class="fas ${item.icon}"
                 style="color:${item.type === 'lost' ? 'var(--lost)' : 'var(--found)'}"></i>
            </div>
            <div style="flex:1;min-width:0;">
              <div class="search-result-title">${item.title}</div>
              <div class="search-result-meta">
                <span style="background:${item.type === 'lost' ? 'rgba(239,68,68,0.1);color:var(--lost)' : 'rgba(16,185,129,0.1);color:var(--found)'};
                             padding:1px 7px;border-radius:10px;font-weight:700;font-size:0.68rem;">
                  ${item.type.toUpperCase()}
                </span>
                · ${item.category} · ${item.location}
              </div>
            </div>
          </a>
        `).join('') + `
          <a href="/items/?query=${encodeURIComponent(q)}"
             style="display:block;padding:10px 16px;text-align:center;font-size:0.8rem;
                    color:var(--blue);font-weight:600;text-decoration:none;
                    border-top:1px solid var(--border);background:var(--surface2);">
            View all results for "${q}" →
          </a>`;
      } catch(e) {
        drop.innerHTML = '<div class="search-no-results">Something went wrong. Try again.</div>';
      }
    }, 320);
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!input.closest('.search-wrap').contains(e.target)) {
      drop.classList.remove('open');
    }
  });

  // Navigate with Enter
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && input.value.trim()) {
      window.location.href = `/items/?query=${encodeURIComponent(input.value.trim())}`;
    }
  });
}

// Init both desktop and mobile search
initSearch('navSearch', 'searchDrop');
initSearch('navSearchMobile', 'searchDropMobile');
