% rebase("_basicpage", title="Игры")
      <div class="jumbotron">
        <h1>Таблица игр</h1>
        <p>Здесь вы можете присоединиться к любой игре, в которой еще есть места.</p>
      </div>

      <ul class="nav nav-tabs">
        <li class="active"><a href="#all" data-toggle="tab">Все</a></li>
        <li><a href="#basket" data-toggle="tab">Баскетбол</a></li>
        <li><a href="#volley" data-toggle="tab">Воллейбол</a></li>
        <li><a href="#football" data-toggle="tab">Футбол</a></li>
        <li class="pull-right"><a href="/games?add"><span class="glyphicon glyphicon-plus"></span> Создать</a></li>
      </ul>

      <div class="tab-content">
        <div class="tab-pane active" id="all">
          <div class="panel panel-deafult">
            <br>
            % for game in games:
            % include("game", game=game)
            % end
          </div>
        </div><!-- End of All games -->

        <!-- Basketball games -->
        <div class="tab-pane" id="basket">
          <div class="panel panel-deafult">
            <br>
            % for game in games:
            	% if game['sport_type']['sport_id']==3:
            	% include("game", game=game)
            	% end
            % end
          </div>
        </div><!-- End of Basketball games -->

        <!-- Volleyball games -->
        <div class="tab-pane" id="volley">
          <div class="panel panel-deafult">
            <br>
            % for game in games:
            	% if game['sport_type']['sport_id']==5:
            	% include("game", game=game)
            	% end
            % end
          </div>
        </div><!-- End of volleyball games -->

        <!-- Football games -->
        <div class="tab-pane" id="football">
          <div class="panel panel-deafult">
            <br>
            % for game in games:
            	% if game['sport_type']['sport_id']==2:
            	% include("game", game=game)
            	% end
            % end
          </div>
        </div><!-- End of football games -->

      </div>

      % if loggedin:
      <script type="text/javascript">
      $(document).on('click', 'li', function() {
        arr = $(this).attr("id").split('-');
        var user_id = arr[1],
          game_id = arr[0],
          unsubscribe = arr[2];
        if (unsubscribe=='u') {
          $.ajax({
            url: 'http://sportcourts.ru/subscribe',
            data: {
              game_id: game_id,
              unsubscribe: 0
            },
            async: true,
            success: function (responseData, textStatus) {
              // alert(responseData + ' Status: ' + textStatus);
              alert('Теперь вас нет в списках на игру');
              // document.location.href = 'http://sportcourts.ru/games#game' + game_id;
              window.location.reload();
            },
            error: function (response, status, errorThrown) {
              alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
            },
            type: "POST",
            dataType: "text"
          });
        } else {
          $.ajax({
            url: 'http://sportcourts.ru/subscribe',
            data: {
              game_id: game_id
            },
            async: true,
            success: function (responseData, textStatus) {
              // alert(responseData + ' Status: ' + textStatus);
              alert('Вы успешно записаны на игру');
              // document.location.href = 'http://sportcourts.ru/games#game' + game_id;
              window.location.reload();
            },
            error: function (response, status, errorThrown) {
              alert('Все плохо' + response + status + errorThrown);
            },
            type: "POST",
            dataType: "text"
          });
        }

      });
      </script>
      % end