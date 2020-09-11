$(document).ready(function() {
    calculatePointsAvailable();
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
        var betAmount = $(this).find('.game-bet-amount').html();
        var gameId = $(this).children('.bet-box').find('input').attr('name');
        if (pick == undefined) {
            pick = null;
        }

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
        });


    });
    if (status == true) {
        alert("Bets saved successfully.");
    } else {
        alert("Unable to save bets. The Onside Pick team has been notified. We apologize for the inconvenience.");
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

        /*Disable +/- buttons and set bet amount to 0*/
        $(this).siblings().children('.increase-bet-button').prop('disabled', true);
        $(this).siblings().children('.decrease-bet-button').prop('disabled', true);
        $(this).siblings().children('.game-bet-amount').html('0').val('0');
        calculatePointsAvailable();
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

        /*Enable +/- buttons*/
        $(this).siblings().children('.increase-bet-button').prop('disabled', false);
        $(this).siblings().children('.decrease-bet-button').prop('disabled', false);
    }
});

/*Increase bet amount*/
$(".increase-bet-button").click(function() {
    /*Get total points available to bet*/
    var pointsAvailable = parseInt($('#totalPoints').html());

    /*Sum up all points that have already been bet on other games*/
    $('.game-bet-amount').each(function(index) {
        pointsAvailable -= (parseInt($(this).html()));
    });

    if (pointsAvailable >= 10) {
        /*Add 10 points to current game bet*/
        var gameBetAmountDisplay = $(this).siblings('.game-bet-amount');
        var gameBetAmount = parseInt(gameBetAmountDisplay.html());
        gameBetAmount += 10;
        gameBetAmountDisplay.html(gameBetAmount.toString());
        gameBetAmountDisplay.siblings('.game-bet-amount-input').val(gameBetAmount);

        calculatePointsAvailable();
    }
});

/*Decrease bet amount*/
$(".decrease-bet-button").click(function() {
    /*Decrease 10 points to current game bet*/
    var gameBetAmountDisplay = $(this).siblings('.game-bet-amount');
    var gameBetAmount = parseInt(gameBetAmountDisplay.html());
    if (gameBetAmount > 0) {
        gameBetAmount -= 10;
        gameBetAmountDisplay.html(gameBetAmount.toString());
        gameBetAmountDisplay.siblings('.game-bet-amount-input').val(gameBetAmount);

        calculatePointsAvailable();
    }
});

/*Calculate points available to bet*/
function calculatePointsAvailable() {
    /*Get total user points*/
    var pointsAvailable = parseInt($('#totalPoints').html());

    /*Sum up all points that have already been bet on other games*/
    $('.game-bet-amount').each(function(index) {
        if ($(this).html() != undefined) {
            pointsAvailable -= (parseInt($(this).html()));
        }
    });

    /*Set display at top of page to reflect # of points available to bet*/
    $('#pointsToBet').html(pointsAvailable.toString());
}