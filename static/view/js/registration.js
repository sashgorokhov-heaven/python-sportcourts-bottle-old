var pressed = false;
$(document).ready(function() {
    $(document).on('input','#email2', function(){
      if($(this).val() != '') {
        var pattern = /^([a-z0-9_\.-])+@[a-z0-9-]+\.([a-z]{2,4}\.)?[a-z]{2,4}$/i;
        if(pattern.test($(this).val())){
            $(this).css({'border' : '1px solid #569b44'});
            $('#email2button').removeAttr('disabled');
        } else {
            $(this).css({'border' : '1px solid #ff0000'});
            $('#email2button').attr('disabled', 'disabled');
        }
      } else {
        $(this).css({'border' : '1px solid #ff0000'});
        $('#email2button').attr('disabled', 'disabled');
      };
    });
    $(document).on('click','#email2button', function(){
      var email = $('#email2').val();
      if (!pressed) {
          $.ajax({
            url: '/registration/email',
            data: {
              email: email
            },
            async: true,
            beforeSend: function() {
              pressed = true;
              $('#email2button').attr('disabled', 'disabled');
              $('#email2button').html('Отправка...');
              $('#email2').attr('disabled', 'disabled');
            },
            success: function (data, textStatus) {
              if (data['error_code']==0) {
                  $('#email2button').html('Отправлено');
                  $('#useremail').html(email);
                  $('#activateModal').modal('show');
              }
              if (data['error_code']==1) {
                  alert('Ошибка, пользовтель с таким email уже зарегестрирован!')
                  // в data['error_data'] лежит список [user_id, first_name, last_name] - типо "Вася Пупкин, eto ti?"
                  pressed = false;
                  $('#email2button').removeAttr('disabled');
                  $('#email2button').html('Присоединиться');
                  $('#email2').removeAttr('disabled');
              }
              if (data['error_code']==2) {
                  alert('Ошибка, пользовтель с таким email уже активирован!')
                  // в data['error_data'] лежит список [email, token]
                  pressed = false;
                  $('#email2button').removeAttr('disabled');
                  $('#email2button').html('Присоединиться');
                  $('#email2').removeAttr('disabled');
              }
              if (data['error_code']==3) {
                  alert('Ошибка, пользовтель с таким email уже зарегестрирован!')
                  // в data['error_data'] лежит список [email]
                  pressed = false;
                  $('#email2button').removeAttr('disabled');
                  $('#email2button').html('Присоединиться');
                  $('#email2').removeAttr('disabled');
              }
            },
            error: function (response, status, errorThrown) {
              alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
            },
            type: "POST",
            dataType: "json"
          });
      }
    });
});