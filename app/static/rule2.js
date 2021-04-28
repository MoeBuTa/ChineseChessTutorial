//over the page
var btnPre = document.getElementById("pre");
btnPre.onclick = function(){
    window.location.href="rule1.html";
};
//true or false only
var f = document.getElementById("f");
var t = document.getElementById("t");
t.onclick = function(){
    f.checked = false;
};

f.onclick = function(){
    t.checked = false;
};
//submit feedback
var f = document.getElementById("f");
var t = document.getElementById("t");
var submit = document.getElementById("submit");
submit.onclick = function(){
    if(f.checked != false){
        alert("Correct!")
    }else{
        alert("Try again!")
    }
};
//answer page
$('#show').click(function(){
    $('.show-answer').removeClass('display');
});

$('#hide').click(function(){
    $('.show-answer').addClass('display');
});
