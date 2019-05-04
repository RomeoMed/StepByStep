$(document).ready(function(){
    $('#user_email').focusout(function(){
        var user = $('#user_email').val();
        $.ajax({
            type: 'POST',
            url: '/check_new_user/' + user,
            success: function(response){
                if (response.exists) {
                    $('#user_email').addClass('error_highlight');
                    $('.exists').removeClass('hidden');
                    $('#register').attr('disabled', true);
                }
                else {
                    if ($('#user_email').hasClass('error_highlight')) {
                        $('#user_email').removeClass('error_highlight');
                    }
                    if (!$('.exists').hasClass('hidden')){
                        $('.exists').addClass('hidden');
                    }
                    if ($('#register').is(':disabled')) {
                        $('#register').removeAttr('disabled');
                    }
                }
            },
            error: function(xhr, textStatus, error){
                console.log(xhr.statusText);
                console.log(textStatus);
                console.log(error);
            }
        });
    });

    $('#security_form').submit(function(e){
        var question1 = $('#question1').val();
        var question2 = $('#question2').val();
        var question3 = $('#question3').val();

        if (question2 === question1 || question2 === question3 ) {
            e.preventDefault();
            $('#question2').addClass('error_highlight');
            if (question2 === question1) {
                $('#question1').addClass('error_highlight');
            }
            else {
                $('#question3').addClass('error_highlight');
            }
            $('#security_form .err').removeClass('hidden');
        }
        else if (question3 === question2 || question3 === question1) {
            e.preventDefault();
            $('#question3').addClass('error_highlight');
            if (question3 === question2) {
                $('#question2').addClass('error_highlight');
            }
            else {
                $('#question1').addClass('error_highlight');
            }
            $('#security_form .err').removeClass('hidden');
        }
    });

    $('#security_form select').change(function(){
        $('#security_form .err').addClass('hidden');
        $('#security_form select').each(function(){
            if ($(this).hasClass('error_highlight')){
                $(this).removeClass('error_highlight');
            }
        });
    });

    $('#reg_form').submit(function(e){
        var pwd = $('#password').val();
        var confirm = $('#confirm').val();
        if (pwd !== confirm){
            e.preventDefault();
            $('#password').addClass('error_highlight');
            $('#confirm').addClass('error_highlight');
             $('#reg_form .err').removeClass('hidden');
        }
    });

    $('#confirm').keyup(function(){
        if ($('#password').hasClass('error_highlight')) {
            $('#password').removeClass('error_highlight');
        }
        if ($('#confirm').hasClass('error_highlight')){
            $('#confirm').removeClass('error_highlight');
        }
        if (!('#reg_form .err').hasClass('hidden')){
            $('#reg_form .err').addClass('hidden');
        }
    });

    var clicked = '';
    $('.landing-btn').on('click', function(){
        clicked = $(this).attr('name');
    });
    $('#landing_form').one('submit', function(e) {
        e.preventDefault();
        $('#landing-input').val(clicked);
        $(this).submit();
    });

});

var action = function() {
    if( $('#username').val().length > 0 && $('#password').val().length > 0) {
        $('#submit').prop("disabled", false);
    } else {
        $('#submit').prop("disabled", true);
    }
}

var login_user = function(user, pass) {
    var data = { user: user, password: pass };
    $.ajax({
        type: 'POST',
        url: '/get_content',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response){
            //var url = response.redirect_tgt;
            //var token = response.access_token;
            //document.cookie='access_token=' + token;
            //window.location.href = url;
        },
        error: function(xhr, textStatus, error){
            console.log(xhr.statusText);
            console.log(textStatus);
            console.log(error);
        }
    });
}