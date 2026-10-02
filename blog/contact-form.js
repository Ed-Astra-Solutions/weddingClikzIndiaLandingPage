/* Post-footer enquiry form.
 *
 * The /api/enquiry endpoint rejects any request without a reCAPTCHA v3 token,
 * so the token is fetched before posting. Phone is required here and on the
 * server, matching the homepage form.
 */
(function () {
  'use strict';

  var RECAPTCHA_KEY = '6LevLlIsAAAAACA4B0mAG0wvTCNnubTNA-OgUgai';
  var isLocal = ['localhost', '127.0.0.1'].indexOf(location.hostname) !== -1;
  var API = isLocal ? 'http://localhost:3000' : 'https://api.edastra.in';

  var form = document.getElementById('postEnquiryForm');
  if (!form) return;

  var btn = form.querySelector('.pe-submit');
  var msg = form.querySelector('.pe-msg');
  var label = btn ? btn.textContent : 'Send Enquiry';

  function say(text, kind) {
    if (!msg) return;
    msg.textContent = text;
    msg.className = 'pe-msg ' + (kind || '');
  }

  function token() {
    return new Promise(function (resolve) {
      if (typeof grecaptcha === 'undefined' || !grecaptcha.execute) return resolve(null);
      try {
        grecaptcha.ready(function () {
          grecaptcha.execute(RECAPTCHA_KEY, { action: 'submit_enquiry' })
            .then(resolve)
            .catch(function () { resolve(null); });
        });
      } catch (e) { resolve(null); }
    });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;

    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = (v || '').toString().trim(); });
    if (!data.name || !data.email || !data.phone) {
      say('Name, email and phone are required.', 'err');
      return;
    }
    data.source = 'blog';
    data.page = location.pathname;

    btn.disabled = true;
    btn.textContent = 'Sending…';
    say('', '');

    token().then(function (t) {
      if (t) data.recaptchaToken = t;
      return fetch(API + '/api/enquiry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
    }).then(function (r) {
      return r.json().catch(function () { return { success: false }; });
    }).then(function (res) {
      if (res && res.success) {
        form.reset();
        btn.textContent = 'Sent ✓';
        say('Thank you — we reply within 24 hours.', 'ok');
        setTimeout(function () { btn.textContent = label; btn.disabled = false; }, 3500);
      } else {
        throw new Error((res && res.message) || 'Failed');
      }
    }).catch(function () {
      btn.textContent = label;
      btn.disabled = false;
      say('Could not send that. Please WhatsApp +91 97402 22927 instead.', 'err');
    });
  });
})();
