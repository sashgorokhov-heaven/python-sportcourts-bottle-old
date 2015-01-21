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

  $( document ).ready(function() {
    $('#adminModal').modal('show');
  });

  $(document).on('click', '#loginAdmins', function(){
    var url = '/admin/bad_vk/auth';
    $.ajax({
      url: url,
      async: true,
      success: function (responseData, textStatus) {
        alert('Залогинен!\n' + responseData);
      },
      error: function (response, status, errorThrown) {
        alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
      },
      type: "GET",
      dataType: "text"
    });
  });

  $(document).on('change','#sporttype',function(){

    var value = $('#sporttype').val();
    if (value){
      var url = '/admin/bad_vk/get_users/'+value;
      $.ajax({
        url: url,
        async: true,
        success: function (responseData, textStatus) {
          alert('Список получен!\n' + responseData);
          $('#userslist').html(responseData);
        },
        error: function (response, status, errorThrown) {
          alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
        },
        type: "GET",
        dataType: "text"
      });
    }

  });
</script>