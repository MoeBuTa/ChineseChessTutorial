// for switch box login and register
$('#sign-up').click(function () {
    $('.switch-box').css('transform', 'translateX(80%)');
    $('.sign-in').addClass('display');
    $('.register').removeClass('display');
});

$('#sign-in').click(function () {
    $('.switch-box').css('transform', 'translateX(0%)');
    $('.register').addClass('display');
    $('.sign-in').removeClass('display');
});


//validate registration form
function registerValidation() {
    var pwd = $("#register_password").val();
    var pwd2 = $("#register_password2").val();
    var email = $("#email").val();
    var response = null;
    mailReg = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
    if (!mailReg.test(email)) {
        toastr.error("Invalid email!");
        return false;
    }

    if (pwd2 !== pwd) {
        toastr.error("The two passwords entered were inconsistent!");
        return false;
    }

    $.ajax({
        url: "/api/registerValidation",
        data: {
            register_username: $("#register_username").val(),
            email: email,
            register_password: pwd
        },
        type: "POST",
        async: false,
        success: function (re) {
            console.log(re)
            response = re;
        },
        error: function () {
            toastr.error("server timeout")
        }
    });

    if (response == 'success') {
        return true;
    }
    else{
        toastr.error(response);
    }
    return false;

}