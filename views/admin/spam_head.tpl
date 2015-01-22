<script type="text/javascript">
  var users = [];

  $(document).on('click', '#showbutton', function(){
    var tpl_id = $('#sporttype').val();

    if (tpl_id) {
      $.ajax({
      url: '/showtpl/spam'+tpl_id,
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
    var tpl_id = $('#sporttype').val();
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

  $( document ).ready(function() {
    $('#adminModal').modal('show');
    var url = '/admin/bad_vk/auth';
    $.ajax({
      url: url,
      async: true,
      success: function (responseData, textStatus) {
        var json = JSON.parse(responseData);
        success = json['success'];
        if (success) {
          $('#adminslist').html(success);
          $('#adminModal').modal('hide');
        } else {
          $('#authinfo').html(responseData);
        }
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
          var json = JSON.parse(responseData);
          users = json['users'];
          $('#userslist').html('Найдено людей: '+users.length);
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