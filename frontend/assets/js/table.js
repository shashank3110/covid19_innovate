function load_hospital_data(){
	  $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/india/hospitals"
    }).done(function (res) {
		    var tableHtml='';
		    for (var i = 0; i < res.hospitals.length; i++) {
            var hospital = res.hospitals[i];
            var state = res.states[i];
            var beds = res.beds[i];
			      tableHtml += "<tr>"
				        +"<td>"+ state +"</td>"
                + "<td>"+ beds+"</td>"
				        +  "<td>"+ hospital +"</td>"
                + "</tr>";
        }
		    $('#hospitals_table tbody').html(tableHtml);
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
    setTimeout(load_hospital_data, 60000);
});

load_hospital_data();
