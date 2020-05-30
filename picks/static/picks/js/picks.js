$(document).ready(function() {

});

/*Select a team box to make picks*/
$(".pick-box").click(function() {
    if ($(this).children('input').is(':disabled')) {
        /*Radio button is locked, do nothing*/
    } else if ($(this).hasClass('pick-box-selected')) {
        /*Unselect the currently selected box and unselect radio button*/
        $(this).removeClass('pick-box-selected')
        var radioButton = $(this).find("input");
        radioButton.attr('checked', false);

        /*Select opposite div and radio button to mark as untouched pick box*/
        var oppositeDiv = $(this).siblings('.pick-box');
        oppositeDiv.removeClass('pick-box-unselected')

        /*Save pick as None*/
        var gameId = $(this).children('input').attr('name');
        savePick(gameId, null)
    } else {
        /*Select child radio button and div to mark as checked*/
        $(this).toggleClass(function() {
            return $(this).is('.pick-box-selected, .pick-box-unselected') ? 'pick-box-selected pick-box-unselected' : 'pick-box-selected';
        }, 200)
        var radioButton = $(this).find("input");
        radioButton.attr('checked', true);
        var gameId = $(this).children('input').attr('name');
        var pick = $(this).children('input').val();
        savePick(gameId, pick);

        /*Select opposite div and radio button to mark as unchecked*/
        var oppositeDiv = $(this).siblings(".pick-box");
        oppositeDiv.toggleClass(function() {
            return oppositeDiv.is('.pick-box-unselected, .pick-box-selected') ? 'pick-box-unselected pick-box-selected' : 'pick-box-unselected';
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
                alert("Unable to save pick. The Onside Pick team has been notified. We apologize for the inconvenience.");
            } else {
                /*Update Game summary page with updated pick*/
                var gameRow = $('#' + gameId);
                var existingBet = gameRow.children('.pick').find('img');
                if (pick == null) {
                    /*Remove from game summary page if the bet currently exists*/
                    if (existingBet.length > 0) {
                        gameRow.children('.pick').find('img').remove();
                    }

                } else {

                    /*Check if bet already existed, add/change image and add/update betAmount*/
                    if (existingBet.length > 0) {
                        gameRow.children('.pick').find('img').attr('src', '/static/media/' + pick + '.png');
                    } else {
                        gameRow.children('.pick').append(`<img src="/static/media/` + pick + `.png" width="50" height="50">`);
                    }

                }
            }
        }
    });
}