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
