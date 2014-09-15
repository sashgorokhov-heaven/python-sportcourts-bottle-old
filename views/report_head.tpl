    <script>
      $(document).ready(function(){
        // счетчик новых пользователей
        var startFromNew = 0;
        // считаем, сколько юзеров уже в таблице
        var oldUsers = $('.user').size();

        $('#more').click(function() {

          var current = oldUsers+startFromNew+1;

          $("#userstable").append(
            "<tr class='newuser_" + (startFromNew+1) + "'><td>" + current + "</td><td><input type='text' class='form-control input-sm' name='first_name=-" + (startFromNew+1) + "' data-bv-notempty></td><td><input type='text' class='form-control input-sm' name='last_name=-" + (startFromNew+1) + "'></td><td><input id='phone' class='form-control input-sm phonemask' type='text' name='phone=-" + (startFromNew+1) + "'></td><td><select name='status=-" + (startFromNew+1) + "' class='form-control input-sm user_status'><option value='0'></option><option value='1'>Оплатил</option><option value='2'>Не оплатил</option><option value='3'>Не пришел</option></select></td><td align='center' valign='middle'><a class='removeuser'><span class='glyphicon glyphicon-remove'></span></a></td></tr>"
          );

          $('.phonemask').inputmask({
            mask: '+7 (999) 999 99 99'
          });
          $('#phone').tooltip();

          $('.removeuser').click(function() {
            $(this).parent().parent().remove();
          });

          startFromNew += 1;

        });
      });
    </script>