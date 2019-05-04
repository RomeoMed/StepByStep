// Convert the report table to a datatable for a nicer look.
$(document).ready(function(){
    $('#report_table').DataTable();
});

// Function that handles cleaning up the submitted data, and prepping it to
// Post to the server.
$(document).ready(function(){
    $('.btnRegister').click(function() {
        var fname = '', lname = '', address1 = '',
            address2 = '', city = '', state = '', zip = '',
            country = '';
        fname = $('#first_name').val();
        lname = $('#last_name').val();
        address1 = $('#address1').val();
        address2 = $('#address2').val();
        city = $('#city').val();
        state = $('#state').val().toUpperCase();
        zip = $('#zip').val().replace(/\D/g, '');;
        country = $('#country').val().toUpperCase();
        regex = /^[A-Za-z]+$/;

        if (!fname.match(regex) && !lname.match(regex))
        {
            alert('Name fields contain invalid characters!');
            return false;
        }
        else if(address1.length == 0 && address2.length == 0)
        {
            alert('At least one address field must have input!');
            return false;
        }
        else if (!(state.match(regex)))
        {
            alert('State field contain invalid characters!');
            return false;
        }
        else if(!country.match(regex))
        {
            alert('Country field contains illegal characters!');
            return false;
        }
        else if(zip.lengh() > 9)
        {
            alert('Zip contains too many characters!');
            return false;
        }
        else{
            return true
        }

    });
});
