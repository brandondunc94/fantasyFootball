$(document).ready(function() {

});

/*Select a team box to make bets*/
$(".bet-box").click(function() {
    if ($(this).children('input').is(':disabled')) {
        /*Radio button is locked, do nothing*/
    } else if ($(this).hasClass('bet-box-selected')) {
        /*Unselect the currently selected box and unselect radio button*/
        $(this).removeClass('bet-box-selected')
        var radioButton = $(this).find("input");
        radioButton.attr('checked', false);

        /*Select opposite div and radio button to mark as untouched bet box*/
        var oppositeDiv = $(this).siblings('.bet-box');
        oppositeDiv.removeClass('bet-box-unselected')

        /*Save pick as None*/
        var gameId = $(this).children('input').attr('name');
        savePick(gameId, null)
    } else {
        /*Select child radio button and div to mark as checked*/
        $(this).toggleClass(function() {
            return $(this).is('.bet-box-selected, .bet-box-unselected') ? 'bet-box-selected bet-box-unselected' : 'bet-box-selected';
        }, 200)
        var radioButton = $(this).find("input");
        radioButton.attr('checked', true);
        var gameId = $(this).children('input').attr('name');
        var pick = $(this).children('input').attr('id');
        savePick(gameId, pick);

        /*Select opposite div and radio button to mark as unchecked*/
        var oppositeDiv = $(this).siblings(".bet-box");
        oppositeDiv.toggleClass(function() {
            return oppositeDiv.is('.bet-box-unselected, .bet-box-selected') ? 'bet-box-unselected bet-box-selected' : 'bet-box-unselected';
        }, 200)
        oppositeRadioButton = oppositeDiv.find("input");
        oppositeRadioButton.attr('checked', false);
    }
});

/*Save pick*/
function savePick(gameId, pick) {
    var leagueName = $('#leagueName').attr('name');
    var weekId = $('#weekId').attr('name');
    $.ajax({
        url: '/picks/save/',
        data: {
            'leagueName': leagueName,
            'weekId': weekId,
            'gameId': gameId,
            'pick': pick
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == false) {
                alert("Unable to save pick. The Onside Pick developer team has been notified. We apologize for the inconvenience.");
            } else {}
        }
    });
}