/*When password fields are entered, check if it matches the other password
and that the length is at least 8 characters*/

$("#password").keyup(checkPasswordMatch);
$("#password2").keyup(checkPasswordMatch);

function checkPasswordMatch() {
    var password = $("#password").val();
    var confirmPassword = $("#password2").val();

    if (password.length < 8) {
        $("#divCheckPasswordMatch").removeClass('alert-success');
        $("#divCheckPasswordMatch").addClass('alert-danger');
        $('#divCheckPasswordMatch').html('Password must be at least 8 characters.');
        $('#submitButton').prop("disabled", true);
    } else if (password != confirmPassword) {
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