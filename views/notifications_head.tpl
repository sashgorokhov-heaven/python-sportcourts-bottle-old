<script type="text/javascript">
  $(document).on('click', 'button', function() {
    n_id = $(this).attr("id");
    $.ajax({
      url: 'http://sportcourts.ru/notifications',
      data: {
        id: n_id
      },
      async: true,
      success: function (responseData, textStatus) {
        // alert(responseData + ' Status: ' + textStatus);
        alert('Вы прочитали эту заметку');
        // document.location.href = 'http://sportcourts.ru/games#game' + game_id;
        window.location.reload();
      },
      error: function (response, status, errorThrown) {
        alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
      },
      type: "POST",
      dataType: "text"
    });
  });
</script>