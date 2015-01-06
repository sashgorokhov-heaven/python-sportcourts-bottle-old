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
    var logins = [];
    if ($("#login1").val().length > 0) {
      logins.push($("#login1").val());
    };
    if ($("#login2").val().length > 0) {
      logins.push($("#login2").val());
    };
    if ($("#login3").val().length > 0) {
      logins.push($("#login3").val());
    };
    var url = '/admin/vk/auth?accounts=';
    for (var i = 0; i < logins.length - 1; i++) {
      url += logins[i] + ',';
    };
    url = url.slice(1);
    $.ajax({
      url: url
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