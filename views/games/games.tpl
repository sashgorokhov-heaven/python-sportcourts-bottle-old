% rebase("_basicpage", title="Игры")
% setdefault("bysport", 0)
% setdefault("old", False)
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
          <div class="row">
            <div class="col-md-12 col-sm-6 col-xs-12">
              <div class="panel panel-default">
                <div class="panel-body">
                  <p class="lead">Наши игры <!-- <a href="/courts?all"><small>на карте</small></a> --></p>
                  <div class="form-group">
                    <select id="sporttype" name="sport_type" class="form-control" data-bv-notempty="true"
                    data-bv-notempty-message="Укажите вид спорта">
                      <option value="0">Все</option>
                      <option value="-1" {{'selected' if old else ''}}>Прошедшие игры</option>
                      % for sport_type in sports:
                          <option value="{{sport_type.sport_id()}}" {{'selected' if bysport==sport_type.sport_id() else ''}}>{{sport_type.title()}}</option>
                      % end
                    </select>
                  </div>
                  <!-- <div class="form-group">
                    <select id="city" name="city_id" class="form-control">
                      <option value="0">Город</option>
                      <option value="1">Екатеринбург</option>
                    </select>
                  </div> -->
                  <!-- <div class="form-group">
                    <button type="button" class="btn btn-primary btn-block gamessearch">Найти</button>
                  </div> -->
                </div>
              </div>
            </div>
            <div class="col-md-12 col-sm-6 col-xs-12">
              <div class="panel panel-default">
                <div class="panel-body">
                  <p class="lead">Поделиться</p>
                  <script type="text/javascript" src="//yandex.st/share/share.js"
                  charset="utf-8"></script>
                  <div class="yashare-auto-init" data-yashareL10n="ru"data-yashareQuickServices="vkontakte,facebook,twitter,odnoklassniki" data-yashareTheme="counter" style="margin-left: -5px; width: 110%;"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-9">
          <ul class="nav nav-tabs">
            <li class="active"><a href="#all" data-toggle="tab">Все
                % if defined("total_count"):
                <b>({{total_count}})</b>
                % end
                </a></li>
            % if loggedin and (len([game for game in games if current_user.user_id() in set(game.subscribed())])>0 or len([game for game in games if current_user.user_id() in set(game.reserved_people())])>0):
            <li><a href="#my" data-toggle="tab">Мои игры</a></li>
            % end
            % if current_user.userlevel.organizer() or current_user.userlevel.admin():
            <li class="pull-right"><a href="/games/add"><span class="glyphicon glyphicon-plus"></span> Создать</a></li>
            % end
          </ul>

          <div class="tab-content">
            <div class="tab-pane active" id="all">
              <div class="panel panel-deafult games_cards_all">
                <br>
                % if len(games)>0:
                    % for game in games:
                        % include("game", game=game, tab_name="all")
                    % end
                % end
                % if len(games)==0:
                  <div class="alert alert-info fade in" style="text-center">
                    <p class="lead">Игр пока нет)</p>
                    <p class="lead">Ожидайте, скоро все будет.</p>
                    <!-- <a class="text-center">
                      <img src="/images/static/2015.png" alt="" style="width:60%; margin:15px auto; margin-left:20%">
                    </a> -->
                  </div>
                % end
              </div>
            </div>

            % if loggedin:
            <div class="tab-pane" id="my">
              <div class="panel panel-deafult">
                <br>
                % for game in games:
                    % if current_user.user_id() in set(game.reserved_people()) or current_user.user_id() in set(game.subscribed()):
                        % include("game", game=game, tab_name="my")
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
          var game_id = arr[0], action = arr[1];

          if ($('#all').hasClass('active') == true){
            var pane = 'all';
          } else if ($('#my').hasClass('active') == true) {
            var pane = 'my';
          };

          $.ajax({
            url: '/games/'+action+'/'+game_id,
            data: {
              tab_name:pane
            },
            async: true,
            success: function (responseData, textStatus) {
              $('#gamepane-'+game_id+'-'+pane).fadeOut('slow', function() {
                  $('#gamepane-'+game_id+'-all').replaceWith(responseData);
                  $('#gamepane-'+game_id+'-my').replaceWith(responseData);
              });
            },
            error: function (response, status, errorThrown) {
              alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
            },
            type: "GET",
            dataType: "text"
          });

        });
        </script>
      % end