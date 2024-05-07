// registration.js

function togglePasswordVisibility() {
    var passwordInput = document.getElementById("password");
    var toggleCheckbox = document.getElementById("togglePassword");

    passwordInput.type = toggleCheckbox.checked ? "text" : "password";
}

function checkPasswordMatch() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;
    var passwordMatchMsg = document.getElementById("passwordMatchMsg");

    if (password !== confirmPassword) {
        passwordMatchMsg.textContent = "Kata Laluan tidak sepadan";
    } else {
        passwordMatchMsg.textContent = ""; // Clear the message if passwords match
    }
}

function validateForm() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
        alert("Kata Laluan tidak sepadan. Sila cuba lagi.");
        return false;
    }
    return true;
}