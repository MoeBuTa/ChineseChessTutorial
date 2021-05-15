// var sub = document.getElementById("submit");
// sub.onclick = function () {
//     alert("You have Submitted!");
// };

window.onload=function(){
for (var i = 0; i < selected_questions.length; i++) {
    if (selected_questions[i].selected_answer == selected_questions[i].option_one) {
        $("#E" + selected_questions[i].id).removeProp("checked", true)
        $("#A" + selected_questions[i].id).attr("checked", true)
    } else if (selected_questions[i].selected_answer == selected_questions[i].option_two) {
        $("#E" + selected_questions[i].id).removeProp("checked", true)
        $("#B" + selected_questions[i].id).prop("checked", true)
    } else if (selected_questions[i].selected_answer == selected_questions[i].option_three) {
        $("#E" + selected_questions[i].id).removeProp("checked", true)
        $("#C" + selected_questions[i].id).prop("checked", true)
    } else if (selected_questions[i].selected_answer == selected_questions[i].option_four) {
        $("#E" + selected_questions[i].id).removeProp("checked", true)
        $("#D" + selected_questions[i].id).prop("checked", true)
    } else {
    }

}
}
var quiz_id = Server.quiz_id;



$(':radio').click(function () {
    var selected_answer = $(this).val();
    var question_log_id = $(this).prop('name');
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







