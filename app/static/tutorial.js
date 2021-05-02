//answer page
$('#show').click(function () {
    $('.show-answer').removeClass('display');
});

$('#hide').click(function () {
    $('.show-answer').addClass('display');
});


var tutorial_id = Server.tutorial_id;
var answer = Server.answer


function getAnotherTutorial(button) {
    if (!button) {
        if (tutorial_id === 1) {
            toastr.warning("this is the first tutorial!");
            return;
        }
        tutorial_id--;
    }
    if (button) {
        if (tutorial_id === 8) {
            toastr.success("you've completed all tutorials!");
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