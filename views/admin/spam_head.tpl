<script type="text/javascript">
  $(document).on('click', '#showbutton', function(){
    var tpl_id = $('#tpl_id').val();
    $.ajax({
      url: '',
      data: {
        tpl: tpl_id
      },
      async: true,
      success: function (responseData, textStatus) {
        $('#tpl_show').html('1');
        $('#showModal').modal('show');
      },
      error: function (response, status, errorThrown) {
        alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
      },
      type: "GET",
      dataType: "text"
    });
  });

  $(document).on('click', '#sendbutton', function(){
    var tpl_id = $('#tpl_id').val();
    var sport_id = $('#sporttype').val();
    $.ajax({
      url: '',
      data: {},
      async: true,
      success: function (responseData, textStatus) {
        alert('Успех!');
      },
      error: function (response, status, errorThrown) {
        alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
      },
      type: "GET",
      dataType: "text"
    });
  });
</script>