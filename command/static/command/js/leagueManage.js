/*Search through leagues*/
$(document).ready(function() {
    $("#searchLeagues").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#leagueTable tbody tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

/*Delete selected league*/
$(".delete-button").click(function() {
    var leagueName = $(this).parent().siblings('.league-name').html();
    var deleteButtonObject = $(this);
    $.ajax({
        url: '/command/leaguedelete/',
        data: {
            'leagueName': leagueName
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == true) {
                deleteButtonObject.prop("disabled", true);
                deleteButtonObject.prop('value', 'Deleted');
            } else {
                alert("Unable to delete league.");
            }
        }
    });
});