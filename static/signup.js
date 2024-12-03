
document.getElementById('signup-next-button').addEventListener('click', function () {
    let signupMailInput = document.getElementById('signup-email');
    let signupMailValue = signupMailInput.value;

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (emailRegex.test(signupMailValue)) {
        document.getElementById('signup-next-button').style.display = "none";
        document.getElementById('signup-submit-button').style.display = "block";
        document.getElementById('signup-mail-input').style.display = "none";
        document.getElementById('signup-password-input').style.display = "block";

        // Bu kısmın ne olduğunu anlamadım artık htmlde form ile checking yapılıyor
    }
    else {

        var toast = new bootstrap.Toast(document.getElementById('emailToastforSignup'));
        toast.show();

        signupMailInput.focus(); // Bunun da ne olduğunu bilmiyorum
    }
});

document.getElementById('signup-submit-button').addEventListener('click', function (event) {
    let passwordInput = document.getElementById('signup-password');
    let passwordValue = passwordInput.value;

    const minLength = /.{6,}/;
    const hasUppercase = /[A-Z]/;
    const hasLowercase = /[a-z]/;
    const hasNumber = /\d/;
    const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/;

    let errorMessage;

    if (!minLength.test(passwordValue)) {
        errorMessage = "The password must be at least 6 characters long.";
    }
    else if (!hasUppercase.test(passwordValue)) {
        errorMessage = "The password must contain at least one uppercase letter.";
    }
    else if (!hasLowercase.test(passwordValue)) {
        errorMessage = "The password must contain at least one lowercase letter.";
    }
    else if (!hasNumber.test(passwordValue)) {
        errorMessage = "The password must contain at least one number.";
    }
    else if (!hasSpecialChar.test(passwordValue)) {
        errorMessage = "The password must contain at least one special character.";
    }

    if (errorMessage != null) {
        event.preventDefault();
        displayErrorToast(errorMessage);
        passwordInput.focus();
    }
});

function displayErrorToast(message) {
    const toastElement = document.getElementById('passwordToastforSignup');
    const toastBody = toastElement.querySelector('.toast-body');
    toastBody.innerHTML = message;
    var toast = new bootstrap.Toast(toastElement);
    toast.show();
}

