% rebase("_basicpage", title="Редактировать игру")
<div class="jumbotron">
  <div class="row">
    <div class="col-md-12 registration" style="text-align:left;">
      <h2 class="text-center">Редактирование игры №{{game.game_id()}}</h2><br>
      <form id="gameaddForm" method="post" class="form-horizontal" action="/games/edit/{{game.game_id()}}" data-bv-message="This value is not valid" enctype="multipart/form-data" data-bv-feedbackicons-valid="glyphicon glyphicon-ok" data-bv-feedbackicons-invalid="glyphicon glyphicon-remove" data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
        <div class="row">
        % if game.created_by()==current_user.user_id() or current_user.userlevel.admin():
          <div class="col-md-6">
            <input type="hidden" name="game_id" value="{{game.game_id()}}">
            <div class="form-group">
              <label for="court_add_count" class="col-sm-4 control-label">Название</label>
              <div class="col-sm-8">
                <input class="form-control" type="text" name="description" value="{{game.description()}}" {{'disabled' if game.reported() else ''}}/>
              </div>
            </div>
            <div class="form-group">
              <label for="inlineCheckbox" class="col-sm-4 control-label">Вид спорта</label>
              <div class="col-sm-8">
                <select id="sporttype" name="sport_type" class="form-control" data-bv-notempty="true"
                data-bv-notempty-message="Укажите вид спорта" {{'disabled' if game.reported() else ''}}>
                  <option value="{{game.sport_type()}}">{{game.sport_type(True).title()}}</option>
                  % for sport_type in sports:
                    % if sport_type.sport_id() != game.sport_type():
                      <option value="{{sport_type.sport_id()}}">{{sport_type.title()}}</option>
                    % end
                  % end
                </select>
              </div>
            </div>
            <div class="form-group">
              <label for="inlineCheckbox" class="col-sm-4 control-label">Тип игры</label>
              <div class="col-sm-8">
                <select id="gametype" name="game_type" class="form-control" data-bv-notempty="true" data-bv-notempty-message="Укажите тип игры" {{'disabled="disabled"' if game.reported() else ''}}>
                  <option value="{{game.game_type()}}" class="{{game.game_type(True).sport_type()}}">{{game.game_type(True).title()}}</option>
                  % for type in game_types:
                    % if type.type_id() != game.game_type():
                      <option value="{{type.type_id()}}" class="{{type.sport_type()}}">{{type.title()}}</option>
                    % end
                  % end
                </select>
              </div>
            </div>
            % if not game.reported():
              <script type="text/javascript">
                $("#gametype").chained("#sporttype");
              </script>
            % end
            <div class="form-group">
              <label for="inputCity" class="col-sm-4 control-label">Город</label>
              <div class="col-sm-8">
                <select id="city" name="city_id" class="form-control" data-bv-notempty="true" data-bv-notempty-message="Укажите город" {{'disabled' if game.reported() else ''}}>
                <option value="{{game.city_id()}}">{{game.city_id(True).title()}}</option>
                % for city in cities:
                    % if city.city_id() != game.city_id():
                      <option value="{{city.city_id()}}">{{city.title()}}</option>
                    % end
                % end
                </select>
                <span id="valid"></span>
              </div>
            </div>
            <div class="form-group">
              <label for="inputBirght" class="col-sm-4 control-label">Площадка</label>
              <div class="col-sm-8">
                <select id="court" name="court_id" class="form-control" data-bv-notempty="true" data-bv-notempty-message="Укажите площадку" {{'disabled' if game.reported() else ''}}>
                  <option value="{{game.court_id()}}" class="{{game.court_id(True).city_id()}}">{{game.court_id(True).title()}}</option>
                  % for court in courts:
                    % if court.court_id()!=game.court_id():
                      <option value="{{court.court_id()}}" class="{{court.city_id()}}">{{court.title()}}</option>
                    % end
                  % end
                </select>
              </div>
            </div>
            <div class="form-group">
              <label for="inputBirght" class="col-sm-4 control-label">Дата</label>
              <div class="col-sm-8">
                <input type="date" class="form-control" name="date"data-bv-notempty="true" value="{{game.datetime.date()}}" data-bv-notempty-message="Укажите дату проведения" {{'disabled' if game.reported() else ''}}/>
              </div>
            </div>
            <div class="form-group">
              <label for="inputBirght" class="col-sm-4 control-label">Начало</label>
              <div class="col-sm-6">
                <input type="time" class="form-control" name="time"data-bv-notempty="true" value="{{game.datetime.time()}}" data-bv-notempty-message="Укажите время начала" {{'disabled' if game.reported() else ''}}/>
              </div>
            </div>
            <div class="form-group">
              <label for="game_add_long" class="col-sm-4 control-label">Длительность</label>
              <div class="col-sm-8">
                <input type="text" id="game_add_long_visible" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                <div id="game_add_slider2"></div>
                <input type="hidden" id="game_add_long" name="duration" readonly>
              </div>
            </div>
            <div class="form-group">
              <label for="game_add_amount" class="col-sm-4 control-label">Цена</label>
              <div class="col-sm-8">
                <input type="text" id="game_add_amount_visible" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                <div id="game_add_slider"></div>
                <input type="hidden" id="game_add_amount" name="cost" readonly>
              </div>
            </div>
            <div class="form-group">
              <label for="game_add_count" class="col-sm-4 control-label">Количество мест</label>
              <div class="col-sm-8">
                <input type="text" id="game_add_count_visible" name="capacity" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                <div id="game_add_slider1" {{'class=disabled' if game.capacity()<0 else ''}}></div>
                <input type="hidden" id="game_add_count" name="capacity" readonly>
              </div>
              <div class="col-sm-8">
                <div class="checkbox">
                  <label>
                    <input type="checkbox" id="unlimit" value="-1" onchange="showOrHide();" {{'checked' if game.capacity()<0 else ''}} {{'disabled="disabled"' if game.reported() else ''}}>Безлимитно
                  </label>
                </div>
              </div>
            </div>
            % if game.reported():
              <script type="text/javascript">
                $( document ).ready(function() {
                  $("#game_add_slider1").slider( "disable" );
                  $("#game_add_slider").slider( "disable" );
                  $("#game_add_slider2").slider( "disable" );
                });
              </script>
            % end
            <div class="form-group">
              <div class="col-sm-offset-2 col-sm-8" style="text-align:center;">
                % if not game.reported():
                <button type="submit" name="submit_edit" class="btn btn-primary">Применить</button>
                % end
                % if current_user.user_id()==game.created_by() or (loggedin and current_user.userlevel.admin()):
                  <button type="button" data-toggle="modal" data-target="#deleteGameModal" class="btn btn-danger">Удалить игру</button>
                  <div class="modal fade" id="deleteGameModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-sm">
                      <div class="modal-content">
                        <div class="modal-header">
                          <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                          <h4 class="modal-title" id="myModalLabel">Подтвердите действие</h4>
                        </div>
                        <div class="modal-body">
                          <p>Вы действительно хотите удалить игру?</p>
                        </div>
                        <div class="modal-footer">
                          <a class="btn btn-danger" href="/games/delete/{{game.game_id()}}">Удалить</a>
                          <button type="button" data-dismiss="modal" class="btn btn-primary">Отмена</button>
                        </div>
                      </div>
                    </div>
                  </div>
                % end
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-group">
              <label for="inputCity" class="col-sm-4 control-label text-left">Ответственный</label>
              <div class="col-sm-8">
                <select name="responsible_user_id" class="form-control" {{'disabled="disabled"' if game.reported() else ''}}>
                  % for user in responsibles:
                    % if user.user_id()!=current_user.user_id():
                      <option value="{{user.user_id()}}" {{'selected' if game.responsible_user_id()==user.user_id() else ''}}>{{user.name}}</option>
                    % end
                  % end
                  <option value="{{current_user.user_id()}}" {{'selected' if game.responsible_user_id()==current_user.user_id() else ''}}>Я сам{{'а' if current_user.sex()=='female' else ''}}</option>
                </select>
                <span id="valid"></span>
              </div>
            </div>
            % if not game.reported():
              <a class="btn btn-success" role="button" href="/games/list/{{game.game_id()}}"><span class="glyphicon glyphicon-print"></span>&nbsp;&nbsp;Распечатать списки на игру</a>
              <br><br>
              <a class="btn btn-success" data-toggle="modal" data-target="#otpisModal">
                Посмотреть отписавшихся
              </a>
              <br><br>
            % end
            % if not game.reported():
              <a class="btn btn-success" role="button" href="#"><span class="glyphicon glyphicon-send"></span>&nbsp;&nbsp;Пригласить бывших</a>
            <br><br>
            % end
            <a class="btn btn-success" role="button" href="/games/report/{{game.game_id()}}"><span class="glyphicon glyphicon-file"></span>&nbsp;&nbsp;
              {{'Смотреть отчет' if game.reported() else 'Заполнить отчет по игре'}}
            </a>
            <br><br>
         % end

            % if len(game.subscribed())>0:
                <label class="control-label">Список участников</label>
                <br>
                <div class="table-responsive">
                  <table class="table table-hover table-bordered">
                    % for n, user in enumerate(game.subscribed(True), 1):
                    <tr class="success">
                      <td>{{n}}</td>
                      <td>
                        <a href="/profile/{{user.user_id()}}" target="_blank">
                          {{user.name.first()}}
                        </a>
                      </td>
                      <td>
                        <a href="/profile/{{user.user_id()}}" target="_blank">
                          {{user.name.last()}}
                        </a>
                      </td>
                      <td>{{user.phone()}}</td>
                      <td>
                        % if not game.reported() and not game.datetime.passed:
                          <a href="/games/unsubscribe/{{game.game_id()}}/{{user.user_id()}}"><span class="glyphicon glyphicon-remove"></span></a>
                        % end
                      </td>
                    </tr>
                    % end
                    % for n, user in enumerate(game.reserved_people(True), 1):
                    <tr class="warning">
                      <td>{{n}}</td>
                      <td>
                        <a href="/profile/{{user.user_id()}}" target="_blank">
                          {{user.name.first()}}
                        </a>
                      </td>
                      <td>
                        <a href="/profile/{{user.user_id()}}" target="_blank">
                          {{user.name.last()}}
                        </a>
                      </td>
                      <td>{{user.phone()}}</td>
                      <td>
                        % if not game.reported() and not game.datetime.passed:
                          <a href="/games/unreserve/{{game.game_id()}}/{{user.user_id()}}"><span class="glyphicon glyphicon-remove"></span></a>
                        % end
                      </td>
                    </tr>
                    % end
                  </table>
                </div>
            % end
          </div>
        </div>
      </form>
    </div>
  </div>
</div>

<div class="modal fade" id="otpisModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Список отписавшихся</h4>
      </div>
      <div class="modal-body">
        <div class="table-responsive">
          <table class="table table-hover table-bordered">
            % for n, user in enumerate(game.subscribed(True), 1):
            <tr class="success">
              <td>{{n}}</td>
              <td>
                <a href="/profile/{{user.user_id()}}" target="_blank">
                  {{user.name.first()}}
                </a>
              </td>
              <td>
                <a href="/profile/{{user.user_id()}}" target="_blank">
                  {{user.name.last()}}
                </a>
              </td>
              <td>{{user.phone()}}</td>
              <td>
                Время
              </td>
            </tr>
            % end
          </table>
        </div>
      </div>
    </div>
  </div>
</div>