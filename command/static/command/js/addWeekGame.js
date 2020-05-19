/*Create new week*/
$("#addWeek").click(function() {
    var seasonYear = $('#season').attr('name');
    var weekType = $('#weekType').val();

    $.ajax({
        url: '/command/addWeek/',
        data: {
            'seasonYear': seasonYear,
            'weekType': weekType,
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == true) {
                alert("New week added successfully.");
            } else {
                alert("Unable to create week.");
            }
        }
    });
});

/*Create new game*/
$("#addGame").click(function() {
    var seasonYear = $('#season').attr('name');
    var weekId = $('#weekId').val();
    var homeTeam = $('#homeTeam').val();
    var awayTeam = $('#awayTeam').val();
    var location = $('#location').val();
    var gameDate = $('#gameDate').val();
    var gameTime = $('#gameTime').val();
    $.ajax({
        url: '/command/addGame/',
        data: {
            'seasonYear': seasonYear,
            'weekId': weekId,
            'homeTeam': homeTeam,
            'awayTeam': awayTeam,
            'location': location,
            'gameDate': gameDate,
            'gameTime': gameTime
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == true) {
                alert("New game created successfully.");
            } else {
                alert("Unable to create game.");
            }
        }
    });
});