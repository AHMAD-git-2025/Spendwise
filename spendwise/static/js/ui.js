/**
 * SpendWise Unified UI Engine
 * Shared Icon Sprite, Single Global Theme System, Notifications, Modals & Navigation
 */
(function() {
  'use strict';

  // --- 1. Comprehensive Icon Sprite ---
  const SPRITE = `<svg xmlns="http://www.w3.org/2000/svg" style="display:none">
<symbol id="i-home" viewBox="0 0 24 24"><path d="M3 11l9-8 9 8"/><path d="M5 10v10h5v-6h4v6h5V10"/></symbol>
<symbol id="i-wallet" viewBox="0 0 24 24"><path d="M20 7H5a2 2 0 010-4h13v4"/><path d="M3 5v14a2 2 0 002 2h15V7"/><circle cx="16" cy="14" r="1"/></symbol>
<symbol id="i-receipt" viewBox="0 0 24 24"><path d="M5 3h14v18l-3-2-2 2-2-2-2 2-2-2-3 2z"/><path d="M9 8h6M9 12h6"/></symbol>
<symbol id="i-calendar" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="17" rx="2"/><path d="M8 2v4M16 2v4M3 10h18"/></symbol>
<symbol id="i-trend" viewBox="0 0 24 24"><path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/></symbol>
<symbol id="i-chart" viewBox="0 0 24 24"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></symbol>
<symbol id="i-target" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></symbol>
<symbol id="i-flag" viewBox="0 0 24 24"><path d="M5 22V4M5 4h13l-2 4 2 4H5"/></symbol>
<symbol id="i-settings" viewBox="0 0 24 24"><path d="M4 6h10M18 6h2M4 12h2M10 12h10M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="8" cy="12" r="2"/><circle cx="18" cy="18" r="2"/></symbol>
<symbol id="i-logout" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/></symbol>
<symbol id="i-moon" viewBox="0 0 24 24"><path d="M21 13A9 9 0 1111 3a7 7 0 0010 10z"/></symbol>
<symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></symbol>
<symbol id="i-bulb" viewBox="0 0 24 24"><path d="M9 18h6M10 21h4M12 3a6 6 0 00-4 10c1 1 1 2 1 3h6c0-1 0-2 1-3a6 6 0 00-4-10z"/></symbol>
<symbol id="i-alert" viewBox="0 0 24 24"><path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18h0"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path d="M5 12l5 5 9-10"/></symbol>
<symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></symbol>
<symbol id="i-lock" viewBox="0 0 24 24"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 018 0v4"/></symbol>
<symbol id="i-bell" viewBox="0 0 24 24"><path d="M6 8a6 6 0 0112 0c0 7 3 8 3 8H3s3-1 3-8M10 21h4"/></symbol>
<symbol id="i-user" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0116 0"/></symbol>
<symbol id="i-users" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.5"/><path d="M2 21a7 7 0 0114 0M16 4.5a3.5 3.5 0 010 7M18 21a7 7 0 00-3-5.7"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s7-6 7-12a7 7 0 10-14 0c0 6 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/></symbol>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 006 6L16 13l5 2v4a2 2 0 01-2 2A16 16 0 013 5a2 2 0 012-2z"/></symbol>
<symbol id="i-camera" viewBox="0 0 24 24"><path d="M3 8h4l2-3h6l2 3h4v12H3z"/><circle cx="12" cy="13" r="4"/></symbol>
<symbol id="i-plane" viewBox="0 0 24 24"><path d="M22 3L2 11l7 3 3 7z"/><path d="M22 3L9 14"/></symbol>
<symbol id="i-heart" viewBox="0 0 24 24"><path d="M12 21s-9-6-9-12a5 5 0 019-3 5 5 0 019 3c0 6-9 12-9 12z"/></symbol>
<symbol id="i-utensils" viewBox="0 0 24 24"><path d="M6 3v8a2 2 0 004 0V3M8 3v18M18 21V3c-3 1-4 5-4 9h4"/></symbol>
<symbol id="i-film" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16M17 4v16M3 12h18"/></symbol>
<symbol id="i-book" viewBox="0 0 24 24"><path d="M3 4h7a2 2 0 012 2v14a2 2 0 00-2-2H3zM21 4h-7a2 2 0 00-2 2v14a2 2 0 012-2h7z"/></symbol>
<symbol id="i-car" viewBox="0 0 24 24"><path d="M3 16v-4l2-5h14l2 5v4zM3 16v2M21 16v2M3 12h18"/></symbol>
<symbol id="i-bag" viewBox="0 0 24 24"><path d="M5 8h14l1 13H4z"/><path d="M9 8V6a3 3 0 016 0v2"/></symbol>
<symbol id="i-calc" viewBox="0 0 24 24"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h1M12 12h1M8 16h1M12 16h1"/></symbol>
<symbol id="i-upload" viewBox="0 0 24 24"><path d="M12 16V4M7 9l5-5 5 5M4 20h16"/></symbol>
<symbol id="i-download" viewBox="0 0 24 24"><path d="M12 4v12M7 11l5 5 5-5M4 20h16"/></symbol>
<symbol id="i-grad" viewBox="0 0 24 24"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/></symbol>
<symbol id="i-bank" viewBox="0 0 24 24"><path d="M3 10l9-6 9 6zM5 10v8M10 10v8M14 10v8M19 10v8M3 21h18"/></symbol>
<symbol id="i-laptop" viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="11" rx="1"/><path d="M2 20h20"/></symbol>
<symbol id="i-mobile" viewBox="0 0 24 24"><rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/></symbol>
<symbol id="i-life" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5"/><path d="M5.6 5.6l3.9 3.9M14.5 14.5l3.9 3.9M18.4 5.6l-3.9 3.9M9.5 14.5l-3.9 3.9"/></symbol>
<symbol id="i-globe" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/></symbol>
<symbol id="i-zap" viewBox="0 0 24 24"><path d="M13 2L4 14h7l-1 8 9-12h-7z"/></symbol>
<symbol id="i-link" viewBox="0 0 24 24"><path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1"/></symbol>
<symbol id="i-palette" viewBox="0 0 24 24"><path d="M12 3a9 9 0 100 18c1.5 0 2-1 1.5-2s0-2 1.5-2h2a3 3 0 003-3c0-6-4-11-8-11z"/><circle cx="8" cy="11" r="1"/><circle cx="12" cy="7.5" r="1"/><circle cx="16" cy="11" r="1"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></symbol>
<symbol id="i-x" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></symbol>
<symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></symbol>
<symbol id="i-printer" viewBox="0 0 24 24"><path d="M7 9V3h10v6M7 17H4v-7h16v7h-3"/><rect x="7" y="14" width="10" height="7"/></symbol>
<symbol id="i-down-right" viewBox="0 0 24 24"><path d="M7 7l10 10M17 8v9H8"/></symbol>
<symbol id="i-up-right" viewBox="0 0 24 24"><path d="M7 17L17 7M8 7h9v9"/></symbol>
<symbol id="i-trophy" viewBox="0 0 24 24"><path d="M8 4h8v6a4 4 0 01-8 0zM8 6H4v2a3 3 0 003 3M16 6h4v2a3 3 0 01-3 3M12 14v4M8 21h8"/></symbol>
<symbol id="i-brain" viewBox="0 0 24 24"><path d="M9 4a3 3 0 00-3 3 3 3 0 00-2 5 3 3 0 002 5 3 3 0 006 1V4a3 3 0 00-3 0zM15 4a3 3 0 013 3 3 3 0 012 5 3 3 0 01-2 5 3 3 0 01-6 1V4"/></symbol>
<symbol id="i-hourglass" viewBox="0 0 24 24"><path d="M6 3h12M6 21h12M7 3c0 5 5 6 5 9s-5 4-5 9M17 3c0 5-5 6-5 9s5 4 5 9"/></symbol>
<symbol id="i-card" viewBox="0 0 24 24"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h4"/></symbol>
<symbol id="i-compass" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/></symbol>
<symbol id="i-layout" viewBox="0 0 24 24"><rect x="3" y="3" width="8" height="10" rx="2"/><rect x="13" y="3" width="8" height="6" rx="2"/><rect x="13" y="11" width="8" height="10" rx="2"/><rect x="3" y="15" width="8" height="6" rx="2"/></symbol>
<symbol id="i-trash" viewBox="0 0 24 24"><path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2M10 11v6M14 11v6"/></symbol>
<symbol id="i-edit" viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></symbol>
</svg>`;

  // --- 2. Single Global Theme System ---
  const STORAGE_KEY = 'spendwiseTheme';

  function getSavedTheme() {
    try {
      let v = localStorage.getItem(STORAGE_KEY) || localStorage.getItem('spendwise_theme');
      if (!v && localStorage.getItem('sw-dark') === '1') v = 'dark';
      if (v === 'dark' || v === 'light') return v;
    } catch (_) {}
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function updateThemeToggles(isDark) {
    // When isDark is true, show Sun icon so user knows clicking will switch to light
    const iconId = isDark ? 'i-sun' : 'i-moon';
    const label = isDark ? 'Switch to light mode' : 'Switch to dark mode';
    const targets = document.querySelectorAll('#themeToggle, #theme, [data-theme-toggle]');

    targets.forEach(el => {
      el.innerHTML = `<svg class="ic" aria-hidden="true"><use href="#${iconId}" /></svg>`;
      el.setAttribute('aria-label', label);
      el.setAttribute('title', label);
      el.setAttribute('aria-pressed', isDark ? 'true' : 'false');
    });

    // Synchronize switches (settings.html uses darkThemeSwitch, other pages may use darkMode)
    const switches = document.querySelectorAll('#darkMode, #darkThemeSwitch');
    switches.forEach(sw => {
      if (sw && sw.checked !== isDark) {
        sw.checked = isDark;
      }
    });
  }

  function applyTheme(theme, persist = false) {
    const isDark = (theme === 'dark');
    const activeTheme = isDark ? 'dark' : 'light';

    document.documentElement.classList.toggle('dark', isDark);
    document.documentElement.setAttribute('data-theme', activeTheme);
    document.documentElement.style.colorScheme = activeTheme;

    if (document.body) {
      document.body.classList.toggle('dark', isDark);
      document.body.setAttribute('data-theme', activeTheme);
      document.body.style.colorScheme = activeTheme;
    }

    if (persist) {
      try {
        localStorage.setItem(STORAGE_KEY, activeTheme);
        localStorage.setItem('spendwise_theme', activeTheme);
        localStorage.setItem('sw-dark', isDark ? '1' : '0');
      } catch (_) {}
    }

    updateThemeToggles(isDark);

    // Notify listeners (e.g. Chart.js redraws on Dashboard & Reports)
    window.dispatchEvent(new CustomEvent('spendwise-theme-change', {
      detail: { theme: activeTheme, isDark }
    }));
  }

  function toggleTheme(e) {
    const isDark = document.documentElement.classList.contains('dark') ||
                   document.documentElement.getAttribute('data-theme') === 'dark';
    const nextTheme = isDark ? 'light' : 'dark';

    // Fallback if View Transitions API is not supported or user prefers reduced motion
    if (!document.startViewTransition || (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) {
      applyTheme(nextTheme, true);
      return;
    }

    // Determine circular expansion origin based on click coordinates or target button
    let x = window.innerWidth / 2;
    let y = 40;
    if (e && e.clientX !== undefined && e.clientX > 0) {
      x = e.clientX;
      y = e.clientY;
    } else {
      const btn = document.querySelector('#themeToggle, #theme, [data-theme-toggle]');
      if (btn) {
        const rect = btn.getBoundingClientRect();
        x = rect.left + rect.width / 2;
        y = rect.top + rect.height / 2;
      }
    }

    const endRadius = Math.hypot(
      Math.max(x, window.innerWidth - x),
      Math.max(y, window.innerHeight - y)
    );

    document.documentElement.setAttribute('data-theme-animating', 'true');
    const transition = document.startViewTransition(() => {
      applyTheme(nextTheme, true);
    });

    transition.ready.then(() => {
      const clipPath = [
        `circle(0px at ${x}px ${y}px)`,
        `circle(${endRadius}px at ${x}px ${y}px)`
      ];
      const anim = document.documentElement.animate(
        {
          clipPath: clipPath
        },
        {
          duration: 380,
          easing: 'cubic-bezier(0.2, 0.8, 0.2, 1)',
          pseudoElement: '::view-transition-new(root)'
        }
      );
      anim.finished.finally(() => {
        document.documentElement.removeAttribute('data-theme-animating');
      });
    }).catch(() => {
      document.documentElement.removeAttribute('data-theme-animating');
    });
  }

  // Expose global SpendWise Theme API
  window.SpendWiseTheme = {
    get: getSavedTheme,
    apply: applyTheme,
    set: function(theme) {
      applyTheme(theme, true);
    },
    toggle: toggleTheme,
    updateIcons: updateThemeToggles
  };

  // Immediate early initialization to prevent theme flashing
  (function initEarlyTheme() {
    const saved = getSavedTheme();
    const isDark = (saved === 'dark');
    document.documentElement.classList.toggle('dark', isDark);
    document.documentElement.setAttribute('data-theme', saved);
    document.documentElement.style.colorScheme = saved;
    if (document.body) {
      document.body.classList.toggle('dark', isDark);
      document.body.setAttribute('data-theme', saved);
      document.body.style.colorScheme = saved;
    }
  })();

  // --- 3. Unified Toast Notification API ---
  function ensureToastContainer() {
    let container = document.getElementById('spendwiseToastContainer');
    if (!container) {
      container = document.createElement('div');
      container.id = 'spendwiseToastContainer';
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    return container;
  }

  window.showToast = function(message, type = 'success', duration = 3200) {
    if (typeof type === 'boolean') {
      type = type ? 'error' : 'success';
    }

    const container = ensureToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    let iconSymbol = 'i-check';
    if (type === 'error') iconSymbol = 'i-alert';
    else if (type === 'warning') iconSymbol = 'i-hourglass';
    else if (type === 'info') iconSymbol = 'i-bulb';

    toast.innerHTML = `<svg class="ic"><use href="#${iconSymbol}" /></svg><span>${escapeHTML(message)}</span>`;
    container.appendChild(toast);

    requestAnimationFrame(() => {
      toast.classList.add('show');
    });

    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 320);
    }, duration);

    // Also sync with legacy inline #toast elements if present
    const legacyToast = document.getElementById('toast');
    if (legacyToast && legacyToast !== toast) {
      legacyToast.textContent = message;
      legacyToast.className = `toast show ${type}`;
      setTimeout(() => legacyToast.classList.remove('show'), duration);
    }
  };

  // --- 4. Confirmation Dialog Modal API ---
  window.spendwiseConfirm = function({
    title = 'Confirm Action',
    message = 'Are you sure you want to proceed?',
    confirmText = 'Confirm',
    cancelText = 'Cancel',
    danger = false
  } = {}) {
    return new Promise(resolve => {
      const backdrop = document.createElement('div');
      backdrop.className = 'sw-modal-backdrop';
      backdrop.innerHTML = `
        <div class="sw-modal-content" role="dialog" aria-modal="true" aria-labelledby="swModalTitle">
          <h3 id="swModalTitle" style="margin:0 0 10px;font-size:18px;">${escapeHTML(title)}</h3>
          <p style="margin:0 0 22px;color:var(--muted);font-size:14px;line-height:1.5;">${escapeHTML(message)}</p>
          <div style="display:flex;justify-content:flex-end;gap:10px;">
            <button type="button" class="btn btn-secondary" id="swModalCancel" style="padding:10px 18px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--ink);font-weight:600;">
              ${escapeHTML(cancelText)}
            </button>
            <button type="button" class="btn ${danger ? 'btn-danger' : 'btn-teal'}" id="swModalConfirm" style="padding:10px 18px;border-radius:10px;border:0;color:#fff;background:${danger ? 'var(--red)' : 'linear-gradient(180deg,#17c6b3,var(--teal-d))'};font-weight:600;">
              ${escapeHTML(confirmText)}
            </button>
          </div>
        </div>
      `;

      document.body.appendChild(backdrop);
      requestAnimationFrame(() => backdrop.classList.add('open'));

      const close = result => {
        backdrop.classList.remove('open');
        setTimeout(() => backdrop.remove(), 250);
        resolve(result);
      };

      backdrop.querySelector('#swModalCancel').onclick = () => close(false);
      backdrop.querySelector('#swModalConfirm').onclick = () => close(true);
      backdrop.onclick = e => {
        if (e.target === backdrop) close(false);
      };

      const keyHandler = e => {
        if (e.key === 'Escape') {
          document.removeEventListener('keydown', keyHandler);
          close(false);
        }
      };
      document.addEventListener('keydown', keyHandler);
    });
  };

  function escapeHTML(str) {
    return String(str ?? '').replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  // --- 5. Main Boot & Wiring ---
  function bootSpendWiseUI() {
    // Inject sprite if not present
    if (!document.getElementById('spendwise-icons')) {
      const div = document.createElement('div');
      div.id = 'spendwise-icons';
      div.style.display = 'none';
      div.innerHTML = SPRITE;
      document.body.insertAdjacentElement('afterbegin', div);
    }

    // Process [data-i] icons
    document.querySelectorAll('[data-i]').forEach(el => {
      const iconName = el.dataset.i;
      el.innerHTML = `<svg class="ic"><use href="#i-${iconName}" /></svg>` + el.innerHTML;
      el.removeAttribute('data-i');
    });

    // Apply active theme to document and body
    const activeTheme = getSavedTheme();
    applyTheme(activeTheme, false);

    // Bind Theme Toggle Buttons
    document.addEventListener('click', e => {
      const btn = e.target.closest('#themeToggle, #theme, [data-theme-toggle]');
      if (btn) {
        e.preventDefault();
        toggleTheme(e);
      }
    });

    // Bind Dark Theme Switches if present in settings or preferences
    const dmSwitches = document.querySelectorAll('#darkMode, #darkThemeSwitch');
    dmSwitches.forEach(dmSwitch => {
      dmSwitch.checked = (getSavedTheme() === 'dark');
      dmSwitch.addEventListener('change', () => {
        applyTheme(dmSwitch.checked ? 'dark' : 'light', true);
      });
    });

    // Listen to OS system preference changes (if user hasn't explicitly set preference)
    try {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem(STORAGE_KEY) && !localStorage.getItem('spendwise_theme')) {
          applyTheme(e.matches ? 'dark' : 'light', false);
        }
      });
    } catch (_) {}

    // Compact Layout Switch
    const clSwitch = document.getElementById('compactLayout');
    if (clSwitch) {
      clSwitch.addEventListener('change', () => {
        document.body.classList.toggle('compact-mode', clSwitch.checked);
      });
    }

    // --- Mobile Sidebar Navigation Drawer & Scrim ---
    function ensureScrim() {
      let scrim = document.getElementById('scrim') || document.querySelector('.scrim');
      if (!scrim) {
        scrim = document.createElement('div');
        scrim.className = 'scrim';
        scrim.id = 'scrim';
        document.body.appendChild(scrim);
      }
      return scrim;
    }

    const scrim = ensureScrim();
    const toggleMenu = open => {
      const willOpen = typeof open === 'boolean' ? open : !document.body.classList.contains('open');
      document.body.classList.toggle('open', willOpen);
      const side = document.getElementById('side') || document.getElementById('sidebar') || document.querySelector('.side, .sidebar');
      if (side) {
        side.classList.toggle('open', willOpen);
      }
    };

    document.addEventListener('click', e => {
      if (e.target.closest('#menu, #mobileMenu, .menu-btn, .mobile-menu-btn')) {
        e.preventDefault();
        toggleMenu();
      } else if (e.target.closest('#scrim') || (document.body.classList.contains('open') && !e.target.closest('.side, .sidebar'))) {
        toggleMenu(false);
      }
    });

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && document.body.classList.contains('open')) {
        toggleMenu(false);
      }
    });

    // --- Active Link Highlighting in Sidebar & Navbar ---
    const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
    document.querySelectorAll('.dash-nav a, .nav a, .nav-links a').forEach(a => {
      const href = a.getAttribute('href');
      if (!href) return;
      const cleanHref = href.split('?')[0].split('#')[0].replace(/\/$/, '') || '/';
      if (cleanHref === currentPath) {
        a.classList.add('active', 'on');
        a.setAttribute('aria-current', 'page');
        const parentLi = a.closest('li');
        if (parentLi) parentLi.classList.add('active');
      }
    });

    // --- Profile Dropdown Menus ---
    const profileBtn = document.getElementById('profileBtn');
    const profileMenu = document.getElementById('profileMenu');
    if (profileBtn && profileMenu) {
      profileBtn.addEventListener('click', e => {
        e.stopPropagation();
        profileMenu.classList.toggle('show');
      });
      document.addEventListener('click', e => {
        if (!e.target.closest('.profile')) {
          profileMenu.classList.remove('show');
        }
      });
    }

    // --- Global Unified Logout Handler ---
    async function handleLogout(e) {
      if (e) e.preventDefault();
      try {
        await fetch('/api/logout', { method: 'POST', credentials: 'same-origin' });
      } catch (_) {}
      try {
        localStorage.removeItem('spendwiseUser');
      } catch (_) {}
      window.location.href = '/login';
    }

    document.querySelectorAll('#logout, #logoutBtn, #profileLogout, #logoutLink').forEach(el => {
      el.addEventListener('click', handleLogout);
    });

    // --- 6. Top Navigation Progress Bar Engine ---
    function ensureTopProgressBar() {
      let bar = document.getElementById('sw-progress-bar');
      if (!bar) {
        bar = document.createElement('div');
        bar.id = 'sw-progress-bar';
        document.body.appendChild(bar);
      }
      return bar;
    }

    function startTopProgressBar() {
      const bar = ensureTopProgressBar();
      bar.classList.add('active');
      bar.style.width = '28%';
      setTimeout(() => {
        if (bar.classList.contains('active')) {
          bar.style.width = '78%';
        }
      }, 70);
    }

    function finishTopProgressBar() {
      const bar = document.getElementById('sw-progress-bar');
      if (!bar) return;
      bar.style.width = '100%';
      setTimeout(() => {
        bar.classList.remove('active');
        setTimeout(() => {
          bar.style.width = '0%';
        }, 180);
      }, 140);
    }

    // --- Page transitions & internal navigation ---
    document.addEventListener('click', e => {
      const a = e.target.closest('a[href]');
      if (!a || e.metaKey || e.ctrlKey || a.target || a.hasAttribute('download')) return;
      const href = a.getAttribute('href');
      if (!href || href[0] === '#' || /^(https?:|mailto:|tel:|javascript:)/.test(href)) return;
      if (href === window.location.pathname + window.location.search) return;

      e.preventDefault();
      startTopProgressBar();
      document.body.classList.add('leaving');
      setTimeout(() => {
        window.location.href = href;
      }, 160);
    });

    window.addEventListener('pageshow', e => {
      document.body.classList.remove('leaving');
      finishTopProgressBar();
    });

    // --- 7. Milestone Confetti Engine ---
    window.spendwiseConfetti = function(originX, originY) {
      if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      let canvas = document.getElementById('sw-confetti-canvas');
      if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.id = 'sw-confetti-canvas';
        document.body.appendChild(canvas);
      }

      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      canvas.width = window.innerWidth * dpr;
      canvas.height = window.innerHeight * dpr;
      ctx.scale(dpr, dpr);

      const colors = ['#14b8a6', '#5eead4', '#0d9488', '#10b981', '#f59e0b', '#6366f1', '#ec4899', '#38bdf8'];
      const particles = [];
      const count = 90;
      const startX = originX !== undefined ? originX : window.innerWidth / 2;
      const startY = originY !== undefined ? originY : window.innerHeight * 0.45;

      for (let i = 0; i < count; i++) {
        const angle = Math.random() * Math.PI * 2;
        const velocity = Math.random() * 12 + 4;
        particles.push({
          x: startX,
          y: startY,
          vx: Math.cos(angle) * velocity,
          vy: Math.sin(angle) * velocity - 3,
          size: Math.random() * 8 + 5,
          color: colors[Math.floor(Math.random() * colors.length)],
          rotation: Math.random() * 360,
          rotationSpeed: (Math.random() - 0.5) * 12,
          opacity: 1,
          decay: Math.random() * 0.012 + 0.012,
          wobble: Math.random() * 10
        });
      }

      let animId;
      function render() {
        ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
        let active = 0;

        particles.forEach(p => {
          if (p.opacity <= 0) return;
          active++;
          p.x += p.vx;
          p.y += p.vy;
          p.vy += 0.28; // gravity
          p.vx *= 0.98; // air friction
          p.rotation += p.rotationSpeed;
          p.opacity -= p.decay;

          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate((p.rotation * Math.PI) / 180);
          ctx.globalAlpha = Math.max(0, p.opacity);
          ctx.fillStyle = p.color;
          ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.7);
          ctx.restore();
        });

        if (active > 0) {
          animId = requestAnimationFrame(render);
        } else {
          cancelAnimationFrame(animId);
          if (canvas && canvas.parentNode) canvas.parentNode.removeChild(canvas);
        }
      }
      render();
    };

    // Auto-trigger confetti on [data-confetti] click or custom events
    document.addEventListener('click', e => {
      const btn = e.target.closest('[data-confetti]');
      if (btn) {
        const rect = btn.getBoundingClientRect();
        window.spendwiseConfetti(rect.left + rect.width / 2, rect.top + rect.height / 2);
      }
    });

    window.addEventListener('spendwise-celebrate', e => {
      const detail = e.detail || {};
      window.spendwiseConfetti(detail.x, detail.y);
    });

    // --- 8. Number Ticker / Roll-Up Animation Engine ---
    window.spendwiseAnimateNumber = function(el, targetTextOrNum, duration = 750) {
      if (!el) return;
      if (el._swAnimId) {
        cancelAnimationFrame(el._swAnimId);
        el._swAnimId = null;
      }
      if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        if (targetTextOrNum !== undefined) el.textContent = targetTextOrNum;
        return;
      }

      const raw = String(targetTextOrNum !== undefined ? targetTextOrNum : el.textContent).trim();
      // Match prefix (currency symbol, sign, etc.), numeric value with commas/decimals, and suffix (%)
      const match = raw.match(/^([^\d\-+.]*?)([\-+])?([0-9,.]+)(.*?)$/);
      if (!match) return;

      const prefix = match[1] || '';
      const sign = match[2] || '';
      const numStr = match[3].replace(/,/g, '');
      const suffix = match[4] || '';
      const targetValue = parseFloat(numStr);
      if (isNaN(targetValue)) return;

      // Determine decimals
      const decimalMatch = numStr.match(/\.(\d+)$/);
      const decimals = decimalMatch ? decimalMatch[1].length : 0;

      const startTime = performance.now();
      const startValue = 0;

      function update(now) {
        const elapsed = now - startTime;
        const progress = Math.min(1, elapsed / duration);
        // Ease-out exponential interpolation
        const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
        const current = startValue + (targetValue - startValue) * ease;

        const formattedNumber = current.toLocaleString('en-IN', {
          minimumFractionDigits: decimals,
          maximumFractionDigits: decimals
        });

        el.textContent = `${prefix}${sign}${formattedNumber}${suffix}`;

        if (progress < 1) {
          el._swAnimId = requestAnimationFrame(update);
        } else {
          el._swAnimId = null;
          el.dataset.swCounted = 'true';
          const finalFormatted = targetValue.toLocaleString('en-IN', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
          });
          el.textContent = `${prefix}${sign}${finalFormatted}${suffix}`;
        }
      }

      el._swAnimId = requestAnimationFrame(update);
    };

    function initNumberCounters() {
      // Exclude loading placeholders (.skel) and elements already managed by custom page scripts (like dashboard #vBal, #vInc, etc.)
      const counterSelectors = '[data-counter], .stat-val:not(.skel)';
      const items = document.querySelectorAll(counterSelectors);
      items.forEach(el => {
        if (el.dataset.swCounted || el.classList.contains('skel') || el.id === 'vBal' || el.id === 'vInc' || el.id === 'vExp' || el.id === 'vSav') {
          return;
        }
        const txt = el.textContent.trim();
        if (/\d/.test(txt) && !txt.includes('...') && txt !== '₹0.00' && txt !== '$0.00' && txt !== '₹0') {
          window.spendwiseAnimateNumber(el);
        }
      });
    }

    // --- 9. Dynamic Progress Bar Animation Controller ---
    window.spendwiseAnimateProgress = function(container = document) {
      const bars = container.querySelectorAll('.progress-fill, .progress-bar');
      bars.forEach(bar => {
        const styleWidth = bar.style.width || bar.getAttribute('data-width');
        if (styleWidth && styleWidth !== '0%') {
          const target = styleWidth;
          const numPercent = parseFloat(target) || 0;
          if (numPercent >= 100) {
            bar.classList.add('danger');
            bar.setAttribute('data-danger', 'true');
          } else if (numPercent >= 80) {
            bar.classList.add('warning');
          }

          bar.style.width = '0%';
          requestAnimationFrame(() => {
            requestAnimationFrame(() => {
              bar.style.width = target;
            });
          });
        }
      });
    };

    // --- 10. Smooth Row Deletion Helper ---
    window.spendwiseAnimateDelete = function(rowElement, callback) {
      return new Promise(resolve => {
        if (!rowElement) {
          if (callback) callback();
          resolve();
          return;
        }

        const height = rowElement.offsetHeight;
        rowElement.style.maxHeight = height + 'px';
        rowElement.style.boxSizing = 'border-box';

        requestAnimationFrame(() => {
          rowElement.classList.add('row-collapsing');
          setTimeout(() => {
            if (rowElement.parentNode) rowElement.parentNode.removeChild(rowElement);
            if (callback) callback();
            resolve();
          }, 330);
        });
      });
    };

    // --- 11. Interactive 3D Mouse Spotlight for Cards ---
    function initCardSpotlights() {
      const cards = document.querySelectorAll('.card, .stat, .stat-card, .goal-card, .budget-card, .settings-card, .spotlight-card');
      cards.forEach(card => {
        card.addEventListener('mousemove', e => {
          const rect = card.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          card.style.setProperty('--mouse-x', `${x}px`);
          card.style.setProperty('--mouse-y', `${y}px`);
        }, { passive: true });
      });
    }

    // --- 12. Tactile Button Click Ripple ---
    document.addEventListener('click', e => {
      const btn = e.target.closest('.btn, button.btn, .icon-btn, .ib');
      if (!btn) return;

      const rect = btn.getBoundingClientRect();
      const circle = document.createElement('span');
      const diameter = Math.max(rect.width, rect.height);
      const radius = diameter / 2;

      circle.style.width = circle.style.height = `${diameter}px`;
      circle.style.left = `${e.clientX - rect.left - radius}px`;
      circle.style.top = `${e.clientY - rect.top - radius}px`;
      circle.classList.add('sw-ripple');

      const existingRipple = btn.querySelector('.sw-ripple');
      if (existingRipple) existingRipple.remove();

      btn.appendChild(circle);
      setTimeout(() => circle.remove(), 600);
    });

    // --- 13. Scroll Reveal & Cascading Ingress Initialization ---
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      const revealTargets = document.querySelectorAll(
        '.card, .stat, .stat-card, .summary-card, .goal-card, .budget-card, .budget-item, .fcard, .step, .step-card, .vcard, .rv'
      );

      const winHeight = window.innerHeight;
      const inViewTargets = [];
      const outOfViewTargets = [];

      revealTargets.forEach(el => {
        const top = el.getBoundingClientRect().top;
        if (top < winHeight * 0.95) {
          inViewTargets.push(el);
        } else {
          outOfViewTargets.push(el);
        }
      });

      // Cascade initial in-view elements
      inViewTargets.forEach((el, idx) => {
        el.classList.add('rv');
        el.style.setProperty('--d', `${(idx % 6) * 45}ms`);
      });

      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          inViewTargets.forEach(el => el.classList.add('in'));
        });
      });

      // Lazy reveal elements entering as user scrolls
      if ('IntersectionObserver' in window && outOfViewTargets.length > 0) {
        const io = new IntersectionObserver((entries, obs) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              entry.target.classList.add('in');
              obs.unobserve(entry.target);
            }
          });
        }, { threshold: 0.08 });

        outOfViewTargets.forEach((el, idx) => {
          el.classList.add('rv');
          el.style.setProperty('--d', `${(idx % 4) * 60}ms`);
          io.observe(el);
        });
      }

      // Initialize micro-interactions
      initCardSpotlights();
      window.spendwiseAnimateProgress();
      setTimeout(initNumberCounters, 120);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootSpendWiseUI);
  } else {
    bootSpendWiseUI();
  }
})();

