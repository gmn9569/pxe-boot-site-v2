// Waitlist posts to Formspree. The only setup value is the form id in
// index.html (REPLACE_WITH_FORMSPREE_ID). Nothing is stored in this repo.
(function () {
  var PLACEHOLDER_ID = 'REPLACE_WITH_FORMSPREE_ID';
  var form = document.getElementById('waitlist-form');
  var msg = document.getElementById('form-msg');
  var success = document.getElementById('form-success');
  var year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());
  if (!form || !msg || !success) return;

  var submitBtn = form.querySelector('button[type="submit"]');
  var email = form.elements.email;
  var defaultLabel = submitBtn ? submitBtn.textContent : 'Join the waitlist';

  email.addEventListener('invalid', function (e) {
    e.preventDefault();
    setMsg('Please enter a valid email address.', true);
  });
  email.addEventListener('input', function () {
    if (!msg.hidden && msg.classList.contains('err')) {
      msg.hidden = true;
      msg.textContent = '';
    }
  });

  function formId() {
    var action = form.getAttribute('action') || '';
    var marker = '/f/';
    var at = action.lastIndexOf(marker);
    if (at === -1) return '';
    return action.slice(at + marker.length).split(/[?#]/)[0].replace(/\/+$/, '');
  }

  function setMsg(text, isError) {
    msg.hidden = false;
    msg.className = isError ? 'form-msg err' : 'form-msg';
    msg.textContent = text;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!email.value || !email.checkValidity()) {
      setMsg('Please enter a valid email address.', true);
      email.focus();
      return;
    }

    var id = formId();
    if (!id || id === PLACEHOLDER_ID) {
      setMsg("Thanks for your interest. The waitlist isn't open for signups yet.", false);
      return;
    }
    msg.hidden = true;
    msg.textContent = '';

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Joining…';
    }
    form.setAttribute('aria-busy', 'true');

    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    }).then(function (res) {
      if (!res.ok) throw new Error('waitlist');
      form.hidden = true;
      msg.hidden = true;
      success.hidden = false;
      var heading = success.querySelector('h3');
      if (heading && heading.focus) heading.focus({ preventScroll: true });
    }).catch(function () {
      setMsg('Something went wrong sending that. Please try again in a moment.', true);
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = defaultLabel;
      }
    }).then(function () {
      form.removeAttribute('aria-busy');
    });
  });
})();

// Voice-clone card: play a local sample. Nothing autoplays.
(function () {
  var button = document.querySelector('.voice-toggle');
  var audio = document.getElementById('cari-sample');
  if (!button || !audio) return;

  var playLabel = 'Play voice sample: Cari, an AI character voice';
  var pauseLabel = 'Pause voice sample: Cari, an AI character voice';

  function setPlaying(playing) {
    button.setAttribute('aria-pressed', playing ? 'true' : 'false');
    button.setAttribute('aria-label', playing ? pauseLabel : playLabel);
  }

  button.addEventListener('click', function () {
    if (audio.paused) {
      setPlaying(true);
      var pending = audio.play();
      if (pending && typeof pending.catch === 'function') {
        pending.catch(function () {
          setPlaying(false);
        });
      }
    } else {
      audio.pause();
    }
  });

  audio.addEventListener('play', function () {
    setPlaying(true);
  });
  audio.addEventListener('pause', function () {
    setPlaying(false);
  });
  audio.addEventListener('ended', function () {
    audio.currentTime = 0;
    setPlaying(false);
  });
})();
