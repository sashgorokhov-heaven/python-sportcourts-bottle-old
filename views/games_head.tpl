        <meta property="og:title" content="Таблица предстоящих игр" />
        <meta property="og:site_name" content="Site Name" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="http://{{serverinfo['ip']}}:{{serverinfo['port']}}"/>
        <meta property="og:image" content="/images/og/games.jpg" />
        <meta property="og:description" content="Здесь вы можете выбрать подходящую любительскую игру и принять в ней участие"/>

<script>

  $(document).on('click','.gamessearch',function(){

    var value = $('#sporttype').val();
    if (value == ''){
      location.href='/games';
    }
    else{
      location.href='/games?sport_id='+value;
    }

  });

  $(document).ready(function(){

    var inProgress = false;
    var step = 4;
    var startFromAll = step;

    $(window).scroll(function() {

      if($(window).scrollTop() + $(window).height() >= $(document).height() - 1 && !inProgress) {

        if($('#all').hasClass('active') == true)
        {
          var section = 'all';
          var startFrom = startFromAll;
        }
        else
        {
          return false;
        }

        alert('sdgd');

        $.ajax({
          url: '/games',
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
              $.each(data, function(index, data){
                if(section == 'all'){
                  $('.games_cards_all').append(data);
                }
                // else if(section == 'friends'){
                //   $('.user_cards_friends').append(data+'<hr>');
                // }
              });
              inProgress = false;
              if(section == 'all'){
                startFromAll += step;
              }
              // else if(section == 'friends'){
              //   startFromFriends += step;
              // }
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