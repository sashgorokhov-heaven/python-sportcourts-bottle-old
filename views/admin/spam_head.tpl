<script type="text/javascript">
  var users = {};
  var count = 0;

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

    var sent = 0;
    var errors = 0;
    var sentlimit = 2;
    var errorslimit = 3;

    for(key in users) {
      if (sent == sentlimit) break;
      if (errors == errorslimit) break;
      id = key;
      var url = '/admin/new_vk/users/send/'+id+'/spam'+tpl_id+'/1';
      $.ajax({
        url: url,
        async: false,
        success: function (responseData, textStatus) {
          var str = '';
          var type = '';
          var json = JSON.parse(responseData);
          var error = json["error"];
          var response = json["response"];
          console.log(responseData);
          if (error) {
            type = 'danger';
            str = error["description"];
            sent++;
            errors++;
          } else if (response) {
            if ("continued" in response) {
              type = 'warning';
              str = 'Пользователь уже зарегистрирован у нас';
              sent++;
            } else {
              type = 'success';
              str = 'Успешно: '+responseData;
              sent++;
            }
          };
          console.log(str);
          $('#sendtable').append('<tr class="'+type+'"><td><a href="http://vk.com/id'+id+'">'+id+'</a></td><td>'+str+'</td></tr>');
        },
        error: function (response, status, errorThrown) {
          $("#sendtable").append('<tr class="danger"><td><a href="http://vk.com/id'+id+'">'+id+'</a></td><td>'+responseData+'</td></tr>');
        },
        type: "POST",
        dataType: "text"
      });
    }
  });

  $( document ).ready(function() {
    $('#adminModal').modal('show');
    var url = '/admin/new_vk/auth/check';
    $.ajax({
      url: url,
      async: true,
      success: function (responseData, textStatus) {
        var json = JSON.parse(responseData);
        response = json['response'];
        if (response) {
          var str = '';
          for (key in response) {
            str += key+' ('+response[key]+')'+'<br>';
          };
          $('#adminslist').html(str);
          $('#adminModal').modal('hide');
        } else {
          var url = '/admin/new_vk/auth';
          $.ajax({
            url: url,
            async: true,
            success: function (responseData, textStatus) {
              var json = JSON.parse(responseData);
              response = json['response'];
              success = response['success'];
              if (success) {
                var str = '';
                for (i=0; i<success.length; i++) {
                  str += success[i]+'<br>';
                };
                $('#adminslist').html(str);
                $('#adminModal').modal('hide');
              } else {
                $('#authinfo').html(responseData);
              }
            },
            error: function (response, status, errorThrown) {
              alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
            },
            type: "POST",
            dataType: "text"
          });
        }
      },
      error: function (response, status, errorThrown) {
        alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
      },
      type: "POST",
      dataType: "text"
    });
  });

  $(document).on('change','#sporttype',function(){

    var value = $('#sporttype').val();
    if (value){
      var url = '/admin/new_vk/users/get/'+value;
      $.ajax({
        url: url,
        async: true,
        success: function (responseData, textStatus) {
          var json = JSON.parse(responseData);
          users = json["response"];
          count = 0;
          for (key in users) {
            count++;
          };
          $('#userslist').html('Найдено людей: '+count);
        },
        error: function (response, status, errorThrown) {
          alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
        },
        type: "POST",
        dataType: "text"
      });
    }

  });
</script>