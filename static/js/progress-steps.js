setStep = function(step) {
    console.log(step);
    counter = 1
    if ($('#step_' + (step + counter)).hasClass('active')){
        while($('#step_' + (step + counter)).hasClass('active')) {
            $('#step_' + (step + counter)).removeClass('active');
            counter++;
        }
    }

    if (step > 1) {
        var counter = 1
        while (counter < step) {
            $('#step_' + (step - 1)).addClass('active');
        }
    }
    else if(step === 1) {
        $('#step_' + step).addClass('active');
    }
}

var advance = function(subtitle){
    var req = {
        'subtitle': subtitle,
        'content': $('#txt_setting').val(),
        'extra': $('#txt_char_intro').val(),
        'image': null
    }
    var json = JSON.stringify(req);
    $.ajax({
        type: "POST",
        contentType: 'application/json',
        url: "/get_next",
        dataType: "application/json;charset=utf-8",
        success: function(){},
        data: json,
        success:function(response){
            document.write(response);
        }
   });
}