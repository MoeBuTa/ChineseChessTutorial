var sub = document.getElementById("submit");
sub.onclick = function () {
    alert("You have Submitted!");
};


var quiz_id = Server.quiz_id;

for (var i = 0; i < selected_questions.length; i++) {
    if (selected_questions[i].selected_answer == selected_questions[i].option_one) {
        $("#E" + selected_questions[i].id).removeAttr("checked", true)
        $("#A" + selected_questions[i].id).attr("checked", true)
    } else if (selected_questions[i].selected_answer == selected_questions[i].option_two) {
        $("#E" + selected_questions[i].id).removeAttr("checked", true)
        $("#B" + selected_questions[i].id).attr("checked", true)
    } else if (selected_questions[i].selected_answer == selected_questions[i].option_three) {
        $("#E" + selected_questions[i].id).removeAttr("checked", true)
        $("#C" + selected_questions[i].id).attr("checked", true)
    } else if (selected_questions[i].selected_answer == selected_questions[i].option_four) {
        $("#E" + selected_questions[i].id).removeAttr("checked", true)
        $("#D" + selected_questions[i].id).attr("checked", true)
    } else {
    }

}

$(':radio').click(function () {
    var selected_answer = $(this).val();
    console.log(selected_answer)
    var question_log_id = $(this).attr('name');
    var data = {
        'selected_answer': selected_answer,
        'question_log_id': question_log_id,
        'quiz_id': quiz_id
    }
    $.post('/api/saveQuestionsProgress', data).done(function (response) {
        toastr.success("answer saved!");
    }).fail(function () {
        toastr.error("connection timeout!");
    })
});







