"use strict";



// $('#display-number').on('click', function (evt){
//     evt.preventDefault();

// });

// Set maximum number of characters to text per Twilio standard and
// output number of characters left for user
// let maxLength = 1600;
// $('#text-type').keyup(function (evt) {
//   let textlength = maxLength - $(this).val().length;
//   $('#chars-left').text(textlength);


// });
// Get message from text area on team page to send

$('#send-msg').on('submit', function (evt){
        evt.preventDefault();
        let message = $('#text-type').val();
        console.log(message);
        let formInputs = {'userMessage': message};

        $.post('/sms-send', formInputs, function (results){
            alert(results.message);

        });
    });