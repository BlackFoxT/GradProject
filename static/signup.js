const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

document.getElementById('signup-next-button').addEventListener('click', function(){
    console.log("1");
    let signupMailInput= document.getElementById('signup-email');
    let signupMailValue= signupMailInput.value;
    console.log("2");

    if(emailRegex.test(signupMailValue)){
        console.log("3");
        document.getElementById('signup-next-button').style.display="none";
        document.getElementById('signup-submit-button').style.display="block";
        document.getElementById('signup-mail-input').style.display="none";
        document.getElementById('signup-password-input').style.display="block";

        // Bu kısımda password checking yapılacak
    }
    else{

        // Alert tipi değiştirilebilir.
    console.log("4");

        alert("Geçerli bir mail girin");
        signupMailInput.focus();
    }
});