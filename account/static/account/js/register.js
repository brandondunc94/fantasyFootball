/*When passwords are entered, check if it matches the other password*/
$(document).ready(function() {
    $("#password1, #password2").keyup(checkPasswordMatch);
});

function checkPasswordMatch() {
    var password = $("#password").val();
    var confirmPassword = $("#password2").val();

    if (password != confirmPassword) {
        $("#divCheckPasswordMatch").removeClass('alert-success');
        $("#divCheckPasswordMatch").addClass('alert-danger');
        $('#divCheckPasswordMatch').html('Passwords do not match.');
        $('#submitButton').prop("disabled", true);
    } else {
        $("#divCheckPasswordMatch").removeClass('alert-danger');
        $("#divCheckPasswordMatch").addClass('alert-success');
        $('#divCheckPasswordMatch').html('Passwords match.');
        $('#submitButton').prop("disabled", false);
    }
}