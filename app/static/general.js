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
    data.addColumn('number', 'CSR(%)');
    data.addRows([
    ['Satisfied', .7],
    ['Dissatisfied', .2],
    ['Neutral', .1]
    ]);

    var options = {'title':'Questionnaire - Consumer Satisfactional Research',
                'width':800,
                'height':300,

                };

    var chart = new google.visualization.PieChart(document.getElementById('Anthony_chart_div'));
    chart.draw(data, options);


google.charts.load("current", {packages:["calendar"]});
google.charts.setOnLoadCallback(drawChart);

 function drawChart() {
     var dataTable = new google.visualization.DataTable();
     dataTable.addColumn({ type: 'date', id: 'Date' });
     dataTable.addColumn({ type: 'number', id: 'visited' });
     dataTable.addRows([
        [ new Date(2020, 3, 13), 332 ],
        [ new Date(2020, 3, 14), 384 ],
        [ new Date(2020, 4, 15), 324 ],
        [ new Date(2020, 4, 16), 318 ],
        [ new Date(2020, 4, 17), 389 ],
        [ new Date(2020, 5, 4), 387 ],
        [ new Date(2020, 6, 5), 305 ],
        [ new Date(2020, 7, 12), 210 ],
        [ new Date(2020, 8, 13), 389 ],
        [ new Date(2020, 8, 19), 388 ],
        [ new Date(2020, 10, 23), 345 ],
        [ new Date(2020, 10, 24), 346 ],
        [ new Date(2020, 11, 30), 347 ]
      ]);

     var chart = new google.visualization.Calendar(document.getElementById('calendar_basic'));

     var options = {
       title: "Number of Visited our Website",
       width: 1000,
       height: 350,
     };

     chart.draw(dataTable, options);
 }
}
