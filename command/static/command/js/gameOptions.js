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

                $.notify("Unable to lock game.", "error");
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
                $.notify("Unable to unlock game", "error");
            }
        }
    });
});

/*Save all game scores*/
$(".save-button").click(function() {
    var statusFlag = true;

    $(".score-input").each(function(index) {
        var homeScore = $(this).children().children('.home-score').val();
        var homeSpread = $(this).children().children('.home-spread').val();
        var awayScore = $(this).children().children('.away-score').val();
        var awaySpread = $(this).children().children('.away-spread').val();
        var gameId = $(this).children('.game-id').attr('value');
        $.ajax({
            url: '/command/saveScoreSpread/',
            data: {
                'gameId': gameId,
                'homeScore': homeScore,
                'homeSpread': homeSpread,
                'awayScore': awayScore,
                'awaySpread': awaySpread
            },
            dataType: 'json',
            success: function(data) {
                if (data.status == "FAILED") {
                    statusFlag = false;
                } else {

                }
            }
        });
    });

    if (statusFlag == true) {
        $.notify("All game scores and spreads saved successfully.", "success");
    } else {
        $.notify("Unable to save all game scores.", "error");
    }

});

/*Delete selected game*/
$(".delete-button").click(function() {
    var seasonYear = $('#seasonId').attr('value');
    var weekId = $('#weekId').attr('value');
    var gameId = $(this).parent().siblings('.game-id').attr('value');

    $.ajax({
        url: '/command/deleteGame/',
        data: {
            'seasonYear': seasonYear,
            'weekId': weekId,
            'gameId': gameId
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == true) {
                $.notify("Game deleted successfully.", "success");
            } else {
                $.notify("Unable to delete game.", "error");
            }
        }
    });
});

/*Activate current week to be the default*/
$(".activate-week-button").click(function() {
    var seasonYear = $('#seasonId').attr('value');
    var weekId = $('#weekId').attr('value');
    $.ajax({
        url: '/command/activateWeek/',
        data: {
            'season': seasonYear,
            'week': weekId,
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == "FAILED") {
                $.notify("Unable to activate week", "error");
            } else {
                $.notify("Week " + weekId + " has been activated.", "success");
            }
        }
    });
});

/*Go retrieve upcoming schedule for current week*/
$("#get-week-schedule-button").click(function() {
    var seasonYear = $('#seasonId').attr('value');
    var weekId = $('#weekId').attr('value');
    $.ajax({
        url: '/command/getWeekSchedule/',
        data: {
            'season': seasonYear,
            'week': weekId,
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == "FAILED") {
                $.notify("Unable to retrieve or save upcoming games", "error");
            } else {
                $.notify("Upcoming games added/updated. Please refresh the page.", "success");
            }
        }
    });
});

/*Go get latest live scores*/
$("#get-live-scores-button").click(function() {
    $.ajax({
        url: '/command/getLatestScores/',
        data: {},
        dataType: 'json',
        success: function(data) {
            if (data.status == "FAILED") {
                $.notify("Unable to get latest scores.", "error");
            } else {
                $.notify("Latest scores have been updated.", "success");
            }
        }
    });
});

/*Go get latest live scores*/
$("#get-final-scores-button").click(function() {
    $.ajax({
        url: '/command/getFinalScores/',
        data: {},
        dataType: 'json',
        success: function(data) {
            if (data.status == "FAILED") {
                $.notify("Unable to get latest scores.", "error");
            } else {
                $.notify("Final scores have been updated and games have been scored.", "success");
            }
        }
    });
});