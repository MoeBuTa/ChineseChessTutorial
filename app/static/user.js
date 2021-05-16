function toCorrectArray(data) {
    let arrays = [[["Score (%)", "Number of Occurrance"]]];
    let lessforty = 0, mid = 0, largereighty = 0;
    let complete = 1; //0 is false, 1 is true
    let separateScore = [["Quiz Number", "Score (%)"]];
    for (var i = data.length-1; i >= 0; i--) {
        if(data[i] == null){
            complete = 0;
            separateScore.push([data.length-i, -100]);
            continue;
        }
        if(data[i] < 40){
            lessforty++;
        }
        else if(data[i] >= 40 && data[i] < 80){
            mid++;
        }
        else {
            let content = ["≥80", data[i]];
            largereighty++;
        }
        separateScore.push([data.length-i, data[i]]);
    }
    let lessArray = ["<40", lessforty];
    let midArray = ["40-79", mid];
    let largeArray = ["≥80", largereighty];
    arrays[0].push(lessArray, midArray, largeArray);
    arrays.push(separateScore);
    arrays.push(complete);
    return arrays;
}
//  RETURNS: [2D ARRAY DATA FOR PIE, 2D ARRAY DATA FOR LINE, COMPLETE QUIZ NUMBER]
var arrays = toCorrectArray(data);


google.charts.load('current', {'packages': ['corechart']});
google.charts.setOnLoadCallback(drawTuteProgress);

if(data.length > 0) {
    google.charts.setOnLoadCallback(drawLineChart);
    let qComment = "<p>*click on graph dot to see previous quiz result</p>";

    $("#Sarah_chart_div").before("<div class=\"first-quiz\">"+qComment+"</div>")

}
else{
    $("#Sarah_chart_div").addClass("first-quiz");
    $('#Sarah_chart_div').append("<a href="+quizURL+" class=\"text\">Chart is not available! Please click to start your first Quiz here!</a>");
}


google.charts.setOnLoadCallback(drawCharts);




function drawTuteProgress() {
    let tuteProgressData = [["Chinese Chess Tutorial", "Tutorial Progress (Page No.)"],["Current Progress", tutorialProgress]];
    // console.log(tuteProgressData);
    let tuteData = google.visualization.arrayToDataTable(tuteProgressData);
    let tuteOptions = {
      'title': 'My Current Tutorial Progress',
      'width': 1000,
      'height': 300,
      'hAxis': {
        viewWindow: {
        min: 0,
        max: 8 //BETTER TO DYNAMICALLY INSERT TUTE SIZE
        },
      }
    };
    let tuteBarchart = new google.visualization.BarChart(document.getElementById('tute_chart_div'));
    tuteBarchart.draw(tuteData, tuteOptions);
}

function drawCharts() {
    // console.log(arrays);
    var data = google.visualization.arrayToDataTable(arrays[0]);
    var options = {
      'title': 'My Quiz Score Proportion',
      'width': 400,
      'height': 300,
    };

    var chart = new google.visualization.PieChart(document.getElementById('Anthony_chart_div'));
    chart.draw(data, options);

    var barchart_options = {
        title: 'My Quiz Scores',
        width: 400,
        height: 300,
    };
    var barchart = new google.visualization.BarChart(document.getElementById('barchart_div'));
    barchart.draw(data, barchart_options);
}

function drawLineChart() {
    var data = google.visualization.arrayToDataTable(arrays[1]);
    var options = {
        title: 'My Quiz Scores',
        hAxis: {
          title: 'Quiz Number',
        },
        vAxis: {
          title: 'Score (%)',
          format: '0',
        }
      };

      var chart = new google.visualization.LineChart(document.getElementById('Sarah_chart_div'));

      // console.log(QuizIDArray);

      function selectHandler() {
          var selectedItem = chart.getSelection()[0];
          if (selectedItem) {
            var topping = data.getValue(selectedItem.row, 0);
            // alert('The user selected ' + topping);
          }
          var length = QuizIDArray.length;
          var quizID = QuizIDArray[length-topping];
          // alert(quizID);

//        WHEN THERE IS INCOMPLETE QUIZ AND USER CLICKED ON THE INCOMPLETE QUIZ DOT (LAST ONE)
          if(arrays[2] === 0 && topping === length){
              alert("Please click the link below the chart to continue your quiz!")
          }
          else{
              resultFinalURL = resultTempURL + quizID;
              window.location.replace(resultFinalURL);
          }

      };


      google.visualization.events.addListener(chart, 'select', selectHandler);
      chart.draw(data, options);


}

// THERE IS STILL IMCOMPLETE QUIZ
if(arrays[2] == 0){
    // $(".dashboard-progress .text .progress").attr("href", link);
    let comment = "<p>* -100% = Quiz incomplete</p><br>";
    let incomplete = "<a class=\"text\" href="+continueQuizURL+">Click here to continue your Quiz!</a>"
    $("#Sarah_chart_div").after("<div class=\"first-quiz\">"+comment+incomplete+"</div>");
}


//TO DYNAMICALLY CHANGE THE COMMENT BELOW THE TUTE CHART
if(tutorialProgress < 8){
    $("#tute_chart_div").after("<div class=\"first-quiz text\"><a href="+tuteURL+">Click here to continue your Tutorial!</a></div>");
}
else{
    $("#tute_chart_div").after("<div class=\"first-quiz text\"><p>Congradulation! You have completed the tutorial.</p></div>");
}
