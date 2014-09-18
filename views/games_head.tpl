        <meta property="og:title" content="Таблица предстоящих игр" />
        <meta property="og:site_name" content="Site Name" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="http://{{serverinfo['ip']}}:{{serverinfo['port']}}"/>
        <meta property="og:image" content="/images/og/games.jpg" />
        <meta property="og:description" content="Здесь вы можете выбрать подходящую любительскую игру и принять в ней участие"/>

<script>

  $(document).on('click','.gamessearch',function(){

    var value = $('#sporttype').val();
    location.href='/games?sport_id='+value;

  });
</script>