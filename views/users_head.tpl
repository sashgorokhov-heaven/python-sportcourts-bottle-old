<script>
  $(document).ready(function(){

    /* Переменная-флаг для отслеживания того, происходит ли в данный момент ajax-запрос. В самом начале даем ей значение false, т.е. запрос не в процессе выполнения */
    var inProgress = false;
    /* С какого профиля надо делать выборку из базы при ajax-запросе */
    var startFromAll = 10;
    var startFromFriends = 10;

    /* Используем вариант $('#more').click(function() для того, чтобы проматывать по кнопке "Дальше"*/
    $(window).scroll(function() {

      /* Если высота окна + высота прокрутки больше или равны высоте всего документа и ajax-запрос в настоящий момент не выполняется, то запускаем ajax-запрос */
      if($(window).scrollTop() + $(window).height() >= $(document).height() - 200 && !inProgress) {

        // смотрим, на какой мы вкладке
        if($('.panel-all').hasClass('active') == true)
        {
          var section = 'all';
          var startFrom = startFromAll;
        }
        else if($('.panel-friends').hasClass('active') == true)
        {
          var section = 'friends';
          var startFrom = startFromFriends;
        }

        $.ajax({
          url: '/moreusers',
          data: {
            startfrom: startFrom,
            section: section
          },
          type: "POST",
          dataType: "text",
          async: true,
          beforeSend: function() {
            /* меняем значение флага на true, т.е. запрос сейчас в процессе выполнения */
            inProgress = true;},
          success: function (responseData, textStatus) {
            // alert(responseData + ' Status: ' + textStatus);
            alert('Загрузили еще юзеров');
            data = jQuery.parseJSON(data);
            // если массив не пустой
            if (data.length > 0) {

              $.each(data, function(index, data){
                /* Отбираем по идентификатору блок с юзерами и дозаполняем его новыми данными */
                $("#users").append("<p><b>" + data.name + "</b><br />" + data.text + "</p>");
                // если сработает, забью сюда нормальный вид
              });
              /* По факту окончания запроса снова меняем значение флага на false */
              inProgress = false;
              // Увеличиваем на 10 порядковый номер статьи, с которой надо начинать выборку из базы
              startFrom += 10;

            }
          },
          error: function (response, status, errorThrown) {
            alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
          }
        });
      };
    });
  });
</script>