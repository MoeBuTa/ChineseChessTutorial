var sub = document.getElementById("submit");
sub.onclick = function () {
    alert("You have Submitted!");
};

var cel = document.getElementById("cancel");
cel.onclick = function () {
    window.location.href = "quiz.html";
};


var quiz_id = Server.quiz_id;

console.log(selected_assessments)
for (var i =0; i < selected_assessments.length; i++) {
    if (selected_assessments[i].selected_answer == selected_assessments[i].option_one) {
        $("#A" + selected_assessments[i].id ).attr("checked", true)
    } else if (selected_assessments[i].selected_answer == selected_assessments[i].option_two) {
        $("#B" + selected_assessments[i].id ).attr("checked", true)
    } else if (selected_assessments[i].selected_answer == selected_assessments[i].option_three) {
        $("#C" + selected_assessments[i].id).attr("checked", true)
    } else {
        $("#D" + selected_assessments[i].id ).attr("checked", true)
    }
}

$(':radio').click(function () {
    var selected_answer = $(this).val();
    var assessment_log_id = $(this).attr('name');
    $.post('/saveAssessmentsProgress', {
        selected_answer: selected_answer,
        assessment_log_id: assessment_log_id,
        quiz_id: quiz_id
    }).done(function (response) {

    }).fail(function () {
        // toastr.error("connection timeout!");
    })


});


