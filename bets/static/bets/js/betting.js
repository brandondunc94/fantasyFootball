$( document ).ready(function() {
    calculatePointsAvailable();
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
    } 
    else {
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
    var totalUserPoints =  parseInt($('#totalPoints').html());
    var pointsAvailable = totalUserPoints;
    /*Sum up all points that have already been bet on other games*/
    $('.game-bet-amount').each(function( index ) {
        pointsAvailable -= (parseInt($(this).html()));
      });

    if(pointsAvailable >= 10){
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
    if (gameBetAmount > 0){
        gameBetAmount -= 10;
        gameBetAmountDisplay.html(gameBetAmount.toString());
        gameBetAmountDisplay.siblings('.game-bet-amount-input').val(gameBetAmount);

        calculatePointsAvailable();
    }
});

/*Calculate points available to bet*/
function calculatePointsAvailable(){
    /*Get total user points*/
    pointsAvailable = parseInt($('#totalPoints').html());

    /*Sum up all points that have already been bet on other games*/
    $('.game-bet-amount').each(function( index ) {
        pointsAvailable -= (parseInt($(this).html()));
      });
    
    /*Set display at top of page to reflect # of points available to bet*/
    $('#pointsToBet').html(pointsAvailable.toString());
}
