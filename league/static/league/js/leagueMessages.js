$(document).ready(function() {
    /*Auto scroll to botton of message board*/
    $(".message-board").animate({
        scrollBottom: $('.message-board')[0].scrollHeight - $('.message-board')[0].clientHeight
    }, 1000);

    // Get the input field
    var input = document.getElementById('messageBox');

    // Execute a function when the user releases a key on the keyboard
    input.addEventListener("keyup", function(event) {
        // Number 13 is the "Enter" key on the keyboard
        if (event.keyCode === 13) {
            // Cancel the default action, if needed
            event.preventDefault();
            // Trigger the button element with a click
            $(".post-button").click();
        }
    });
});

/*Try to post message when enter key is hit*/
$("#messageBox").keypress(function(event) {
    if (event.keyCode === 13) {
        $(".post-button").click();
    }
});

/*Post message to league message board*/
$(".post-button").click(function() {
    var leagueName = $('#leagueName').attr('name');
    var message = $('#messageBox').val();
    var csrftoken = $.cookie('csrftoken');
    if (message) {
        $.ajax({
            headers: { 'X-CSRFToken': csrftoken },
            url: '/league/post/',
            data: {
                'leagueName': leagueName,
                'message': message,
            },
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                if (data.status == 'SUCCESS') {
                    /*Append message to message board*/
                    var username = $('.username-nav').html().replace("Welcome, ", "");
                    var newMessage = `
                                    <div class='media text-muted pt-3'>
                                    <p class='media-body pb-3 mb-0 small lh-125 border-bottom border-gray'><strong class='d-block text-gray-dark'>@` + username + `</strong>` + message + `</p>
                                    </div>`
                    $('.messages-div').append(newMessage);
                    $('#messageBox').val("");
                    $('.message-board').scrollTop($('.message-board')[0].scrollHeight - $('.message-board')[0].clientHeight);
                }
            }
        });
    }

});