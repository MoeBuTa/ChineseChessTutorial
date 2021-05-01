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


function registerValidation() {
    var pwd = $("#register_password").val();
    var pwd2 = $("#register_password2").val();
    var email = $("#email").val();
    var response = null;
    mailReg = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
    if (!mailReg.test(email)) {
        $("#msg").removeClass();
        $("#msg").addClass("alert alert-danger alert-dismissible");
        $("#msg").html("Invalid email!")
        return false;
    }

    if (pwd2 !== pwd) {
        $("#msg").removeClass();
        $("#msg").addClass("alert alert-danger alert-dismissible");
        $("#msg").html("The two passwords entered were inconsistent!")
        return false;
    }

    $.ajax({
        url: "/auth/registerValidation",
        data: {
            register_username: $("#register_username").val(),
            email: email,
            register_password: pwd
        },
        type: "POST",
        async: false,
        success: function (re) {
            response = re;
        }
    });
    $("#msg").html(response.msg)
    if (response.action == 1) {
        $("#msg").removeClass();
        alert("Congratulations, you are now a registered user!")
        return true;
    } else {
        $("#msg").removeClass();
        $("#msg").addClass("alert alert-warning alert-dismissible");
        return false;
    }
}