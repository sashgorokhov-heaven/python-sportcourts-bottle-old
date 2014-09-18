% rebase("_basicpage", title="Игры")
      <!-- <div class="jumbotron">
        <h1>Таблица игр</h1>
        <p>Здесь вы можете присоединиться к любой игре, в которой еще есть места.</p>
      </div> -->
      <div class="row">
        <div class="col-md-12"  style="margin-top:50px;">
          &nbsp;
        </div>
      </div>
      <div class="row">
        <div class="col-md-3">
          <div class="panel panel-default">
            <div class="panel-body">
              <p class="lead">Наши игры <!-- <a href="/courts?all"><small>на карте</small></a> --></p>
              <div class="form-group">
                <select id="sporttype" name="sport_type" class="form-control" data-bv-notempty="true"
                data-bv-notempty-message="Укажите вид спорта">
                  <option value="">Вид спорта</option>
                  % for sport_type in sports:
                      <option value="{{sport_type['sport_id']}}" {{'selected' if sport_type['sport_id']==sport_type['sport_id'] else ''}}>{{sport_type['title']}}</option>
                  % end
                </select>
              </div>
              <!-- <div class="form-group">
                <select id="city" name="city_id" class="form-control">
                  <option value="0">Город</option>
                  <option value="1">Екатеринбург</option>
                </select>
              </div> -->
              <div class="form-group">
                <button type="button" class="btn btn-primary btn-block gamessearch">Найти</button>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-9">
          <ul class="nav nav-tabs">
            <li class="active"><a href="#all" data-toggle="tab">Все</a></li>
            % if loggedin and len([game for game in games if userinfo['user_id'] in {i['user_id'] for i in game['subscribed']['users']}])>0:
            <li><a href="#my" data-toggle="tab">Мои игры</a></li>
            % end
            % if userinfo['organizer']:
            <li class="pull-right"><a href="/games?add"><span class="glyphicon glyphicon-plus"></span> Создать</a></li>
            % end
          </ul>

          <div class="tab-content">
            <div class="tab-pane active games_cards_all" id="all">
              <div class="panel panel-deafult">
                <br>
                % for game in games:
                    % include("game", game=game)
                % end
                <ul class="pager">
                  <!--<li class="previous disabled"><a href="#">&larr; Раньше</a></li> -->
                  % if defined("nextpage") and nextpage:
                    <li class="next"><a href="/games?page={{nextpage}}">Позже &rarr;</a></li>
                  % end
                </ul>
              </div>
            </div>

            % if loggedin:
            <div class="tab-pane" id="my">
              <div class="panel panel-deafult">
                <br>
                % for game in games:
                    % if userinfo['user_id'] in {i['user_id'] for i in game['subscribed']['users']}:
                        % include("game", game=game)
                    % end
                % end
              </div>
            </div>
            % end

          </div>

        </div>
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
            url: '/subscribe',
            data: {
              game_id: game_id,
              unsubscribe: 0
            },
            async: true,
            success: function (responseData, textStatus) {
              // alert(responseData + ' Status: ' + textStatus);
              alert('Теперь вас нет в списках на игру');
              // document.location.href = '/games#game' + game_id;
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
            url: '/subscribe',
            data: {
              game_id: game_id
            },
            async: true,
            success: function (responseData, textStatus) {
              // alert(responseData + ' Status: ' + textStatus);
              alert('Вы успешно записаны на игру');
              // document.location.href = '/games#game' + game_id;
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