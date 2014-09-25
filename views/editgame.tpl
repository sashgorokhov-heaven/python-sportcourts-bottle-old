% rebase("_basicpage", title="Редактировать игру")
      <div class="jumbotron">
        <div class="row">
          <div class="col-md-12 registration" style="text-align:left;">
            <h2 class="text-center">Редактирование игры №{{game['game_id']}}</h2><br>
            <form id="gameaddForm" method="post" class="form-horizontal" action="/games"
            data-bv-message="This value is not valid" enctype="multipart/form-data"
            data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
            data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
            data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
              <div class="row">
              % if game['created_by']['user_id']==userinfo['user_id'] or userinfo['admin']:
                <div class="col-md-6">
                  <input type="hidden" name="game_id" value="{{game['game_id']}}">
                  <div class="form-group">
                    <label for="court_add_count" class="col-sm-4 control-label">Название</label>
                    <div class="col-sm-8">
                      <input class="form-control" type="text" name="description" value="{{game['description']}}"/>
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="inlineCheckbox" class="col-sm-4 control-label">Вид спорта</label>
                    <div class="col-sm-8">
                      <select id="sporttype" name="sport_type" class="form-control" data-bv-notempty="true"
                      data-bv-notempty-message="Укажите вид спорта">
                        <option value="{{game['sport_type']['sport_id']}}">{{game['sport_type']['title']}}</option>
                        % for sport_type in sports:
                          % if sport_type['sport_id'] != game['sport_type']['sport_id']:
                            <option value="{{sport_type['sport_id']}}">{{sport_type['title']}}</option>
                          % end
                        % end
                      </select>
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="inlineCheckbox" class="col-sm-4 control-label">Тип игры</label>
                    <div class="col-sm-8">
                      <select id="gametype" name="game_type" class="form-control" data-bv-notempty="true"
                      data-bv-notempty-message="Укажите тип игры">
                        <option value="{{game['game_type']['type_id']}}" class="{{game['game_type']['sport_type']}}">{{game['game_type']['title']}}</option>
                        % for type in game_types:
                          % if type['type_id'] != game['game_type']['type_id']:
                            <option value="{{type['type_id']}}" class="{{type['sport_type']}}">{{type['title']}}</option>
                          % end
                        % end
                      </select>
                    </div>
                  </div>
                  <script type="text/javascript">
                    $("#gametype").chained("#sporttype");
                  </script>
                  <div class="form-group">
                    <label for="inputCity" class="col-sm-4 control-label">Город</label>
                    <div class="col-sm-8">
                      <select id="city" name="city_id" class="form-control"
                      data-bv-notempty="true"
                      data-bv-notempty-message="Укажите город">
                      <option value="{{game['city']['city_id']}}">{{game['city']['title']}}</option>
                      % for city in cities:
                          % if city['city_id'] != game['city']['city_id']:
                            <option value="{{city['city_id']}}">{{city['title']}}</option>
                          % end
                      % end
                      </select>
                      <span id="valid"></span>
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="inputBirght" class="col-sm-4 control-label">Площадка</label>
                    <div class="col-sm-8">
                      <select id="court" name="court_id" class="form-control"
                      data-bv-notempty="true"
                      data-bv-notempty-message="Укажите площадку">
                        <option value="{{game['court']['court_id']}}" class="{{game['court']['city_id']}}">{{game['court']['title']}}</option>
                        % for court in courts:
                          % if court['court_id']!=game['court']['court_id']:
                            <option value="{{court['court_id']}}" class="{{court['city_id']}}">{{court['title']}}</option>
                          % end
                        % end
                      </select>
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="inputBirght" class="col-sm-4 control-label">Дата</label>
                    <div class="col-sm-8">
                      <input type="date" class="form-control" name="date"
                      data-bv-notempty="true" value="{{game['datetime'].split(' ')[0]}}"
                      data-bv-notempty-message="Укажите дату проведения" />
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="inputBirght" class="col-sm-4 control-label">Начало</label>
                    <div class="col-sm-6">
                      <input type="time" class="form-control" name="time"
                      data-bv-notempty="true" value="{{':'.join(game['datetime'].split(' ')[-1].split(':')[:2])}}"
                      data-bv-notempty-message="Укажите время начала" />
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="game_add_long" class="col-sm-4 control-label">Длительность</label>
                    <div class="col-sm-8">
                      <input type="text" id="game_add_long_visible" name="durationv" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                      <div id="game_add_slider2"></div>
                      <input type="hidden" id="game_add_long" name="duration" readonly>
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="game_add_amount" class="col-sm-4 control-label">Цена</label>
                    <div class="col-sm-8">
                      <input type="text" id="game_add_amount_visible" name="costv" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                      <div id="game_add_slider"></div>
                      <input type="hidden" id="game_add_amount" name="cost" readonly>
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="game_add_count" class="col-sm-4 control-label">Количество мест</label>
                    <div class="col-sm-8">
                      <input type="text" id="game_add_count_visible" name="capacityv" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                      <div id="game_add_slider1"></div>
                      <input type="hidden" id="game_add_count" name="capacity" readonly>
                    </div>
                    <div class="col-sm-8">
                      <div class="checkbox">
                        <label>
                          <input type="checkbox" id="unlimit" name="unlimit" value="-1" onchange="showOrHide();">Безлимитно
                        </label>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <div class="col-sm-offset-2 col-sm-8" style="text-align:center;">
                      <button type="submit" name="submit_edit" class="btn btn-primary">Применить</button>
                      % if userinfo['user_id']==game['created_by']['user_id'] or userinfo['admin']:
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
                                <a class="btn btn-danger" href="/games?delete={{game['game_id']}}">Удалить</a>
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
                      <select name="responsible_user_id" class="form-control">
                        % for user in responsibles:
                          % if user['user_id']!=userinfo["user_id"]:
                            <option value="{{user['user_id']}}" {{'selected' if game['responsible_user']['user_id']==user['user_id'] else ''}}>{{user['first_name']}} {{user['last_name']}}</option>
                          % end
                        % end
                        <option value="{{userinfo["user_id"]}}" {{'selected' if game['responsible_user']['user_id']==userinfo['user_id'] else ''}}>Я сам{{'а' if userinfo["usersex"]=='female' else ''}}</option>
                      </select>
                      <span id="valid"></span>
                    </div>
                  </div>
               % end
               % if game['created_by']['user_id']!=userinfo['user_id'] and not userinfo['admin']:
               	<div class="col-md-6">
               % end
                  % if game['subscribed']['count']>0:
                      <label class="control-label">Список участников</label>
                      <br>
                      <div class="table-responsive">
                        <table class="table table-hover table-bordered">
                          % for n, user in enumerate(game['subscribed']['users'], 1):
                          <tr class="success">
                            <td>{{n}}</td>
                            <td>{{user['first_name']}}</td>
                            <td>{{user['last_name']}}</td>
                            <td>{{user['phone']}}</td>
                            <td><a href="/subscribe?user_id={{user['user_id']}}&unsubscribe&game_id={{game['game_id']}}"><span class="glyphicon glyphicon-remove"></span></a></td>
                          </tr>
                          % end
                        </table>
                      </div>
                  % end
                  <a class="btn btn-success" role="button" href="/list/{{game['game_id']}}">Распечатать списки на игру</a>
                  <br><br>
                  <a class="btn btn-success" role="button" href="/report?game_id={{game['game_id']}}">Заполнить отчет по игре</a>
                </div>
              </div>
            </form>
          </div>
        </div>

        <!--<div class="row">
          <div class="col-md-8 col-md-offset-2">
            <h3>Для ответственного</h3>
            % if game['subscribed']['count']>0:
                <label class="control-label" style="float:left;">Список участников</label>
                <br>
                <div class="table-responsive">
                  <table class="table table-hover table-bordered">
                    % for n, user in enumerate(game['subscribed']['users'], 1):
                    <tr class="success">
                      <td>{{n}}</td>
                      <td>{{user['first_name']}}</td>
                      <td>{{user['last_name']}}</td>
                      <td>{{user['phone']}}</td>
                      <td><a href="/subscribe?user_id={{user['user_id']}}&unsubscribe&game_id={{game['game_id']}}"><span class="glyphicon glyphicon-remove"></span></a></td>
                    </tr>
                    % end
                  </table>
                </div>
            % end
          </div>
        </div> -->
      </div>