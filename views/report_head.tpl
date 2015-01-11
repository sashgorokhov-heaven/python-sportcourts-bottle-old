<meta name="robots" content="noindex"/>

<link rel="stylesheet" href="/view/jasny/css/jasny-bootstrap.css">
<script src="/view/jasny/js/jasny-bootstrap.js"></script>

% if ask_autocreate:
<script>
  $(document).ready(function() {
    $('#nextGameModal').modal('show');
  });
</script>
% end 

<script>
  function writeamount (summ,summ1) {
    $('.amount').html('<p class="lead">Сумма к расчету: ' + summ + ' руб.</p>');
    $('.dolg_amount').html('<p class="lead">Клиенты должны вам: ' + summ1 + ' руб.</p>');
    $('.amount_input').val(summ);
  };

  function calculate () {
    var Price = {{game.cost()}};
    var summ = 0;
    var summ1 = 0;

    var values = $.map($('.user_status'), function(element, i) {
      return $(element).val();
    });

    var values1 = $.map($('.amountss'), function(element, i) {
      return $(element).val();
    });

    for(var i=0; i<values.length; i++) {
      if (values[i] == 2){
        summ += Price;
      }
      if (values[i] == 1){
        summ += Price;
        summ1 += Price;
      }
    }

    for(var i=0; i<values1.length; i++) {
      summ -= parseInt(values1[i],10);
    }
    writeamount(summ,summ1);
  };

  $(document).ready(function(){
    // счетчик новых пользователей
    var startFromNew = 0;
    // счетчик затрат
    var startFromCharges = 0;
    // считаем, сколько юзеров уже в таблице
    var oldUsers = $('.user').size();

    $('#more').click(function() {

      var current = oldUsers+startFromNew+1;

      $("#userstable").append(
        "<tr class='newuser_" + (startFromNew+1) + "'><td>" + current + "</td><td><input type='text' class='form-control input-sm' name='first_name=-" + (startFromNew+1) + "' data-bv-notempty></td><td><input type='text' class='form-control input-sm' name='last_name=-" + (startFromNew+1) + "'></td><td><input id='phone' class='form-control input-sm phonemask' type='text' name='phone=-" + (startFromNew+1) + "'></td><td><select name='status=-" + (startFromNew+1) + "' class='form-control input-sm user_status'><option value='0'>Не пришел</option><option value='1'>Не оплатил</option><option value='2'>Оплатил</option></select></td><td align='center' valign='middle'><a class='removeuser'><span class='glyphicon glyphicon-remove'></span></a></td><td>" + (Price) + "</td></tr>"
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

    $('#morecharge').click(function() {

      var currentcharge = startFromCharges+1;

      $("#chargestable").append(
        "<tr class='charge_" + (startFromCharges+1) + "'><td>" + currentcharge + "</td><td><input type='text' class='form-control input-sm' name='description=-" + (startFromCharges+1) + "' data-bv-notempty></td><td><input type='text' class='form-control input-sm amountss' name='amount-" + (startFromCharges+1) + "'></td><td align='center' valign='middle'><a class='removecharge'><span class='glyphicon glyphicon-remove'></span></a></td></tr>"
      );

      $('.removecharge').click(function() {
        $(this).parent().parent().remove();
      });

      startFromCharges += 1;
    });

    var Amount = 0;
    var Price = {{game.cost()}};

    $('.container').on('change','.user_status',function(){
      calculate();
      $('#reportForm').bootstrapValidator();
    });

    $('.container').on('input','.amountss',function(){
      calculate();
    });
  });
</script>