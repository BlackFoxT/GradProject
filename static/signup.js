const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

document.getElementById('signup-next-button').addEventListener('click', function () {
    let signupMailInput = document.getElementById('signup-email');
    let signupMailValue = signupMailInput.value;

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