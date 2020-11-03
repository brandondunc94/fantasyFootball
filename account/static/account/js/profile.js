/*Edit Profile */
$("#edit-button").click(function() {
    $("#firstName").attr("readonly", false);
    $("#lastName").attr("readonly", false);
    $("#email").attr("readonly", false);
    $("#favoriteTeam").attr("disabled", false);

    $(this).attr('style', 'display:none;');
    $("#save-button").attr("style", "");
});

/*Save Profile*/
$("#save-button").click(function() {

    var updatedFirstName = $("#firstName").val();
    var updatedLastName = $("#lastName").val();
    var updatedEmail = $("#email").val();
    var updatedFavTeam = $("#favoriteTeam").val();

    $.ajax({
        url: '/account/update/',
        data: {
            'firstName': updatedFirstName,
            'lastName': updatedLastName,
            'email': updatedEmail,
            'favoriteTeam': updatedFavTeam,
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == "SUCCESS") {

            } else {
                alert("Unable to save profile. Please try again later.");
            }
        }
    });

    $("#firstName").attr("readonly", true);
    $("#lastName").attr("readonly", true);
    $("#email").attr("readonly", true);
    $("#favoriteTeam").attr("disabled", true);
    $("#favTeamImage").attr("src", "/static/media/" + updatedFavTeam + ".png");

    $(this).attr('style', 'display:none;');
    $("#edit-button").attr("style", "");
});