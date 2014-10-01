<meta property="og:title" content="{{user['first_name']+' '+user['last_name']}}" />
<meta property="og:site_name" content="SportCourts.ru" />
<meta property="og:type" content="website" />
<meta property="og:url" content="http://{{serverinfo['ip']}}:{{serverinfo['port']}}"/users>
<meta property="og:image" content="/images/og/games.jpg" />
<meta property="og:description" content="профиль игрока на сайте sportcourts.ru"/>

<script>
  $(document).on('click','.friendsbutton',function(){
    arr = $(this).attr("id").split('-');
    var user_id = arr[1],
      action = arr[0];
    if (action == 'addfriend'){
      $.ajax({
        url: '/profile',
        data: {
          addfriend: user_id
        },
        type: "GET",
        dataType: "text",
        async: true,
        beforeSend: function() {
          inProgress = true;
        },
        success: function (responseData, textStatus) {
          $('#addfriend-'+user_id).html(' ');
          var count = $(".friendscount").html();
          count1 = parseInt(count);
          count1 += 1;
          $(".friendscount").html(count1);
          location.reload();
        },
        error: function (response, status, errorThrown) {
          alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
          inProgress = false;
        }
      });
    } else if (action == 'removefriend'){
      $.ajax({
        url: '/profile',
        data: {
          removefriend: user_id
        },
        type: "GET",
        dataType: "text",
        async: true,
        beforeSend: function() {
          inProgress = true;
        },
        success: function (responseData, textStatus) {
          $('#removefriend-'+user_id).html(' ');
          var count = $(".friendscount").html();
          count1 = count - 1;
          $(".friendscount").html(count1);
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