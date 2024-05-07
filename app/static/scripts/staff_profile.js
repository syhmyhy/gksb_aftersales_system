// staff_profile.js

function togglePasswordVisibility() {
    var currentPasswordInput = document.getElementById("currentPassword");
    var newPasswordInput = document.getElementById("newPassword");
    var confirmPasswordInput = document.getElementById("confirmPassword");
    var toggleCheckbox = document.getElementById("togglePassword");

    var inputs = [currentPasswordInput, newPasswordInput, confirmPasswordInput];

    inputs.forEach(function(input) {
        input.type = toggleCheckbox.checked ? "text" : "password";
    });
}

function checkPasswordMatch() {
    var newPassword = document.getElementById("newPassword").value;
    var confirmPassword = document.getElementById("confirmPassword").value;
    var passwordMatchMsg = document.getElementById("passwordMatchMsg");

    if (newPassword !== confirmPassword) {
        passwordMatchMsg.textContent = "Kata Laluan tidak sepadan";
    } else {
        passwordMatchMsg.textContent = ""; // Clear the message if passwords match
    }
}

function confirmSubmit() {
    var confirmation = confirm("Adakah anda pasti ingin kemaskini Profil anda?");
    if (!confirmation) {
        return false;
    }

    // Validate password match before submitting
    var newPassword = document.getElementById("newPassword").value;
    var confirmPassword = document.getElementById("confirmPassword").value;

    if (newPassword !== confirmPassword) {
        alert("Kata Laluan tidak sepadan. Sila cuba lagi.");
        return false;
    }

    return true;
}

// Event listeners
document.addEventListener("DOMContentLoaded", function() {
    var toggleCheckbox = document.getElementById("togglePassword");
    toggleCheckbox.addEventListener("change", togglePasswordVisibility);

    var confirmPasswordInput = document.getElementById("confirmPassword");
    confirmPasswordInput.addEventListener("keyup", checkPasswordMatch);
});
