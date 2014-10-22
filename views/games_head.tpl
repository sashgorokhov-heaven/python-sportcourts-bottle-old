<meta property="og:title" content="Таблица предстоящих игр" />
<meta property="og:site_name" content="Site Name" />
<meta property="og:type" content="website" />
<meta property="og:url" content="http://{{serverinfo['ip']}}:{{serverinfo['port']}}"/>
<meta property="og:image" content="/images/og/games_basketball.jpg" />
<meta property="og:description" content="Здесь вы можете выбрать подходящую игру и принять в ней участие"/>


<script>

  $(document).on('change','#sporttype',function(){

    var value = $('#sporttype').val();
    if (value == '0'){
      location.href='/games';
    }
    if (value == '-1'){
      location.href='/games?old';
    }
    if (value != '0' && value != '-1') {
      location.href='/games?sport_id='+value;
    }

  });

  $(document).ready(function(){

    var inProgress = false;
    var page = 2;
    var stop = false;

    $(window).scroll(function() {

      if($(window).scrollTop() + $(window).height() >= $(document).height() - 200 && !inProgress && !stop && $('#all').hasClass('active')) {

        $.ajax({
          url: '/games',
          data: {
            page: page {{', sport_id: '+str(bysport) if bysport else ''}}{{', old: 1' if old else ''}}
          },
          type: "GET",
          dataType: "json",
          async: true,
          beforeSend: function() {
            inProgress = true;
          },
          success: function (data, textStatus) {
            if (data["stop"]) {
              stop = true;
              // alert('stop');
            }
            if (data["games"].length > 0) {
              $.each(data["games"], function(index, data){
                $('.games_cards_all').append(data);
              });
              inProgress = false;
              page++;
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