/* ===== Notification bell (self-contained; injects itself into .top-actions) ===== */
(function(){
  function initBell(){
    var themeBtn = document.getElementById('themeToggle');
    var bar = document.querySelector('.top-actions');
    if(!bar && themeBtn && document.querySelector('header.top, .top')){
      bar = themeBtn.parentElement;
    }
    if(!bar || document.getElementById('notifBtn')) return;

    var wrap = document.createElement('div');
    wrap.className = 'notif-wrap';
    wrap.innerHTML =
      '<button class="notif-btn" id="notifBtn" type="button" aria-label="Notifications" title="Notifications">' +
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/></svg>' +
        '<span class="notif-badge" id="notifBadge">0</span>' +
      '</button>' +
      '<div class="notif-panel" id="notifPanel"></div>';

    if(themeBtn && bar.contains(themeBtn)){
      bar.insertBefore(wrap, themeBtn);
    } else {
      bar.insertBefore(wrap, bar.firstChild);
    }

    var btn = wrap.querySelector('#notifBtn');
    var badge = wrap.querySelector('#notifBadge');
    var panel = wrap.querySelector('#notifPanel');
    var items = [];

    function esc(v){
      return String(v == null ? '' : v).replace(/[&<>"']/g, function(c){
        return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c];
      });
    }

    function ago(iso){
      var d = new Date(iso);
      if(isNaN(d)) return '';
      var s = Math.floor((Date.now() - d.getTime()) / 1000);
      if(s < 60) return 'Just now';
      if(s < 3600) return Math.floor(s / 60) + ' min ago';
      if(s < 86400) return Math.floor(s / 3600) + ' h ago';
      return Math.floor(s / 86400) + ' d ago';
    }

    function setBadge(n){
      badge.textContent = n > 9 ? '9+' : n;
      badge.classList.toggle('show', n > 0);
    }

    function render(){
      var html = '<div class="notif-head"><span>Notifications</span><button type="button" id="notifReadAll">Mark all read</button></div>';
      if(!items.length){
        html += '<div class="notif-empty">You are all caught up.</div>';
      } else {
        html += items.map(function(n){
          return '<div class="notif-item ' + (n.is_read ? '' : 'unread ') + esc(n.severity) + '" data-id="' + n.id + '">' +
            '<span class="notif-dot"></span>' +
            '<div class="notif-body">' +
              '<p class="notif-title">' + esc(n.title) + '</p>' +
              '<p class="notif-msg">' + esc(n.message) + '</p>' +
              '<div class="notif-time">' + esc(ago(n.created_at)) + '</div>' +
            '</div>' +
            '<button class="notif-x" type="button" data-del="' + n.id + '" aria-label="Dismiss">&times;</button>' +
          '</div>';
        }).join('');
      }
      panel.innerHTML = html;
    }

    // Toast only alerts newer than the last one this browser has seen
    function toastNew(){
      var maxId = 0;
      items.forEach(function(n){ if(n.id > maxId) maxId = n.id; });
      var last = null;
      try { last = localStorage.getItem('swLastNotifId'); } catch(e) {}
      if(last !== null && window.showToast){
        items.filter(function(n){ return n.id > Number(last) && !n.is_read && n.severity !== 'info'; })
             .slice(0, 2)
             .forEach(function(n){ window.showToast(n.title + ': ' + n.message, 'error'); });
      }
      try { localStorage.setItem('swLastNotifId', String(maxId)); } catch(e) {}
    }

    async function load(){
      try {
        var r = await fetch('/api/notifications', {headers: {'Accept': 'application/json'}});
        if(!r.ok) return;
        var d = await r.json();
        if(!d.success) return;
        items = d.notifications || [];
        setBadge(d.unread_count || 0);
        render();
        toastNew();
      } catch(e) { console.error(e); }
    }

    btn.addEventListener('click', function(e){
      e.stopPropagation();
      panel.classList.toggle('show');
    });

    document.addEventListener('click', function(e){
      if(!wrap.contains(e.target)) panel.classList.remove('show');
    });

    panel.addEventListener('click', async function(e){
      e.stopPropagation();
      var del = e.target.closest('[data-del]');
      if(del){
        await fetch('/api/notifications/' + del.getAttribute('data-del'), {method: 'DELETE'});
        return load();
      }
      if(e.target.id === 'notifReadAll'){
        await fetch('/api/notifications/read-all', {method: 'POST'});
        return load();
      }
      var row = e.target.closest('.notif-item');
      if(row && row.classList.contains('unread')){
        await fetch('/api/notifications/' + row.getAttribute('data-id') + '/read', {method: 'POST'});
        return load();
      }
    });

    window.refreshNotifications = load;
    load();
    setInterval(function(){ if(!document.hidden) load(); }, 60000);
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initBell);
  } else {
    initBell();
  }
})();
