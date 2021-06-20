$(document).ready(function() {

    //Use last accessed tab cookie to determine which tab is active
    var lastAccessedTab = getCookie('lastAccessedTab');
    if (lastAccessedTab) {
        $('#' + lastAccessedTab).addClass('active');
        $('#' + lastAccessedTab.replace('-tab', "")).addClass('active show');
    } else {
        $("#nav-games-tab").addClass('active');
        $("#nav-league").addClass('active show');
        setCookie('lastAccessedTab', 'nav-games-tab');
    }

    //Auto scroll to botton of message board
    $(".message-board").animate({
        scrollTop: $('.message-board')[0].scrollHeight - $('.message-board')[0].clientHeight
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

/*Save last accessed page*/
$(".dashboard-menu-item").click(function() {
    setCookie('lastAccessedTab', $(this).attr('id'));
});


/*Post message to league message board*/
$(".post-button").click(function() {
    var leagueName = $('#leagueName').html();
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
                if (data.status == 'SUCCESS') {}
            }
        });
    }

});

/*Collapse column logic*/
$(".collapse-col").click(function() {

    //getting the next element
    cardContent = $(this).next('div');
    $(this).next('div').toggleClass('max-height-650');
    $(this).find('i').toggleClass('arrow-down');
    //open up the content needed - toggle the slide- if visible, slide up, if not slidedown.
    cardContent.slideToggle(0, function() {
        //execute this after slideToggle is done
    });

});

function setCookie(cname, cvalue) {
    document.cookie = cname + "=" + cvalue + ";";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}