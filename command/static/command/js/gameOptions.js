/*Lock selected game*/
$(".lock-button").click(function() {
    var seasonYear = $('#seasonId').attr('value');
    var week = $('#weekId').attr('value');
    var game = $(this).parent().siblings('.game-id').attr('value');
    var lockButtonObject = $(this)
    var unlockButtonObject = $(this).parent().siblings().children('.unlock-button')
    $.ajax({
        url: '/command/lock/',
        data: {
            'seasonYear': seasonYear,
            'week': week,
            'game': game
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == "SUCCESS") {
                /*Disabled lock button*/
                lockButtonObject.prop("disabled", true);
                lockButtonObject.prop('value', 'Locked');
                /*Enable unlock button*/
                unlockButtonObject.prop("disabled", false);
                unlockButtonObject.prop('value', 'Unlock');
            } else {
                alert("Unable to lock game.");
            }
        }
    });
});

/*Unlock selected game*/
$(".unlock-button").click(function() {
    var seasonYear = $('#seasonId').attr('value');
    var week = $('#weekId').attr('value');
    var game = $(this).parent().siblings('.game-id').attr('value');
    var unlockButtonObject = $(this)
    var lockButtonObject = $(this).parent().siblings().children('.lock-button')

    $.ajax({
        url: '/command/unlock/',
        data: {
            'seasonYear': seasonYear,
            'week': week,
            'game': game
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == "SUCCESS") {
                /*Disabled unlock button*/
                unlockButtonObject.prop("disabled", true);
                unlockButtonObject.prop('value', 'Unlocked');
                /*Enable lock button*/
                lockButtonObject.prop("disabled", false);
                lockButtonObject.prop('value', 'Lock');
            } else {
                alert("Unable to unlock game.");
            }
        }
    });
});

/*Save all game scores*/
$(".save-button").click(function() {
    var seasonYear = $('#seasonId').attr('value');
    var weekId = $('#weekId').attr('value');
    var statusFlag = false;
    /*var saveButtonObject = $(this);*/

    $(".score-input").each(function(index) {
        var homeScore = $(this).children().children().children('.home-score').val();
        var awayScore = $(this).children().children().children('.away-score').val();
        var gameId = $(this).children('.game-id').attr('value');
        if (homeScore != 'TBD') {
            $.ajax({
                url: '/command/save-score/',
                data: {
                    'season': seasonYear,
                    'weekId': weekId,
                    'gameId': gameId,
                    'homeScore': homeScore,
                    'awayScore': awayScore
                },
                dataType: 'json',
                success: function(data) {
                    if (data.status == "SUCCESS") {
                        statusFlag = true;
                    } else {

                    }
                }
            });
        }

    });
    if (statusFlag == true) {
        alert("All games saved successfully.");
    }

});