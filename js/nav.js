/* =========================
   Hamburger Navigation — Right-Side Drawer
   Vanilla JS — no frameworks
   ========================= */
document.addEventListener('DOMContentLoaded', function () {
    const btn = document.querySelector('.hamburger');
    if (!btn) return;

    const nav = btn.closest('nav');

    /* Build the overlay */
    const overlay = document.createElement('div');
    overlay.className = 'nav-overlay';
    document.body.appendChild(overlay);

    /* Build the drawer and clone all nav links into it */
    const drawer = document.createElement('div');
    drawer.className = 'nav-drawer';
    drawer.setAttribute('aria-label', 'Site navigation');

    nav.querySelectorAll('a').forEach(function (link) {
        const clone = link.cloneNode(true);
        drawer.appendChild(clone);
    });

    document.body.appendChild(drawer);

    /* Open / close helpers */
    function openMenu() {
        drawer.classList.add('nav-open');
        overlay.classList.add('nav-open');
        btn.setAttribute('aria-expanded', 'true');
        btn.textContent = '\u2715';   /* ✕ when open */
    }

    function closeMenu() {
        drawer.classList.remove('nav-open');
        overlay.classList.remove('nav-open');
        btn.setAttribute('aria-expanded', 'false');
        btn.textContent = '\u2630';   /* ☰ when closed */
    }

    btn.addEventListener('click', function () {
        drawer.classList.contains('nav-open') ? closeMenu() : openMenu();
    });

    /* Close on overlay click */
    overlay.addEventListener('click', closeMenu);

    /* Close on any drawer link tap */
    drawer.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', closeMenu);
    });
});

/* =========================
   Dark Mode Toggle
   Vanilla JS — persists preference in localStorage
   ========================= */
document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.querySelector('.theme-toggle');
    if (!themeToggle) return;

    const sunIcon = '☀️';
    const moonIcon = '🌙';

    /* Check for saved theme preference or default to light */
    function getPreferredTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        /* Check system preference */
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    /* Apply theme to document */
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        updateToggleButton(theme);
    }

    /* Update the toggle button icon and text */
    function updateToggleButton(theme) {
        const icon = themeToggle.querySelector('.icon');
        const text = themeToggle.querySelector('.text');
        if (theme === 'dark') {
            if (icon) icon.textContent = sunIcon;
            if (text) text.textContent = 'Light';
        } else {
            if (icon) icon.textContent = moonIcon;
            if (text) text.textContent = 'Dark';
        }
    }

    /* Initialize theme on page load */
    const currentTheme = getPreferredTheme();
    applyTheme(currentTheme);

    /* Toggle theme on button click */
    themeToggle.addEventListener('click', function () {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', newTheme);
        applyTheme(newTheme);
    });
});
