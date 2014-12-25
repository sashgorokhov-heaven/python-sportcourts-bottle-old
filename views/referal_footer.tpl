<script src="/view/js/typed.js"></script>

<style>
  .clienthref{
    text-decoration: underline;
  }
</style>

<script>
  function inputfunc (item) {
    $(document).on('input','#'+item, function(){
      if($(this).val() != '') {
        var pattern = /^([a-z0-9_\.-])+@[a-z0-9-]+\.([a-z]{2,4}\.)?[a-z]{2,4}$/i;
        if(pattern.test($(this).val())){
            $(this).css({'border' : '1px solid #569b44'});
            $('#'+item+'button').removeAttr('disabled');
        } else {
            $(this).css({'border' : '1px solid #ff0000'});
            $('#'+item+'button').attr('disabled', 'disabled');
        }
      } else {
        $(this).css({'border' : '1px solid #ff0000'});
        $('#'+item+'button').attr('disabled', 'disabled');
      };
    });
  };

  function emailclient(item) {
    var arr = item.split('@');
    var client = arr[1];
    var result = [];
    switch (client) {
      case 'gmail.com':
        result[0] = 'Открыть Gmail';
        result[1] = 'https://mail.google.com/';
        break
      // case 'sportcourts.ru':
      //   result[0] = 'Открыть Gmail';
      //   result[1] = 'https://mail.google.com/';
      //   break
      case 'mail.ru':
        result[0] = 'Открыть Почту Mail.Ru';
        result[1] = 'https://e.mail.ru/';
        break
      case 'list.ru':
        result[0] = 'Открыть Почту Mail.Ru (list.ru)';
        result[1] = 'https://e.mail.ru/';
        break
      case 'inbox.ru':
        result[0] = 'Открыть Почту Mail.Ru (inbox.ru)';
        result[1] = 'https://e.mail.ru/';
        break
      case 'bk.ru':
        result[0] = 'Открыть Почту Mail.Ru (bk.ru)';
        result[1] = 'https://e.mail.ru/';
        break
      case 'yandex.ru':
        result[0] = 'Открыть Почту Yandex';
        result[1] = 'https://mail.yandex.ru/';
        break
      case 'ya.ru':
        result[0] = 'Открыть Почту Yandex';
        result[1] = 'https://mail.yandex.ru/';
        break
      case 'rambler.ru':
        result[0] = 'Открыть Почту Rambler';
        result[1] = 'https://mail.rambler.ru/';
        break
      case 'e1.ru':
        result[0] = 'Открыть Почту E1.ru';
        result[1] = 'https://mail.e1.ru/';
        break
      case 'icloud.com':
        result[0] = 'Открыть iCloud Mail';
        result[1] = 'https://www.icloud.com/';
        break
      case 'me.com':
        result[0] = 'Открыть iCloud Mail';
        result[1] = 'https://www.icloud.com/';
        break
      case 'yahoo.com':
        result[0] = 'Открыть Yahoo! Mail';
        result[1] = 'https://mail.yahoo.com/';
        break
      case 'live.ru':
        result[0] = 'Открыть Outlook.com (live.ru)';
        result[1] = 'https://mail.live.com/';
        break
      case 'live.com':
        result[0] = 'Открыть Outlook.com (live.com)';
        result[1] = 'https://mail.live.com/';
        break
      default:
        result[0] = 0;
        result[1] = 0;
    };
    return result;
  }

  function clickfunc (item) {
    $(document).on('click','#'+item+'button', function(){
      var email = $('#'+item).val();
      var user_client = emailclient(email);
      if (!pressed) {
        $.ajax({
          url: '/registration/email',
          data: {
            email: email
          },
          async: true,
          beforeSend: function() {
            pressed = true;
            $('#'+item+'button').attr('disabled', 'disabled');
            $('#'+item+'button').html('Отправка...');
            $('#'+item).attr('disabled', 'disabled');
          },
          success: function (data, textStatus) {
            if (data['error_code']==0) {
                $('#'+item+'button').html('Отправлено');
                if (user_client[0]!=0) {
                  $('#userclient').html('<p class="lead">Мы отправили вам письмо.<br>Пожалуйста, проверьте вашу почту</p><br><p class="lead" style="font-size:200%;"><a class="clienthref" href="'+user_client[1]+'" target="_blank">'+user_client[0]+'</a></p>')
                } else {
                  $('#userclient').html('<p class="lead">Сейчас на указанный Вами адрес <span class="text-primary">'+email+'</span> придет сообщение, содержащее ссылку для подтверждения email.<br><br>Пожалуйста, проверьте вашу почту.</p>');
                };
                $('#activateModal').modal('show');
            }
            if (data['error_code']==1) {
                alert('Ошибка, пользовтель с таким email уже зарегестрирован!')
                // в data['error_data'] лежит список [user_id, first_name, last_name] - типо "Вася Пупкин, eto ti?"
                pressed = false;
                $('#'+item+'button').removeAttr('disabled');
                $('#'+item+'button').html('Присоединиться');
                $('#'+item).removeAttr('disabled');
            }
            if (data['error_code']==2) {
                alert('Ошибка, пользовтель с таким email уже активирован!')
                // в data['error_data'] лежит список [email, token]
                pressed = false;
                $('#'+item+'button').removeAttr('disabled');
                $('#'+item+'button').html('Присоединиться');
                $('#'+item).removeAttr('disabled');
            }
            if (data['error_code']==3) {
                alert('Ошибка, пользовтель с таким email уже зарегестрирован!')
                // в data['error_data'] лежит список [email]
                pressed = false;
                $('#'+item+'button').removeAttr('disabled');
                $('#'+item+'button').html('Присоединиться');
                $('#'+item).removeAttr('disabled');
            }
          },
          error: function (response, status, errorThrown) {
            alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
            $('#'+item+'button').html('Ошибка');
          },
          type: "POST",
          dataType: "json"
        });
      }
    });
  };

  var pressed = false;

  $(document).ready(function() {
    inputfunc('email');
    inputfunc('email1');
    inputfunc('email3');
    clickfunc('email');
    clickfunc('email1');
    clickfunc('email3');
  });

  $(function(){
    $(".gamestyped").typed({
      strings: ["футбол", "баскетбол", "волейбол"],
      typeSpeed: 170,
      backDelay: 600,
      loop: true,
      loopCount: false
    });
  });


  $(document).on('click','#regbutton',function(){
    $('#reg1').fadeOut('slow', function() {
      $('#reg2').fadeIn('slow', function() {

      });
    });
  });

  $(document).on('click','#regbutton',function(){
    $('#reg3').fadeOut('slow', function() {
      $('#reg4').fadeIn('slow', function() {

      });
    });
  });
