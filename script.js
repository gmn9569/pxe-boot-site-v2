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
