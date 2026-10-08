// PLACEHOLDER waitlist handler: nothing is sent or stored anywhere.
// Replace with a real signup provider before launch.
(function () {
  var form = document.getElementById('waitlist-form');
  var msg = document.getElementById('form-msg');
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var email = form.email;
    if (!email.value || !email.checkValidity()) {
      msg.className = 'form-msg err';
      msg.textContent = 'Please enter a valid email address.';
      email.focus();
      return;
    }
    msg.className = 'form-msg';
    msg.textContent = "Thanks! Signups are coming soon. We'll open the waitlist shortly.";
    form.reset();
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
