/*Search through leagues*/
$(document).ready(function() {
    $("#searchLeagues").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#leagueTable tbody tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

/*Send a request to join a league*/
$(".request-button").click(function() {
    var leagueName = $(this).parent().siblings('.league-name').html();
    var requestButtonObject = $(this);
    $.ajax({
        url: '/league/request/',
        data: {
            'leagueName': leagueName
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == "SUCCESS") {
                requestButtonObject.prop("disabled", true);
                requestButtonObject.prop('value', 'Requested');
            } else if (data.status == "DUPLICATE") {
                alert("You have already requested to join this league.");
            } else {
                alert("Unable to complete your request.");
            }
        }
    });
});


/*Join league*/
$(".join-button").click(function() {
    var leagueName = $(this).parent().siblings('.league-name').html();
    var joinButtonObject = $(this);
    $.ajax({
        url: '/league/addPublic/',
        data: {
            'leagueName': leagueName
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == "SUCCESS") {
                joinButtonObject.prop("disabled", true);
                joinButtonObject.prop('value', 'Joined');
            } else if (data.status == "DUPLICATE") {
                alert("You are already a member of this league.");
            } else {
                alert("Unable to complete your request.");
            }
        }
    });
});