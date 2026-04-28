// Wait for the DOM to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', function() {
  // ----------------------------------------------------------
  // Get all the elements we need from the page
  // ----------------------------------------------------------
  const form = document.getElementById('member-form');
  const usernameInput = document.getElementById('username');
  const usernameFeedback = document.getElementById('username-feedback');
  const passwordInput = document.getElementById('password');
  const togglePasswordIcon = document.getElementById('toggle-password');

  // Check if all required elements exist
  if (!form || !usernameInput || !usernameFeedback || !passwordInput || !togglePasswordIcon) {
    console.warn('Some required form elements not found');
    return;
  }

  // The URL to check if a username exists.
  // We store it on the form as a "data-check-url" attribute,
  // because we cannot use Django's {% url %} tag inside a .js file.
  const checkUrl = form.dataset.checkUrl;

  // This will become true when the typed username is already taken.
  let isUsernameTaken = false;

  // A timer used to wait until the user stops typing before checking.
  let typingTimer = null;


  // ----------------------------------------------------------
  // Show a message under the username field (green / red / gray)
  // ----------------------------------------------------------
  function showMessage(color, text) {
    // Reset any previous styles first
    usernameInput.classList.remove('is-valid', 'is-invalid');
    usernameFeedback.classList.remove('text-success', 'text-danger', 'text-muted');

    if (color === 'green') {
      usernameInput.classList.add('is-valid');
      usernameFeedback.classList.add('text-success');
    } else if (color === 'red') {
      usernameInput.classList.add('is-invalid');
      usernameFeedback.classList.add('text-danger');
    } else {
      usernameFeedback.classList.add('text-muted');
    }

    usernameFeedback.textContent = text;
  }


  // ----------------------------------------------------------
  // Ask the server if the username already exists
  // ----------------------------------------------------------
  function checkUsername() {
    const value = usernameInput.value.trim();

    // If the box is empty, clear the message
    if (value === '') {
      showMessage('', '');
      isUsernameTaken = false;
      return;
    }

    // If user is editing and didn't change their own username, skip the check
    if (value === usernameInput.dataset.original) {
      showMessage('', '');
      isUsernameTaken = false;
      return;
    }

    // Show a "checking" message while we wait for the server's reply
    showMessage('gray', 'Checking…');

    // Send the request to Django
    fetch(checkUrl + '?username=' + encodeURIComponent(value))
      .then(response => response.json())
      .then(data => {
        if (data.exists) {
          isUsernameTaken = true;
          showMessage('red', 'Username already taken');
        } else {
          isUsernameTaken = false;
          showMessage('green', 'Username is available');
        }
      })
      .catch((error) => {
        console.error('Error checking username:', error);
        // If something went wrong, just clear the message
        showMessage('', '');
        isUsernameTaken = false;
      });
  }


  // ----------------------------------------------------------
  // When the user types, wait 400ms then check the username.
  // (This stops us from sending a request on every keystroke.)
  // ----------------------------------------------------------
  usernameInput.addEventListener('input', function () {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(checkUsername, 400);
  });


  // ----------------------------------------------------------
  // Block the form from submitting if the username is taken
  // ----------------------------------------------------------
  form.addEventListener('submit', function (event) {
    if (isUsernameTaken) {
      event.preventDefault();
      usernameInput.focus();
      alert('Please choose a different username');
    }
  });


  // ----------------------------------------------------------
  // Show / hide the password when the eye icon is clicked
  // ----------------------------------------------------------
  togglePasswordIcon.addEventListener('click', function () {
    if (passwordInput.type === 'password') {
      // Currently hidden → show it
      passwordInput.type = 'text';
      togglePasswordIcon.classList.remove('fa-eye');
      togglePasswordIcon.classList.add('fa-eye-slash');
    } else {
      // Currently shown → hide it
      passwordInput.type = 'password';
      togglePasswordIcon.classList.remove('fa-eye-slash');
      togglePasswordIcon.classList.add('fa-eye');
    }
  });
});
