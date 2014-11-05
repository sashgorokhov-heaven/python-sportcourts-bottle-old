<meta property="og:title" content="SportCourts" />
<meta property="og:site_name" content="Site Name" />
<meta property="og:type" content="website" />
<meta property="og:url" content="http://{{serverinfo['ip']}}:{{serverinfo['port']}}"/>
<meta property="og:image" content="https://pp.vk.me/c620028/v620028278/1312a/jafmfIBHbVs.jpg" />
<meta property="og:description" content="Ваш проводник в мир любительского спорта. Огромная база спортивных событий для каждого! "/>

<script src="/view/js/typed.js"></script>

<script>
  var pressed = false;
  $(document).ready(function() {
      $(document).on('input','#email', function(){
        if($(this).val() != '') {
          var pattern = /^([a-z0-9_\.-])+@[a-z0-9-]+\.([a-z]{2,4}\.)?[a-z]{2,4}$/i;
          if(pattern.test($(this).val())){
              $(this).css({'border' : '1px solid #569b44'});
              $('#emailbutton').removeAttr('disabled');
          } else {
              $(this).css({'border' : '1px solid #ff0000'});
              $('#emailbutton').attr('disabled', 'disabled');
          }
        } else {
          $(this).css({'border' : '1px solid #ff0000'});
          $('#emailbutton').attr('disabled', 'disabled');
        };
      });
      $(document).on('input','#email1', function(){
        if($(this).val() != '') {
          var pattern = /^([a-z0-9_\.-])+@[a-z0-9-]+\.([a-z]{2,4}\.)?[a-z]{2,4}$/i;
          if(pattern.test($(this).val())){
              $(this).css({'border' : '1px solid #569b44'});
              $('#email1button').removeAttr('disabled');
          } else {
              $(this).css({'border' : '1px solid #ff0000'});
              $('#email1button').attr('disabled', 'disabled');
          }
        } else {
          $(this).css({'border' : '1px solid #ff0000'});
          $('#email1button').attr('disabled', 'disabled');
        };
      });
      $(document).on('input','#email3', function(){
        if($(this).val() != '') {
          var pattern = /^([a-z0-9_\.-])+@[a-z0-9-]+\.([a-z]{2,4}\.)?[a-z]{2,4}$/i;
          if(pattern.test($(this).val())){
              $(this).css({'border' : '1px solid #569b44'});
              $('#email3button').removeAttr('disabled');
          } else {
              $(this).css({'border' : '1px solid #ff0000'});
              $('#email3button').attr('disabled', 'disabled');
          }
        } else {
          $(this).css({'border' : '1px solid #ff0000'});
          $('#email3button').attr('disabled', 'disabled');
        };
      });
      $(document).on('click','#emailbutton', function(){
        var email = $('#email').val();
        if (!pressed) {
            $.ajax({
              url: '/registration/email',
              data: {
                email: email
              },
              async: true,
              beforeSend: function() {
                pressed = true;
                $('#emailbutton').attr('disabled', 'disabled');
                $('#emailbutton').html('Отправка...');
                $('#email').attr('disabled', 'disabled');
              },
              success: function (data, textStatus) {
                if (data['error_code']==0) {
                    $('#emailbutton').html('Отправлено');
                    $('#useremail').html(email);
                    $('#activateModal').modal('show');
                }
                if (data['error_code']==1) {
                    alert('Ошибка, пользовтель с таким email уже зарегестрирован!')
                    // в data['error_data'] лежит список [user_id, first_name, last_name] - типо "Вася Пупкин, eto ti?"
                    pressed = false;
                    $('#emailbutton').removeAttr('disabled');
                    $('#emailbutton').html('Присоединиться');
                    $('#email').removeAttr('disabled');
                }
                if (data['error_code']==2) {
                    alert('Ошибка, пользовтель с таким email уже активирован!')
                    // в data['error_data'] лежит список [email, token]
                    pressed = false;
                    $('#emailbutton').removeAttr('disabled');
                    $('#emailbutton').html('Присоединиться');
                    $('#email').removeAttr('disabled');
                }
                if (data['error_code']==3) {
                    alert('Ошибка, пользовтель с таким email уже зарегестрирован!')
                    // в data['error_data'] лежит список [email]
                    pressed = false;
                    $('#emailbutton').removeAttr('disabled');
                    $('#emailbutton').html('Присоединиться');
                    $('#email').removeAttr('disabled');
                }
              },
              error: function (response, status, errorThrown) {
                alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
                $('#emailbutton').html('Ошибка');
              },
              type: "POST",
              dataType: "json"
            });
        }
      });
      $(document).on('click','#email1button', function(){
        var email = $('#email1').val();
        if (!pressed) {
            $.ajax({
              url: '/registration/email',
              data: {
                email: email
              },
              async: true,
              beforeSend: function() {
                pressed = true;
                $('#email1button').attr('disabled', 'disabled');
                $('#email1button').html('Отправка...');
                $('#email1').attr('disabled', 'disabled');
              },
              success: function (data, textStatus) {
                if (data['error_code']==0) {
                    $('#email1button').html('Отправлено');
                    $('#useremail').html(email);
                    $('#activateModal').modal('show');
                }
                if (data['error_code']==1) {
                    alert('Ошибка, пользовтель с таким email уже зарегестрирован!')
                    // в data['error_data'] лежит список [user_id, first_name, last_name] - типо "Вася Пупкин, eto ti?"
                    pressed = false;
                    $('#email1button').removeAttr('disabled');
                    $('#email1button').html('Присоединиться');
                    $('#email1').removeAttr('disabled');
                }
                if (data['error_code']==2) {
                    alert('Ошибка, пользовтель с таким email уже активирован!')
                    // в data['error_data'] лежит список [email, token]
                    pressed = false;
                    $('#email1button').removeAttr('disabled');
                    $('#email1button').html('Присоединиться');
                    $('#email1').removeAttr('disabled');
                }
                if (data['error_code']==3) {
                    alert('Ошибка, пользовтель с таким email уже зарегестрирован!')
                    // в data['error_data'] лежит список [email]
                    pressed = false;
                    $('#email1button').removeAttr('disabled');
                    $('#email1button').html('Присоединиться');
                    $('#email1').removeAttr('disabled');
                }
              },
              error: function (response, status, errorThrown) {
                alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
                $('#email1button').html('Ошибка');
              },
              type: "POST",
              dataType: "json"
            });
        }
      });
      $(document).on('click','#email3button', function(){
        var email = $('#email3').val();
        if (!pressed) {
            $.ajax({
              url: '/registration/email',
              data: {
                email: email
              },
              async: true,
              beforeSend: function() {
                pressed = true;
                $('#email3button').attr('disabled', 'disabled');
                $('#email3button').html('Отправка...');
                $('#email3').attr('disabled', 'disabled');
              },
              success: function (data, textStatus) {
                if (data['error_code']==0) {
                    $('#email3button').html('Отправлено');
                    $('#useremail').html(email);
                    $('#activateModal').modal('show');
                }
                if (data['error_code']==1) {
                    alert('Ошибка, пользовтель с таким email уже зарегестрирован!')
                    // в data['error_data'] лежит список [user_id, first_name, last_name] - типо "Вася Пупкин, eto ti?"
                    pressed = false;
                    $('#email3button').removeAttr('disabled');
                    $('#email3button').html('Присоединиться');
                    $('#email3').removeAttr('disabled');
                }
                if (data['error_code']==2) {
                    alert('Ошибка, пользовтель с таким email уже активирован!')
                    // в data['error_data'] лежит список [email, token]
                    pressed = false;
                    $('#email3button').removeAttr('disabled');
                    $('#email3button').html('Присоединиться');
                    $('#email3').removeAttr('disabled');
                }
                if (data['error_code']==3) {
                    alert('Ошибка, пользовтель с таким email уже зарегестрирован!')
                    // в data['error_data'] лежит список [email]
                    pressed = false;
                    $('#emailbutton').removeAttr('disabled');
                    $('#emailbutton').html('Присоединиться');
                    $('#email').removeAttr('disabled');
                }
              },
              error: function (response, status, errorThrown) {
                alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
                $('#email3button').html('Ошибка');
              },
              type: "POST",
              dataType: "json"
            });
        }
      });
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
  ul{
    font-size: 120%;
    margin-top: 30px;
  }

  li{
    margin-top: 10px;
  }

  #content{
    font-family: 'PF Agora Sans', Helvetica, Arial, sans-serif;
  }

  .typed-cursor{
      opacity: 1;
      -webkit-animation: blink 0.7s infinite;
      -moz-animation: blink 0.7s infinite;
      animation: blink 0.7s infinite;
  }
  @keyframes blink{
      0% { opacity:1; }
      50% { opacity:0; }
      100% { opacity:1; }
  }
  @-webkit-keyframes blink{
      0% { opacity:1; }
      50% { opacity:0; }
      100% { opacity:1; }
  }
  @-moz-keyframes blink{
      0% { opacity:1; }
      50% { opacity:0; }
      100% { opacity:1; }
  }

  .bigheadrow{
    height:100vh;
    max-height:800px;
  }

  .bigheadrow-dark{
    background: #585350;
    color: white;
  }

  .bighead{
    position:absolute;
    top:{{'37' if loggedin else '20'}}%;
    left:15%;
    z-index:30;
    width:70%;
    max-height:800px;
    color: rgb(255, 255, 255);
    text-shadow: rgba(0, 0, 0, 0.6) 0px 1px 2px;
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
    top:70%;
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
    overflow:hidden;
  }

  .item img{
    min-height:100% !important;
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
</style>