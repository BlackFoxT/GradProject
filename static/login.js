const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

document.getElementById('login-next-button').addEventListener('click', function(){
    let loginMailInput= document.getElementById('login-email');
    let loginMailValue= loginMailInput.value;

    if(emailRegex.test(loginMailValue)){
        document.getElementById('login-next-button').style.display="none";
        document.getElementById('login-submit-button').style.display="block";
        document.getElementById('login-mail-input').style.display="none";
        document.getElementById('login-password-input').style.display="block";

        // Bu kısımda password checking yapılacak
    }
    else{

        // Alert tipi değiştirilebilir.

        alert("Geçerli bir mail girin");
        loginMailInput.focus();
    }
});