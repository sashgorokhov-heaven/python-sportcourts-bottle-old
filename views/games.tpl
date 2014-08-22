% rebase("_basicpage", title="Игры")
      <div class="jumbotron">
        <h1>Таблица игр</h1>
        <p>Здесь вы можете присоединиться к любой игре, в которой еще есть места.</p>
      </div>

      <ul class="nav nav-tabs">
        <li class="active"><a href="#all" data-toggle="tab">Все</a></li>
        % for sport_type in sports:
            <li><a href="#{{sport_type['sport_id']}}" data-toggle="tab">{{sport_type['title']}}</a></li>
        % end
        % if 0<adminlevel<=2:
        <li class="pull-right"><a href="/games?add"><span class="glyphicon glyphicon-plus"></span> Создать</a></li>
        % end
      </ul>

      <div class="tab-content">
        <div class="tab-pane active" id="all">
          <div class="panel panel-deafult">
            <br>
            % for game in games:
                % include("game", game=game)
            % end
            <!--<ul class="pager">
              <li class="previous disabled"><a href="#">&larr; Раньше</a></li>
              <li class="next"><a href="#">Позже &rarr;</a></li>
            </ul>-->
          </div>
        </div>

        % for sport_type in sports:
            <div class="tab-pane" id="{{sport_type['sport_id']}}">
              <div class="panel panel-deafult">
                <br>
                % for game in games:
                	% if game['sport_type']['sport_id']==sport_type['sport_id']:
                	    % include("game", game=game)
                	% end
                % end
              </div>
            </div>
        % end

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