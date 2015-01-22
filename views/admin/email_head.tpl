<script type="text/javascript">
  var users = [];

  $(document).on('click', '#showbutton', function(){
    var tpl_id = 'mail_a4';

    if (tpl_id) {
      $.ajax({
      url: '/showtpl/'+tpl_id,
      async: true,
      success: function (responseData, textStatus) {
        $('#tpl_show').html(responseData);
        $('#showModal').modal('show');
      },
      error: function (response, status, errorThrown) {
        alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
      },
      type: "GET",
      dataType: "text"
    });
    }
  });

  $(document).on('click', '#sendbutton', function(){
    $('#sendtable').html('');
    $('#sendModal').modal('show');

    var ids = [];

    ulength = users.length;
    if (ulength > 15) {
      ulength = 15;
    }

    for(var i=0; i<ulength; i++) {
      id = users[i];
      var url = '/admin/bad_vk/send/'+id+'/spam'+tpl_id+'/0';
      $.ajax({
        url: url,
        async: false,
        success: function (responseData, textStatus) {
          console.log(id);
          $('#sendtable').append('<tr class="success"><td><a href="http://vk.com/id'+id+'">'+id+'</a></td><td>'+responseData+'</td></tr>');
        },
        error: function (response, status, errorThrown) {
          $("#sendtable").append('<tr class="danger"><td><a href="http://vk.com/id'+id+'">'+id+'</a></td><td>'+responseData+'</td></tr>');
        },
        type: "GET",
        dataType: "text"
      });
    }
  });
</script>