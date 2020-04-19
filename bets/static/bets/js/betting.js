/*Search through leagues*/
/*$(document).ready(function() {
    $("#searchLeagues").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#leagueTable tbody tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});*/

/*Increment bet amount*/
$(".increase-bet-button").click(function() {

});

/*Send a request to join a league*/
$(".bet-box").click(function() {
    if ($(this).hasClass('bet-box-selected')) {
        /*do nothing since the div is already selected*/
    } else {
        /*Select child radio button and div to mark as checked*/
        $(this).toggleClass(function() {
            return $(this).is('.bet-box-selected, .bet-box-unselected') ? 'bet-box-selected bet-box-unselected' : 'bet-box-selected';
        }, 200)
        var radioButton = $(this).find("input");
        radioButton.attr('checked', true);

        /*Select opposite div and radio button to mark as unchecked*/
        var oppositeDiv = $(this).siblings(".bet-box");
        oppositeDiv.toggleClass(function() {
            return oppositeDiv.is('.bet-box-unselected, .bet-box-selected') ? 'bet-box-unselected bet-box-selected' : 'bet-box-unselected';
        }, 200)
        oppositeRadioButton = oppositeDiv.find("input");
        oppositeRadioButton.attr('checked', false);
    }






    /*$.ajax({
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
    });*/
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