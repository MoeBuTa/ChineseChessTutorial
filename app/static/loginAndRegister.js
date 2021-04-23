// for switch box login and register
$('#sign-up').click(function(){
    $('.switch-box').css('transform', 'translateX(80%)');
    $('.sign-in').addClass('display');
    $('.register').removeClass('display');
});

$('#sign-in').click(function(){
    $('.switch-box').css('transform', 'translateX(0%)');
    $('.register').addClass('display');
    $('.sign-in').removeClass('display');
});