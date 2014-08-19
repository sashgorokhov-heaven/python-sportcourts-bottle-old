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
      </ul>

      <div class="tab-content">
        <div class="tab-pane active" id="all">
          <div class="panel panel-deafult">
            <br>
            % for game in games:
            <div class="panel panel-default"><a name="{{game['game_id']}}"></a>
              <div class="panel-heading">
                <a href="/games?game_id={{game['game_id']}}">#{{game['game_id']}}</a>
              </div>
              <div class="panel-body">
                <div class="col-md-2">
                  <p>{{game['datetime']}}</p>
                </div>
                <div class="col-md-6">
                  <p>{{game['description']}}</p>
                  <p><a href="/courts?court_id={{game['court']['court_id']}}" target="_blank">{{game['court']['title']}}</a></p>
                  <div class="progress">
                    <div class="progress-bar{{' progress-bar-success' if game['subscribed']['count'] == game['capacity'] else ''}}" role="progressbar" style="width:{{round((game['subscribed']['count']/game['capacity'])*100)}}%">
                        <span class="">{{game['subscribed']['count']}}/{{game['capacity']}}</span>
                    </div>
                  </div>
                  % if game['subscribed']['count'] > 0:
                  <div class="panel-group" id="accordion" style="margin-bottom:0px;">
                    <div class="panel panel-default">
                      <div class="panel-heading" style="text-align: center">
                        <h5 class="panel-title" style="font-size:1em;">
                          <a data-toggle="collapse" data-parent="#accordion" href="#collapse-{{game['game_id']}}">Список участников <span class="caret"></span> 
                        </h5>
                      </div>
                      <div id="collapse-{{game['game_id']}}" class="panel-collapse collapse">
                        <div class="panel-body">
                          % for n, user in enumerate(game['subscribed']['users'], 1):
                          <p><a href="/profile?user_id={{user['user_id']}}">{{'{}. {} {}'.format(n, user['first_name'], user['last_name'])}}</a></p>
                          % end
                        </div>
                      </div>
                    </div>
                  </div>
                  % end
                </div>
                <div class="col-md-2">
                  <p>{{game['cost']}} RUB за {{game['duration']}} минут</p>
                </div>
                <div class="col-md-2">

                  % if game['subscribed']['count'] == game['capacity']:
                    <button type="button" class="btn btn-default btn-xs" disabled="disabled" data-toggle="dropdown">Места заполнены</button>
                  % end
                  % if loggedin:
                    <button type="button" class="btn btn-success btn-xs dropdown-toggle" data-toggle="dropdown">Я иду</button>
                      <ul class="dropdown-menu" role="menu">
                        <li id="{{game['game_id']}}-{{user_id}}-u"><a style="cursor:pointer;">Не пойду</a></li>
                      </ul>
                  % end
                  % if not loggedin:
                    <button type="button" class="btn btn-primary btn-xs dropdown-toggle" data-toggle="dropdown">Идет набор</button>
                  % end
                </div>
              </div>
            </div>
            % end
          </div>
        </div><!-- End of All games -->

        <!-- Basketball games -->
        <div class="tab-pane" id="basket">
          <div class="panel panel-deafult">
            <br>
            % for game in games:
            	% if game['sport_type']['sport_id']==3:
            <div class="panel panel-default"><a name="{{game['game_id']}}"></a>
              <div class="panel-heading">
                <a href="/games?game_id={{game['game_id']}}">#{{game['game_id']}}</a>
              </div>
              <div class="panel-body">
                <div class="col-md-2">
                  <p>{{game['datetime']}}</p>
                </div>
                <div class="col-md-6">
                  <p>{{game['description']}}</p>
                  <p><a href="/courts?court_id={{game['court']['court_id']}}" target="_blank">{{game['court']['title']}}</a></p>
                  <div class="progress">
                    <div class="progress-bar{{' progress-bar-success' if game['subscribed']['count'] == game['capacity'] else ''}}" role="progressbar" style="width:{{round((game['subscribed']['count']/game['capacity'])*100)}}%">
                        <span class="">{{game['subscribed']['count']}}/{{game['capacity']}}</span>
                    </div>
                  </div>
                  % if game['subscribed']['count'] > 0:
                  <div class="panel-group" id="accordion" style="margin-bottom:0px;">
                    <div class="panel panel-default">
                      <div class="panel-heading" style="text-align: center">
                        <h5 class="panel-title" style="font-size:1em;">
                          <a data-toggle="collapse" data-parent="#accordion" href="#collapse-{{game['game_id']}}">Список участников <span class="caret"></span> 
                        </h5>
                      </div>
                      <div id="collapse-{{game['game_id']}}" class="panel-collapse collapse">
                        <div class="panel-body">
                          % for n, user in enumerate(game['subscribed']['users'], 1):
                          <p><a href="/profile?user_id={{user['user_id']}}">{{'{}. {} {}'.format(n, user['first_name'], user['last_name'])}}</a></p>
                          % end
                        </div>
                      </div>
                    </div>
                  </div>
                  % end
                </div>
                <div class="col-md-2">
                  <p>{{game['cost']}} RUB за {{game['duration']}} минут</p>
                </div>
                <div class="col-md-2">

                  % if game['subscribed']['count'] == game['capacity']:
                    <button type="button" class="btn btn-default btn-xs" disabled="disabled" data-toggle="dropdown">Места заполнены</button>
                  % end
                  % if loggedin:
                    <button type="button" class="btn btn-success btn-xs dropdown-toggle" data-toggle="dropdown">Я иду</button>
                      <ul class="dropdown-menu" role="menu">
                        <li id="{{game['game_id']}}-{{user_id}}-u"><a style="cursor:pointer;">Не пойду</a></li>
                      </ul>
                  % end
                  % if not loggedin:
                    <button type="button" class="btn btn-primary btn-xs dropdown-toggle" data-toggle="dropdown">Идет набор</button>
                  % end
                </div>
              </div>
            </div>
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
            <div class="panel panel-default"><a name="{{game['game_id']}}"></a>
              <div class="panel-heading">
                <a href="/games?game_id={{game['game_id']}}">#{{game['game_id']}}</a>
              </div>
              <div class="panel-body">
                <div class="col-md-2">
                  <p>{{game['datetime']}}</p>
                </div>
                <div class="col-md-6">
                  <p>{{game['description']}}</p>
                  <p><a href="/courts?court_id={{game['court']['court_id']}}" target="_blank">{{game['court']['title']}}</a></p>
                  <div class="progress">
                    <div class="progress-bar{{' progress-bar-success' if game['subscribed']['count'] == game['capacity'] else ''}}" role="progressbar" style="width:{{round((game['subscribed']['count']/game['capacity'])*100)}}%">
                        <span class="">{{game['subscribed']['count']}}/{{game['capacity']}}</span>
                    </div>
                  </div>
                  % if game['subscribed']['count'] > 0:
                  <div class="panel-group" id="accordion" style="margin-bottom:0px;">
                    <div class="panel panel-default">
                      <div class="panel-heading" style="text-align: center">
                        <h5 class="panel-title" style="font-size:1em;">
                          <a data-toggle="collapse" data-parent="#accordion" href="#collapse-{{game['game_id']}}">Список участников <span class="caret"></span> 
                        </h5>
                      </div>
                      <div id="collapse-{{game['game_id']}}" class="panel-collapse collapse">
                        <div class="panel-body">
                          % for n, user in enumerate(game['subscribed']['users'], 1):
                          <p><a href="/profile?user_id={{user['user_id']}}">{{'{}. {} {}'.format(n, user['first_name'], user['last_name'])}}</a></p>
                          % end
                        </div>
                      </div>
                    </div>
                  </div>
                  % end
                </div>
                <div class="col-md-2">
                  <p>{{game['cost']}} RUB за {{game['duration']}} минут</p>
                </div>
                <div class="col-md-2">

                  % if game['subscribed']['count'] == game['capacity']:
                    <button type="button" class="btn btn-default btn-xs" disabled="disabled" data-toggle="dropdown">Места заполнены</button>
                  % end
                  % if loggedin:
                    <button type="button" class="btn btn-success btn-xs dropdown-toggle" data-toggle="dropdown">Я иду</button>
                      <ul class="dropdown-menu" role="menu">
                        <li id="{{game['game_id']}}-{{user_id}}-u"><a style="cursor:pointer;">Не пойду</a></li>
                      </ul>
                  % end
                  % if not loggedin:
                    <button type="button" class="btn btn-primary btn-xs dropdown-toggle" data-toggle="dropdown">Идет набор</button>
                  % end
                </div>
              </div>
            </div>
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
            <div class="panel panel-default"><a name="{{game['game_id']}}"></a>
              <div class="panel-heading">
                <a href="/games?game_id={{game['game_id']}}">#{{game['game_id']}}</a>
              </div>
              <div class="panel-body">
                <div class="col-md-2">
                  <p>{{game['datetime']}}</p>
                </div>
                <div class="col-md-6">
                  <p>{{game['description']}}</p>
                  <p><a href="/courts?court_id={{game['court']['court_id']}}" target="_blank">{{game['court']['title']}}</a></p>
                  <div class="progress">
                    <div class="progress-bar{{' progress-bar-success' if game['subscribed']['count'] == game['capacity'] else ''}}" role="progressbar" style="width:{{round((game['subscribed']['count']/game['capacity'])*100)}}%">
                        <span class="">{{game['subscribed']['count']}}/{{game['capacity']}}</span>
                    </div>
                  </div>
                  % if game['subscribed']['count'] > 0:
                  <div class="panel-group" id="accordion" style="margin-bottom:0px;">
                    <div class="panel panel-default">
                      <div class="panel-heading" style="text-align: center">
                        <h5 class="panel-title" style="font-size:1em;">
                          <a data-toggle="collapse" data-parent="#accordion" href="#collapse-{{game['game_id']}}">Список участников <span class="caret"></span> 
                        </h5>
                      </div>
                      <div id="collapse-{{game['game_id']}}" class="panel-collapse collapse">
                        <div class="panel-body">
                          % for n, user in enumerate(game['subscribed']['users'], 1):
                          <p><a href="/profile?user_id={{user['user_id']}}">{{'{}. {} {}'.format(n, user['first_name'], user['last_name'])}}</a></p>
                          % end
                        </div>
                      </div>
                    </div>
                  </div>
                  % end
                </div>
                <div class="col-md-2">
                  <p>{{game['cost']}} RUB за {{game['duration']}} минут</p>
                </div>
                <div class="col-md-2">

                  % if game['subscribed']['count'] == game['capacity']:
                    <button type="button" class="btn btn-default btn-xs" disabled="disabled" data-toggle="dropdown">Места заполнены</button>
                  % end
                  % if loggedin:
                    <button type="button" class="btn btn-success btn-xs dropdown-toggle" data-toggle="dropdown">Я иду</button>
                      <ul class="dropdown-menu" role="menu">
                        <li id="{{game['game_id']}}-{{user_id}}-u"><a style="cursor:pointer;">Не пойду</a></li>
                      </ul>
                  % end
                  % if not loggedin:
                    <button type="button" class="btn btn-primary btn-xs dropdown-toggle" data-toggle="dropdown">Идет набор</button>
                  % end
                </div>
              </div>
            </div>
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
              user_id: user_id,
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
            url: 'http://sportcourts.ru:4444/api/games.subscribe',
            data: {
              user_id: user_id,
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