"use strict";



// $('#display-number').on('click', function (evt){
//     evt.preventDefault();
//     $.get('/display-number')
//     $('#display-number').text('Hide Number');

// });

// Set maximum number of characters to text per Twilio standard and
// output number of characters left for user
let maxLength = 1600;
$('#text-type').keyup(function (evt) {
  let textlength = maxLength - $(this).val().length;
  $('#chars-left').text(textlength);

});

// Get message from text area on team page to send
$(document).on('click', '#send-message', function (evt){
        evt.preventDefault();
        let message = $('#text-type').val();
        let formInputs = {'userMessage': message};

        // confirm sent message, reset the characters available, empty field
        $.post('/sms-send', formInputs, function (results){
            $('#text-type').val(null);
            console.log('nope');
            $('#chars-left').text(maxLength);

            alert(results.message);

        });
    });