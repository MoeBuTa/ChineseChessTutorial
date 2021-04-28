// over the page
var btnNext = document.getElementById("next");
btnNext.onclick = function(){
    window.location.href="rule2.html";
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
//sumbit feedback
var f = document.getElementById("f");
var t = document.getElementById("t");
var submit = document.getElementById("submit");
submit.onclick = function(){
    if(t.checked != false){
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
        
