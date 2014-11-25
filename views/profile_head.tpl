<meta property="og:title" content="{{user.name}}" />
<meta property="og:site_name" content="SportCourts.ru" />
<meta property="og:type" content="website" />
<meta property="og:url" content="http://{{serverinfo['ip']}}:{{serverinfo['port']}}/profile/{{user.user_id()}}">
<meta property="og:image" content="/images/og/games.jpg" />
<meta property="og:description" content="профиль игрока на сайте sportcourts.ru"/>

<script>
  $(document).on('click','.friendsbutton',function(){
    arr = $(this).attr("id").split('-');
    var user_id = arr[1],
      action = arr[0];
    if (action == 'addfriend'){
      $.ajax({
        url: '/profile/addfriend/{{user.user_id()}}',
        data: {},
        type: "GET",
        dataType: "text",
        async: true,
        beforeSend: function() {
          inProgress = true;
        },
        success: function (responseData, textStatus) {
          location.reload();
        },
        error: function (response, status, errorThrown) {
          alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
          inProgress = false;
        }
      });
    } else if (action == 'removefriend'){
      $.ajax({
        url: '/profile/addfriend/{{user.user_id()}}',
        data: {},
        type: "GET",
        dataType: "text",
        async: true,
        beforeSend: function() {
          inProgress = true;
        },
        success: function (responseData, textStatus) {
          location.reload();
        },
        error: function (response, status, errorThrown) {
          alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
          inProgress = false;
        }
      });
    };
      
  });
</script>