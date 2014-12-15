<script type="text/javascript">
  $(document).on('click', '#sendbutton', function(){
    var group_id = $('#group_id').val();
    var sport_id = $('#sporttype').val();
    if($("#city").is(":checked")){ 
      var city = 1;
    } else {
      var city = 0;
    };
    if($("#msg").is(":checked")){ 
      var msg = 1;
    } else {
      var msg = 0;
    };
    $.ajax({
      url: '',
      data: {

      },
      async: true,
      success: function (responseData, textStatus) {
        $('#group_name').html('1');
        $('#group_count').html('1');
        $('#group_count1').html('1');
        $('#group_male').html('1');
        $('#group_female').html('1');
        $('#resultModal').modal('show');
      },
      error: function (response, status, errorThrown) {
        alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
      },
      type: "GET",
      dataType: "text"
    });
  });

  $(document).on('click', '#addbutton', function(){
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