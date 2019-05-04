$(document).ready(function(){
    $.ajax({
        type: 'POST',
        url: '/get_content',
        success: function(response){
            var title = response.title;
            var subtitle = response.subtitle;
            var section = response.section_name;
            var body = response.body;
            var step = response.step;
            var section_num = response.section
            $('#main_title').html(title);
            $('#sub_title').html(subtitle);
            $('#input2').html('Additional Description');
            $('#inst_subtitle').html(subtitle);
            $('#inst_section').html(section);
            $('#main_txt').html(body)

            if (step > 1) {
                while (step >= 1) {
                    var newStep = '#step_' + step
                    $(newStep).addClass('active');
                    step--;
                }
            }
        },
        error: function(xhr, textStatus, error){
            console.log(xhr.statusText);
            console.log(textStatus);
            console.log(error);
        }
    });

    $('#next').click(function(){
        advanceStep();
    });
});

var advanceStep = function(){
    var text = $('#txt_setting').text();
    var details = $('#txt_details').text();

    $.ajax({
        type: 'POST',
        url: '/advance_next',
        success: function(response){
            var title = response.title;
            var subtitle = response.subtitle;
            var section = response.section_name;
            var body = response.body;
            var step = response.step;
            var section_num = response.section
            $('#main_title').html(title);
            $('#sub_title').html(subtitle);
            $('#input2').html('Additional Description');
            $('#inst_subtitle').html(subtitle);
            $('#inst_section').html(section);
            $('#main_txt').html(body)

            if (step > 1) {
                while (step >= 1) {
                    var newStep = '#step_' + step
                    $(newStep).addClass('active');
                    step--;
                }
            }
        },
        error: function(xhr, textStatus, error){
            console.log(xhr.statusText);
            console.log(textStatus);
            console.log(error);
        }
    });
}