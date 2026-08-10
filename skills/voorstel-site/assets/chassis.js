/* ============================================================================
   AGYLE VOORSTEL-CHASSIS — gedrag
   Één observer voor alles. JS zet alleen klassen; de timing blijft in CSS.
   Elke init in try/catch: één exception mag nooit de hele pagina op opacity:0 laten staan.
   ============================================================================ */

document.documentElement.classList.replace('no-js', 'js');

/* -------------------------------------------------- 1. De enige observer */
const io = new IntersectionObserver((entries, obs) => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add('is-visible');
    obs.unobserve(e.target);              // eenrichtingsverkeer — herhaling leest als goedkoop
  });
}, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

function initReveals() {
  document.querySelectorAll('.reveal, .choreo').forEach(el => io.observe(el));
  document.querySelectorAll('.reveal-group').forEach(g => {
    [...g.children].forEach((c, i) => c.style.setProperty('--i', i));
    io.observe(g);                        // de CONTAINER, niet de kinderen
  });
}

/* --------------------------------------------- 2. Header die wegduikt */
function initHeader() {
  const header = document.querySelector('.header');
  if (!header) return;
  let lastY = window.scrollY;
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    if (Math.abs(y - lastY) < 8) return;              // drempel tegen rubber-band-jitter
    header.classList.toggle('is-hidden', y > 200 && y > lastY);
    lastY = y;
  }, { passive: true });
}

/* ---------------------------------------------------- 3. Accordeon */
function initAccordions() {
  document.querySelectorAll('.acc__head').forEach(head => {
    head.setAttribute('aria-expanded', head.closest('.acc').classList.contains('is-open'));
    head.addEventListener('click', () => {
      const acc = head.closest('.acc');
      const open = acc.classList.toggle('is-open');
      head.setAttribute('aria-expanded', open);
    });
  });
}
/* Markup: <div class="acc is-open"><button class="acc__head" aria-expanded="true">…
   Een <button>, geen <div> met listener — anders is het paneel niet met toetsenbord te openen. */

/* ---------------------------------------------------- 4. Count-up */
function initCountUp() {
  const obs = new IntersectionObserver((entries, o) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target;
      const target = parseInt(el.dataset.count, 10);
      const t0 = performance.now(), dur = 1200;
      (function tick(now) {
        const p = Math.min((now - t0) / dur, 1);
        const eased = 1 - Math.pow(1 - p, 3);                      // easeOutCubic
        el.textContent = (el.dataset.prefix || '') +
                         Math.round(eased * target).toLocaleString('nl-NL') +
                         (el.dataset.suffix || '');
        if (p < 1) requestAnimationFrame(tick);
      })(t0);
      o.unobserve(el);
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('[data-count]').forEach(el => obs.observe(el));
}
/* Harde voorwaarde: font-variant-numeric: tabular-nums plus een gereserveerde breedte in ch,
   anders springt de layout per frame. */

/* ------------------------------------------------------- 5. De gate */
/* LET OP: dit is frame-setting, geen beveiliging. Zet er .htpasswd of een signed token
   onder als het document echt vertrouwelijk is — claim geen vertrouwelijkheid die je
   niet levert. De vorm blijft 100% hetzelfde. */
function initGate(pin) {
  const gate = document.querySelector('.gate');
  if (!gate) return;
  const wrap = gate.querySelector('.gate__inputs');
  const digits = [...gate.querySelectorAll('.gate__digit')];
  const KEY = 'unlocked:' + location.pathname;

  try { if (sessionStorage.getItem(KEY)) { gate.remove(); return; } } catch (_) {}

  document.body.style.overflow = 'hidden';
  digits[0].focus();

  const value = () => digits.map(d => d.value).join('');

  function check() {
    if (value().length < digits.length) return;
    if (value() === pin) {
      wrap.classList.add('is-success');
      setTimeout(() => {                                  // 500ms pauze — dít ís het effect
        gate.classList.add('is-hidden');                  // 0.5s CSS-fade
        document.body.style.overflow = '';
        try { sessionStorage.setItem(KEY, '1'); } catch (_) {}
        setTimeout(() => gate.remove(), 600);             // loopt parallel aan de fade
      }, 500);
    } else {
      wrap.classList.add('is-error');
      setTimeout(() => wrap.classList.remove('is-error'), 450);
      digits.forEach(d => { d.value = ''; d.classList.remove('is-filled'); });
      digits[0].focus();
    }
  }

  digits.forEach((d, i) => {
    d.addEventListener('focus', () => d.select());
    d.addEventListener('input', () => {
      d.value = d.value.replace(/\D/g, '').slice(-1);
      d.classList.toggle('is-filled', !!d.value);
      if (d.value && i < digits.length - 1) digits[i + 1].focus();
      check();
    });
    d.addEventListener('keydown', e => {
      if (e.key === 'Backspace' && !d.value && i > 0) { digits[i - 1].focus(); digits[i - 1].value = ''; }
      if (e.key === 'ArrowLeft'  && i > 0) digits[i - 1].focus();
      if (e.key === 'ArrowRight' && i < digits.length - 1) digits[i + 1].focus();
    });
    /* Plakken vult alle vakjes in één keer — het detail dat de meeste implementaties vergeten */
    d.addEventListener('paste', e => {
      e.preventDefault();
      const chars = (e.clipboardData.getData('text') || '').replace(/\D/g, '').split('');
      digits.forEach((x, j) => { x.value = chars[j] || ''; x.classList.toggle('is-filled', !!chars[j]); });
      check();
    });
  });
}
/* Markup per vakje: <input class="gate__digit" type="tel" inputmode="numeric" maxlength="1">
   Vier losse inputs, geen enkel veld met maxlength=4 — dat patroon leent de autoriteit
   van 2FA-flows van banken. Voeg role="dialog" + aria-modal + focus-trap toe. */

/* ------------------------------------------------------------- 6. Init */
document.addEventListener('DOMContentLoaded', () => {
  [initReveals, initHeader, initAccordions, initCountUp].forEach(fn => {
    try { fn(); } catch (err) { console.error(fn.name, err); }
  });
  try { initGate('0000'); } catch (err) { console.error('initGate', err); }
});
