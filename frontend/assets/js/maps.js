function refresh_maps_data(){
	  $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/map"
    }).done(function (res) {

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
    setTimeout(refresh_maps_data, 60000);
});

refresh_maps_data();
