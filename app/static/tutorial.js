// over the page
// var btnNext = document.getElementById("next");
// btnNext.onclick = function(){
//     window.location.href="rule2.html";
// };
//true or false only
var f = document.getElementById("f");
var t = document.getElementById("t");
t.onclick = function () {
    f.checked = false;
};

f.onclick = function () {
    t.checked = false;
};
//sumbit feedback
var f = document.getElementById("f");
var t = document.getElementById("t");
var submit = document.getElementById("submit");
submit.onclick = function () {
    if (!t.checked) {
        alert("Correct!")
    } else {
        alert("Try again!")
    }
};
//answer page
$('#show').click(function () {
    $('.show-answer').removeClass('display');
});

$('#hide').click(function () {
    $('.show-answer').addClass('display');
});


var tutorial_id = Server.tutorial_id;

function getAnotherTutorial(button) {
    if (!button) {
        if (tutorial_id === 1) {
            alert("this is the first tutorial!");
            return;
        }
        tutorial_id--;
    }
    if (button) {
        if (tutorial_id === 8) {
            alert("you've completed all the tutorial!");
            return;
        }
        tutorial_id++;
    }
    $("#box").scrollTop(0);
    $.post('/tutorialSwitch', {
        target_tutorial_id: tutorial_id
    }).done(function (response) {
        refreshContent(response)
    })

}

function refreshContent(tutorial) {
    $("#title").html(tutorial.title);
    $("#main_content").html(tutorial.main_content);
    $("#subtitle").html(tutorial.subtitle);
    $("#extra_content").html(tutorial.extra_content);
    $("#img_url").attr("src", tutorial.img_url);
    $("#question_title").html(tutorial.question_title);
    $("#hint").html(tutorial.hint);
}