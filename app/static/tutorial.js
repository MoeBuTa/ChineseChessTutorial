//answer page
$('#show').click(function () {
    $('.show-answer').removeClass('display');
});

$('#hide').click(function () {
    $('.show-answer').addClass('display');
});


var tutorial_num = Server.tutorial_num;
var answer = Server.answer;
var count = Server.tutorial_count;

//function for switching tutorial chapters
function getAnotherTutorial(button) {
    if (!button) {
        if (tutorial_num == 1) {
            toastr.warning("this is the first tutorial!");
            return;
        }
        tutorial_num--;
    }
    if (button) {
        if (tutorial_num == count) {
            toastr.success("you've completed all tutorials!");
            return;
        }
        tutorial_num++;
    }
    $.post('/tutorialSwitch', {
        target_tutorial_num: tutorial_num
    }).done(function (response) {
        $("#box").scrollTop(0);
        refreshContent(response)
    }).fail(function (){
        toastr.error("connection timeout!");
    })

}

//update tutorial content by assigning data received from server
function refreshContent(tutorial) {
    $("#title").html(tutorial.title);
    $("#main_content").html(tutorial.main_content);
    $("#subtitle").html(tutorial.subtitle);
    $("#extra_content").html(tutorial.extra_content);
    $("#img_url").attr("src", tutorial.img_url);
    $("#question_title").html(tutorial.question_title);
    $("#hint").html(tutorial.hint);
    answer = tutorial.answer
    $(':radio').prop('checked', false);
}

$(':radio').click(function () {
    if ($(this).val() != answer) {
        toastr.error("Try again!");
    } else {
        toastr.success("Correct!");
    }
});