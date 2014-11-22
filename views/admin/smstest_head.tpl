<script>

  function initusertable (res, item) {
    $('#userssearchtable').html(' ');

    var l = res.length;
    if (l > 30) {
      l = 30;
    }


  $(document).on('click','#contactsload',function(){
    $.ajax({
      url: 'https://lcab.sms-uslugi.ru/lcabApi/getContacts.php',
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
  });

</script>