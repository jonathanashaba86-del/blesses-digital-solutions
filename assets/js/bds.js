/* Blessed Digital Solutions — site behaviour
   Progressive enhancement only: every page works with JS disabled. */
(function () {
  'use strict';

  /* --- Mobile navigation --- */
  var nav = document.querySelector('[data-nav]');
  if (nav) {
    var toggle = nav.querySelector('[data-nav-toggle]');
    var setOpen = function (open) {
      nav.setAttribute('data-open', open ? 'true' : 'false');
      if (toggle) toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    if (toggle) {
      toggle.addEventListener('click', function () {
        setOpen(nav.getAttribute('data-open') !== 'true');
      });
    }
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  }

  /* --- Scroll reveal --- */
  var revealables = document.querySelectorAll('[data-reveal]');
  if (revealables.length) {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce || !('IntersectionObserver' in window)) {
      revealables.forEach(function (el) { el.classList.add('is-visible'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
      revealables.forEach(function (el, i) {
        el.style.transitionDelay = Math.min(i % 4, 3) * 70 + 'ms';
        io.observe(el);
      });
    }
  }

  /* --- Enquiry form (static host: no backend, so hand off to email) --- */
  var form = document.querySelector('[data-enquiry-form]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var get = function (k) { return String(data.get(k) || '').trim(); };
      var lines = [
        'Name: ' + get('name'),
        'Company: ' + get('company'),
        'Email: ' + get('email'),
        'Phone: ' + get('phone'),
        'Product of interest: ' + get('product'),
        '',
        get('message')
      ];
      var subject = 'BDS Product Lab enquiry — ' + (get('product') || 'General');
      var href = 'mailto:' + form.dataset.enquiryForm +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(lines.join('\n'));
      var status = form.querySelector('[data-form-status]');
      if (status) {
        status.setAttribute('data-state', 'ok');
        status.textContent = 'Thank you, ' + (get('name') || 'there') +
          '. Your email client is opening with the brief prefilled — send it and we reply within one working day.';
      }
      window.location.href = href;
    });
  }

  /* --- Current year --- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
