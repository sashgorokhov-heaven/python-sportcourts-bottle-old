<script>
  $(document).ready(function(){

    var inProgress = false;
    var step = 8;
    var startFromAll = step;
    var startFromFriends = step;

    $(window).scroll(function() {

      if($(window).scrollTop() + $(window).height() >= $(document).height() - 1 && !inProgress) {

        if($('#panel-all').hasClass('active') == true)
        {
          var section = 'all';
          var startFrom = startFromAll;
        }
        // else if($('#panel-friends').hasClass('active') == true)
        // {
        //   var section = 'friends';
        //   var startFrom = startFromFriends;
        // }

        $.ajax({
          url: '/users',
          data: {
            startfrom: startFrom,
            section: section
          },
          type: "POST",
          dataType: "text",
          async: true,
          beforeSend: function() {
            inProgress = true;
          },
          success: function (responseData, textStatus) {
            data = jQuery.parseJSON(responseData);
            if (data.length > 0) {
              $.each(data, function(index, data){
                if(section == 'all'){
                  $('.user_cards_all').append(data+'<hr>');
                }
                // else if(section == 'friends'){
                //   $('.user_cards_friends').append(data+'<hr>');
                // }
              });
              inProgress = false;
              if(section == 'all'){
                startFromAll += step;
              }
              // else if(section == 'friends'){
              //   startFromFriends += step;
              // }
            }
          },
          error: function (response, status, errorThrown) {
            alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
            inProgress = false;
          }
        });
      };
    });
  });
</script>