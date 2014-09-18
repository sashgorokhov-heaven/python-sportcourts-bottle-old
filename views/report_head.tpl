    <script>
      $(document).ready(function(){
        // счетчик новых пользователей
        var startFromNew = 0;
        // считаем, сколько юзеров уже в таблице
        var oldUsers = $('.user').size();

        $('#more').click(function() {

          var current = oldUsers+startFromNew+1;

          $("#userstable").append(
            "<tr class='newuser_" + (startFromNew+1) + "'><td>" + current + "</td><td><input type='text' class='form-control input-sm' name='first_name=-" + (startFromNew+1) + "' data-bv-notempty></td><td><input type='text' class='form-control input-sm' name='last_name=-" + (startFromNew+1) + "'></td><td><input id='phone' class='form-control input-sm phonemask' type='text' name='phone=-" + (startFromNew+1) + "'></td><td><select name='status=-" + (startFromNew+1) + "' class='form-control input-sm user_status'><option value='3'>Не пришел</option><option value='1'>Оплатил</option><option value='2'>Не оплатил</option></select></td><td align='center' valign='middle'><a class='removeuser'><span class='glyphicon glyphicon-remove'></span></a></td></tr>"
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

        var Amount = 0;
        var Price = {{game['cost']}};

        // var isArray = Array.isArray || function(obj) {
        //     return toString.call(obj) == '[object Array]';
        // };
        $('.container').on('change','.user_status',function(){

          var summ = 0;
          var summ1 = 0;

          var values = $.map($('.user_status'), function(element, i) {
            return $(element).val();
          });

          for(var i=0; i<values.length; i++) {
            if (values[i] == 1){
              summ += Price;
            }
            if (values[i] == 2){
              summ += Price;
              summ1 += Price;
            }
          }


          $('.amount').html('<p class="lead">Сумма к расчету: ' + summ + ' руб.</p>');
          $('.dolg_amount').html('<p class="lead">Клиенты должны вам: ' + summ1 + ' руб.</p>');
          $('.amount_input').val(summ);
        });
      });
    </script>