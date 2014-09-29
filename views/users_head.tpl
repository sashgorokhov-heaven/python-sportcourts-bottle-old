<meta property="og:title" content="Наши люди" />
<meta property="og:site_name" content="SportCourts.ru" />
<meta property="og:type" content="website" />
<meta property="og:url" content="http://{{serverinfo['ip']}}:{{serverinfo['port']}}"/users>
<meta property="og:image" content="/images/og/games.jpg" />
<meta property="og:description" content="Здесь вы можете найти своих друзей и всех, кто нас посещает."/>

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



  $(document).ready(function(){

    var inProgress = false;
    var step = 8;
    var startFromAll = step;
    var startFromFriends = step;


    $('#more').click(function() {
      if($('#panel-all').hasClass('active') == true)
      {
        var section = 'all';
        var startFrom = startFromAll;
      }
      else if($('#panel-friends').hasClass('active') == true)
      {
        return false;
      }

      $.ajax({
        url: '/users',
        data: {
          startfrom: startFrom,
          section: section
        },
        type: "POST",
        dataType: "text",
        async: true,
        beforeSend: function() {
          inProgress = true;
        },
        success: function (responseData, textStatus) {
          data = jQuery.parseJSON(responseData);
          if (data.length > 0) {
            $('#more').remove();
            $.each(data, function(index, data){
              if(section == 'all'){
                $('.user_cards_all').append(data+'<hr>');
              }
              // else if(section == 'friends'){
              //   $('.user_cards_friends').append(data+'<hr>');
              // }
            });
            $('.user_cards_all').append('<div id="more"><button type="button" class="btn btn-default btn-sm btn-block">Загрузить еще</button></div>');
            inProgress = false;
            if(section == 'all'){
              startFromAll += step;
            }
            // else if(section == 'friends'){
            //   startFromFriends += step;
            // }
          }
          else
          {
            $('#more').html('<button type="button" class="btn btn-link btn-sm btn-block" disabled>Все пользователи загружены</button>');
          }
        },
        error: function (response, status, errorThrown) {
          alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
          inProgress = false;
        }
      });
    });



    $(window).scroll(function() {

      if($(window).scrollTop() + $(window).height() >= $(document).height() - 40 && !inProgress) {

        if($('#panel-all').hasClass('active') == true)
        {
          var section = 'all';
          var startFrom = startFromAll;
        }
        else if($('#panel-friends').hasClass('active') == true)
        {
          return false;
        }

        $.ajax({
          url: '/users',
          data: {
            startfrom: startFrom,
            section: section
          },
          type: "POST",
          dataType: "text",
          async: true,
          beforeSend: function() {
            inProgress = true;
          },
          success: function (responseData, textStatus) {
            data = jQuery.parseJSON(responseData);
            if (data.length > 0) {
              $('#more').remove();
              $.each(data, function(index, data){
                if(section == 'all'){
                  $('.user_cards_all').append(data+'<hr>');
                }
                // else if(section == 'friends'){
                //   $('.user_cards_friends').append(data+'<hr>');
                // }
              });
              $('.user_cards_all').append('<div id="more"><button type="button" class="btn btn-default btn-sm btn-block">Загрузить еще</button></div>');
              inProgress = false;
              if(section == 'all'){
                startFromAll += step;
              }
              // else if(section == 'friends'){
              //   startFromFriends += step;
              // }
            }
            else
            {
              $('#more').html('<button type="button" class="btn btn-link btn-sm btn-block" disabled>Все пользователи загружены</button>');
            }
          },
          error: function (response, status, errorThrown) {
            alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
            inProgress = false;
          }
        });
      };
    });
  });
</script>