//charts
google.charts.load('current', {'packages':['corechart']});

google.charts.setOnLoadCallback(drawSarahChart);

google.charts.setOnLoadCallback(drawAnthonyChart);

function drawSarahChart() {

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Topping');
    data.addColumn('number', 'Passing-Rate(%)');
    data.addRows([
    ['Q1', 1],
    ['Q2', .7],
    ['Q3', .8],
    ['Q4', 1],
    ['Q5', .9],
    ['Q6', 1],
    ['Q7', .5],
    ['Q8', .7],
    ['Q9', .9],
    ['Q10', 1]
    ]);

    var options = {'title':'OVERALL - The Passing Rates of Different Quizzes of the Chinese Chess',
                'width':800,
                'height':300,
                vAxis: {minValue:0},

                };

    var chart = new google.visualization.AreaChart(document.getElementById('Sarah_chart_div'));
    chart.draw(data, options);
}

function drawAnthonyChart() {

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Topping');
    data.addColumn('number', 'Passing-Rate(%)');
    data.addRows([
    ['Q1', 1],
    ['Q2', .7],
    ['Q3', .8],
    ['Q4', 1],
    ['Q5', .9],
    ['Q6', 1],
    ['Q7', .5],
    ['Q8', .7],
    ['Q9', .9],
    ['Q10', 1]
    ]);

    var options = {'title':'OVERALL - The Passing Rates of Different Quizzes of the Chinese Chess',
                'width':800,
                'height':300,
                vAxis: {minValue:0},

                };

    var chart = new google.visualization.BarChart(document.getElementById('Anthony_chart_div'));
    chart.draw(data, options);
}
