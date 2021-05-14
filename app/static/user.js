function toCorrectPieArray(data) {
    let arrays = [[["Score (%)", "Number of Occurrance"]]];
    let lessforty = 0, mid = 0, largereighty = 0;
    let complete = 1; //0 is false, 1 is true
    let separateScore = [["Quiz Number", "Score (%)"]];
    for (var i = 0; i < data.length; i++) {
        if(data[i] == null){
            complete = 0;
            separateScore.push([i+1, -100]);
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
        separateScore.push([i+1, data[i]]);
    }
    let lessArray = ["<40", lessforty];
    let midArray = ["40-79", mid];
    let largeArray = ["≥80", largereighty];
    arrays[0].push(lessArray, midArray, largeArray);
    arrays.push(separateScore);
    arrays.push(complete);
    return arrays;
}
var arrays = toCorrectPieArray(data);


google.charts.load('current', {'packages': ['corechart']});
google.charts.setOnLoadCallback(drawCharts);
google.charts.setOnLoadCallback(drawLineChart);
function drawCharts() {
    console.log(arrays);
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
        hAxis: {
          title: 'Quiz Number',
        },
        vAxis: {
          title: 'Score (%)',
          format: '0',
        }
      };

      var chart = new google.visualization.LineChart(document.getElementById('Sarah_chart_div'));

      chart.draw(data, options);

}

// THERE IS STILL IMCOMPLETE QUIZ

function changeAIfImcomplete(url){
    if(arrays[2] == 0){
        $(".dashboard-progress .text .progress").attr("href", url);
        $("#Sarah_chart_div").after("<br><p>* -100% = Quiz incomplete</p>");
    }
}
