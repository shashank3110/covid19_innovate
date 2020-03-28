
function renderChart(){
	  $.ajax({
        type: "GET",
        url: "india/cases-per-state",
    }).done(function (res) {
        var data = res.count;
        var labels = res.locations;
        var ctx = document.getElementById("myChart").getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            options: {
                legend: {
                    display: false
                },
                tooltips: {
                    enabled: true
                }
            },

            data: {
                labels: labels,
                datasets: [{
                    label: 'Cases per State Data',
                    data: data,
                }]
            },
        });

    }).fail(function (jqXHR, textStatus, errorThrown) {
        document.getElementById('error_msg').innerHTML = jqXHR.responseText;
        if (errorThrown == "BAD REQUEST") {
        }
        if (errorThrown == "UNAUTHORIZED") {
        }
    });
}

function renderLineChart(){
	  $.ajax({
        type: "GET",
        url: "india/cases-per-day",
    }).done(function (res) {
        var data = res.count_per_day;
        var labels = res.dates;
        var ctx = document.getElementById("line-chart").getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            options: {
                legend: {
                    display: false
                },
                tooltips: {
                    enabled: true
                }
            },
            data: {
                labels: labels,
                datasets: [{
                    label: 'Cases Per Day Data',
                    data: data,
                }]
            },
        });

    }).fail(function (jqXHR, textStatus, errorThrown) {
        document.getElementById('error_msg').innerHTML = jqXHR.responseText;
        if (errorThrown == "BAD REQUEST") {
        }
        if (errorThrown == "UNAUTHORIZED") {
        }
    });
}

function renderLineChartPerState(state){
	  $.ajax({
        type: "GET",
        url: "india/cases-per-day-per-state",
        data: {"state" : state},
    }).done(function (res) {
        var data = res.count_per_day;
        var labels = res.dates;
        var ctx = document.getElementById("line-chart-per-state").getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            options: {
                legend: {
                    display: false
                },
                tooltips: {
                    enabled: true
                }
            },
            data: {
                labels: labels,
                datasets: [{
                    label: 'Cases Per Day Data',
                    data: data,
                }]
            },
        });

    }).fail(function (jqXHR, textStatus, errorThrown) {
        document.getElementById('error_msg').innerHTML = jqXHR.responseText;
        if (errorThrown == "BAD REQUEST") {
        }
        if (errorThrown == "UNAUTHORIZED") {
        }
    });
}

$('#states').on('change',function(){
    var state = $(this).val();
		renderLineChartPerState(state);
});

$(document).ready(function() {
    // run the first time; all subsequent calls will take care of themselves
    setTimeout(renderChart, 60000);
    setTimeout(renderLineChart, 60000);
});

renderLineChartPerState('Delhi');
renderChart();
renderLineChart();
