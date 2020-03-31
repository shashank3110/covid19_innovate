function load_data(){
	  $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/india/covid19-data"
    }).done(function (res) {
		    var tableHtml='';
        var total = res.total;
        var total_deaths = res.total_deaths;
        var recovered = res.total_recovered;
		    for (var i = 0; i < res.deaths.length; i++) {
            var deaths = res.deaths[i];
            var state = res.states[i];
            var discharged = res.discharged[i];
			      tableHtml += "<tr>"
				        +"<td>"+ state +"</td>"
                + "<td>"+ deaths+"</td>"
				        +  "<td>"+ discharged +"</td>"
                + "</tr>";
        }
		    $('#total_cases').html(total);
        $('#deaths').html(total_deaths);
        $('#recovered').html(recovered);
        $('#state_data tbody').html(tableHtml);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        document.getElementById('error_msg').innerHTML = jqXHR.responseText;
        if (errorThrown == "BAD REQUEST") {
        }
        if (errorThrown == "UNAUTHORIZED") {
        }
    });
}
$(document).ready(function() {
    // run the first time; all subsequent calls will take care of themselves
    setTimeout(load_data, 60000);
});

load_data();
