$(document).ready(function(){
    $('#next').click(function(){
        var form = $('#content-post');
        $(form).attr('action', '/advance');
        $(form).submit();
    });
    $('#previous').click(function(){
        var form = $('#content-post');
        $(form).attr('action', '/go_back');
        $(form).submit();
    });
});