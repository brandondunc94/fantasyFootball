$(".accept-button").click(function() {
    var leagueName = $('.league-title').html();
    var username = $(this).parent().siblings('.user-name').html();
    var addButtonObject = $(this);
    var rejectButton = $(this).siblings('.reject-button');
    $.ajax({
        url: '/league/addPrivate/',
        data: {
            'leagueName': leagueName,
            'username': username
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == "SUCCESS") {
                addButtonObject.prop("disabled", true);
                addButtonObject.prop('value', 'Added');
                rejectButton.hide();
            } else if (data.status == "PARTIAL") {
                addButtonObject.prop("disabled", true);
                addButtonObject.prop('value', 'Added');
                rejectButton.hide();
                alert("User has been added to the league, but the request could not be removed. This has been reported to the System Administrator.");
            } else {
                alert("Unable to add " + username + " to this league. Please try again or contact us if you are still experiencing issues.");
            }
        }
    });
});