</script>

<style>
  #content{
    font-family: 'PF Agora Sans', Helvetica, Arial, sans-serif;
  }

  .referalheadrow{
    height:70vh;
    max-height:700px;
    min-height:500px;
  }

  .referalhead{
    position:absolute;
    top:0%;
    left:0%;
    z-index:30;
    width:100%;
    height: 70vh;
    max-height:700px;
    min-height:500px;
    color: rgb(255, 255, 255);
    text-shadow: rgba(0, 0, 0, 0.6) 0px 1px 2px;
  }

  .referalheaddark{
    margin:0 auto;
    width:100%;
    max-width: 1000px;
    height: 70vh;
    max-height:700px;
    min-height:500px;
    color: rgb(255, 255, 255);
    text-shadow: rgba(0, 0, 0, 0.6) 0px 1px 2px;
    background-color: rgba(0,0,0, 0.6);
  }

  .referal-avatar{
    border: 4px white solid;
  }

  .item-ref{
    background-color:black;
    height:70vh;
    max-height:700px;
    min-height:500px;
    overflow:hidden;
  }

  .item-ref img{
    min-height:100%;
    width:100%;
  }

  .promo-ul{
    font-size: 120%;
    margin-top: 30px;
  }

  .promo-li{
    margin-top: 10px;
  }

  .bigheadrow{
    height:100vh;
    min-height:700px;
    max-height:800px;
  }

  .bigheadrow-dark{
    background: #585350;
    color: white;
  }

  .item-ref{
    background-color:black;
    height:70vh;
    max-height:700px;
    min-height:500px;
    overflow:hidden;
  }

  .item-ref img{
    min-height:100%;
    width:100%;
  }

  .emailrow{
    height:100vh;
    max-height:800px;
    margin-bottom: -50px;
  }

  .emailhead{
    position:absolute;
    top:50%;
    left:15%;
    z-index:30;
    width:70%;
    max-height:800px;
    color: rgb(255, 255, 255);
    text-shadow: rgba(0, 0, 0, 0.6) 0px 1px 2px;
  }

  .page1head{
    position:absolute;
    top:50%;
    left:15%;
    z-index:30;
    width:70%;
    max-height:800px;
    color: rgb(255, 255, 255);
    text-shadow: rgba(0, 0, 0, 0.6) 0px 1px 2px;
  }

  .page2head{
    position:absolute;
    top:10%;
    left:15%;
    z-index:30;
    width:70%;
    max-height:800px;
    color: rgb(255, 255, 255);
    text-shadow: rgba(0, 0, 0, 0.6) 0px 1px 2px;
  }

  .item{
    background-color:black;
    height:100vh;
    max-height:800px;
    min-height: 600px;
    overflow:hidden;
  }

  .item img{
    min-height:100%;
    opacity:0.5;
  }

  .smallhead{
    padding-top:60px;
    padding-bottom: 0;
  }

  .indexpromo{
    padding-bottom: 30px;
  }

  #footer{
    background-color: rgb(20,20,20);
    height:61px;
  }

  #footerright{
    display:none;
  }

  #footerleft{
    float: none;
    text-align: center;
  }

  @media all and (max-width : 1000px) {
    .time{
      height: 250px;
    }
  }

  .img-row{
    height:100px;
    overflow: hidden;
    width:100%;
    text-align: center;
  }

  .referal-avatar{
    border: 4px white solid;
  }
</style>