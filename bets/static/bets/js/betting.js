$(document).ready(function() {
    updatePointsAvailable(calculatePointsAvailable());
});

/*Save Bets*/
$("#saveBets").click(function() {
    var status = true;
    var leagueName = $('#leagueName').attr('name');
    var weekId = $('#weekId').attr('name');

    /*For each game, save current bet to database via ajax call*/
    $('.bet-game').each(function(index) {
        var currentBet = $(this);
        var pick = $(this).children('.bet-box-selected').find('input').val();
        var betAmount = $(this).find('.bet-amount-input').val();
        var gameId = $(this).children('.bet-box').find('input').attr('name');
        if (pick == undefined & betAmount != "") {
            $.notify("Please make sure you have made a spread selection before betting points.", "error");
        } else(
            $.ajax({
                url: '/bets/save/',
                data: {
                    'leagueName': leagueName,
                    'weekId': weekId,
                    'gameId': gameId,
                    'pick': pick,
                    'betAmount': betAmount
                },
                dataType: 'json',
                success: function(data) {
                    if (data.status == false) {
                        status = false;
                    } else {
                        /*Get new values, get game id and new bet amount*/
                        var gameRow = $('#' + gameId);
                        var betSpread = currentBet.children('.bet-box-selected').find('h6').html();

                        /*Update game summary page*/
                        var existingBet = gameRow.children('.bet').find('img');

                        if (pick == null) {
                            /*Remove from game summary page if the bet currently exists*/
                            if (existingBet.length > 0) {
                                gameRow.children('.bet').find('img').remove();
                                gameRow.children('.bet').find('h6').html('');
                            }

                        } else {
                            /*Check if bet already existed, add/change image and add/update betAmount*/
                            if (existingBet.length > 0) {
                                gameRow.children('.bet').find('img').attr('src', '/static/media/' + pick + '.png');
                                gameRow.children('.bet').find('h6').html('(' + betSpread + ') $' + betAmount);
                            } else {
                                gameRow.children('.bet').append(`<img class=\"\" src=\"/static/media/` + pick + `.png\" width=\"50\" height=\"50\"> <h6>(` + betSpread + `) $` + betAmount + `</h6>`);
                            }

                        }

                    }
                }
            }));
    });
    if (status == true) {
        $.notify("Bets saved successfully", "success");
    } else {
        $.notify("Unable to save bets. Please try again later.", "error");
    }

});

/*Select a team box to make bets*/
$(".bet-box").click(function() {
    if ($(this).hasClass('bet-box-selected')) {
        /*Unselect the currently selected box and unselect radio button*/
        $(this).removeClass('bet-box-selected')
        var radioButton = $(this).find("input");
        radioButton.attr('checked', false);

        /*Select opposite div and radio button to mark as untouched bet box*/
        var oppositeDiv = $(this).siblings('.bet-box');
        oppositeDiv.removeClass('bet-box-unselected')

        /*Set bet amount to 0*/
        $(this).siblings().children('.bet-amount-input').prop('disabled', true).val('').attr('placeholder', 'Bet Amount');

        updatePointsAvailable(calculatePointsAvailable());
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

        /*Enable input box*/
        $(this).siblings().children('.bet-amount-input').prop('disabled', false);
        updatePointsAvailable(calculatePointsAvailable());
    }
});

var timer = null;
$('.bet-amount-input').keyup(function() {
    clearTimeout(timer);
    timer = setTimeout(checkBetAmount, 750)
});

function checkBetAmount() {
    var betAmount = $(this);
    var leftOverPointsAvailable = calculatePointsAvailable();

    if (leftOverPointsAvailable >= 0) {
        $('#saveBets').prop('disabled', false);
    } else {
        /*User is trying to bet too many points, disabled save button and all input boxes with red border*/
        $.notify("Bet amount is too high.", "error");
        leftOverPointsAvailable = calculatePointsAvailable();
        $('#saveBets').prop('disabled', true);
    }
    updatePointsAvailable(leftOverPointsAvailable);
}

/*Calculate points available to bet*/
function calculatePointsAvailable() {
    /*Get total user points*/
    var pointsAvailableTotal = parseInt($('#totalPoints').html());

    /*Sum up all points that have already been bet on other games*/
    $('.bet-amount-input').each(function(index) {
        if ($(this).val() != "") {
            pointsAvailableTotal -= (parseInt($(this).val()));
        }
    });
    return pointsAvailableTotal;
}

function updatePointsAvailable(pointsAvailable) {
    $('#pointsToBet').html(pointsAvailable.toString());
}