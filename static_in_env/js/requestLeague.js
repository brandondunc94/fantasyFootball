// Basic example
$(document).ready(function() {
    $('#leagueTable').DataTable();
    $('.dataTables_length').addClass('bs-select');
});

function requestLeague() // no ';' here
{
    var requestButton = document.getElementById("requestButton");
    requestButton.type = 'text';
    requestButton.value = "Requested";
}