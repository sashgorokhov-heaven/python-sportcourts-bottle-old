% rebase("_basicpage", title="Редактировать игру")
      <div class="jumbotron">
        <div class="row">
          <div class="col-md-12 registration" style="text-align:left;">
            <h2 class="text-center">Редактирование игры</h2><br>
            <div class="row">
              <div class="col-md-6">
                <form id="gameaddForm" method="post" class="form-horizontal" action="/games"
                data-bv-message="This value is not valid" enctype="multipart/form-data"
                data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
                data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
                data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
                <input type="hidden" name="game_id" value="{{game['game_id']}}">
                    <div class="form-group">
                      <label for="inlineCheckbox" class="col-sm-4 control-label">Вид спорта</label>
                      <div class="col-sm-8">
                        <select id="sporttype" name="sport_type" class="form-control" data-bv-notempty="true"
                        data-bv-notempty-message="Укажите вид спорта">
                          <option value="{{game['sport_type']['sport_id']}}">{{game['sport_type']['title']}}</option>
                          % for sport_id, title in sports:
                            % if sport_id != game['sport_type']['sport_id']:
                              <option value="{{sport_id}}">{{title}}</option>
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
                          % for type_id, sport_id, title in game_types:
                            % if type_id != game['game_type']['type_id']:
                              <option value="{{type_id}}" class="{{sport_id}}">{{title}}</option>
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
                        % for city_id, title in cities:
                            % if city_id != game['city']['city_id']:
                              <option value="{{city_id}}">{{title}}</option>
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
                          % for court_id, city_id, title in courts:
                            % if court_id!=game['court']['court_id']:
                              <option value="{{court_id}}" class="{{city_id}}">{{title}}</option>
                            % end
                          % end
                        </select>
                      </div>
                    </div>
                    <script type="text/javascript">
                      $("#court").chained("#city");
                    </script>
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
                        <input type="text" id="game_add_long" value="{{game['duration']}}" name="duration" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                        <div id="game_add_slider2"></div>
                      </div>
                    </div>
                    <div class="form-group">
                      <label for="game_add_amount" class="col-sm-4 control-label">Цена</label>
                      <div class="col-sm-8">
                        <input type="text" id="game_add_amount"  value="{{game['cost']}}" name="cost" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                        <div id="game_add_slider"></div>
                      </div>
                    </div>
                    <div class="form-group">
                      <label for="game_add_count" class="col-sm-4 control-label">Количество мест</label>
                      <div class="col-sm-8">
                        <input type="text" id="game_add_count" value="{{game['capacity']}}" name="capacity" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                        <div id="game_add_slider1"></div>
                      </div>
                    </div>
                    <div class="form-group">
                      <label for="court_add_count" class="col-sm-4 control-label">Описание</label>
                      <div class="col-sm-8">
                        <textarea class="form-control" name="description" rows="3">{{game['description']}}</textarea>
                      </div>
                    </div>
                    <div class="form-group">
                      <div class="col-sm-offset-2 col-sm-8" style="text-align:center;">
                        <button type="submit" name="submit_edit" class="btn btn-primary">Применить</button>
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
                                <a class="btn btn-danger" href="/games?delete={{game['game_id']}}"></a>
                                <button type="button" data-dismiss="modal" class="btn btn-primary">Отмена</button>
                              </div>
                            </div>
                          </div>
                        </div>
                        <script type="text/javascript">
                          $('#deleteGameModal').modal(options)
                        </script>
                      </div>
                    </div>
                </form>
              </div>
              <div class="col-md-6">
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
                          <td><a href="/subscribe?unsubscribe&fromedit&game_id={{game['game_id']}}"><span class="glyphicon glyphicon-remove"></span></a></td>
                        </tr>
                        % end
                      </table>
                    </div>
                % end
              </div>
            </div>
          </div>
        </div>
      </div>