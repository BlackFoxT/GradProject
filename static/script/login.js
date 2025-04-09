const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

if (document.getElementById('login-next-button')) {
    document.getElementById('login-next-button').addEventListener('click', function () {
        let loginMailInput = document.getElementById('login-email');
        let loginMailValue = loginMailInput.value;

        if (emailRegex.test(loginMailValue)) {
            document.getElementById('login-next-button').style.display = "none";
            document.getElementById('login-submit-button').style.display = "block";
            document.getElementById('login-mail-input').style.display = "none";
            document.getElementById('login-password-input').style.display = "block";

            // Bu kısmın ne olduğunu anlamadım artık htmlde form ile checking yapılıyor
        }
        else {

            var toast = new bootstrap.Toast(document.getElementById('emailToastforLogin'));
            toast.show();

            loginMailInput.focus(); // Bunun da ne olduğunu bilmiyorum
        }
    });
}