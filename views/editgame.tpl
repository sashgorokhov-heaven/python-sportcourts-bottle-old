% rebase("_basicpage", title="Редактировать игру")
      <div class="jumbotron">
        <div class="row">
          <div class="col-md-12 registration" style="text-align:left;">
            <h2 class="text-center">Редактирование игры</h2><br>
            <form id="gameaddForm" method="post" class="form-horizontal" action="/games"
            data-bv-message="This value is not valid"
            data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
            data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
            data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
                <div class="form-group">
                  <label for="inlineCheckbox" class="col-sm-2 control-label">Вид спорта</label>
                  <div class="col-sm-10">
                    <select name="sport" class="form-control"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите вид спорта">
                    <option value="{{game['sport_type']['sport_id']}}">{{game['sport_type']['title']}}</option>
                    % for sport_id, title in sports:
                        % if sport_id != game['sport_type']['sport_id']:
                          <option value="{{sport_id}}">{{title}}</option>
                        % end
                    % end
                    </select>
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="inlineCheckbox" class="col-sm-2 control-label">Тип игры</label>
                  <div class="col-sm-10">
                    <select name="game_type" class="form-control"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите тип игры">
                    <option value="{{game['game_type']['type_id']}}">{{game['game_type']['title']}}</option>
                    % for type_id, title in game_types:
                        % if type_id != game['game_type']['type_id']:
                            <option value="{{type_id}}">{{title}}</option>
                        % end
                    % end
                    </select>
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="inputCity" class="col-sm-2 control-label">Город</label>
                  <div class="col-sm-10">
                    <select name="city" class="form-control"
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
                  <label for="inputBirght" class="col-sm-2 control-label">Площадка</label>
                  <div class="col-sm-10">
                    <select name="place" class="form-control"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите площадку">
                    <option value="{{game['court']['court_id']}}">{{game['court']['title']}}</option>
                      % for court_id, title in courts:
                        % if game['court']['court_id'] != court_id:
                            <option value="{{game['court']['court_id']}}">{{game['court']['title']}}</option>
                        % end
                      % end
                    </select>
                  </div>
                </div>
                <div class="form-group">
                  <label for="inputBirght" class="col-sm-2 control-label">Дата</label>
                  <div class="col-sm-10">
                    <input type="date" class="form-control" name="date" value="{{game['datetime'].split(' ')[0]}}"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите время проведения" />
                  </div>
                </div>
                <div class="form-group">
                  <label for="inputBirght" class="col-sm-2 control-label">Начало</label>
                  <div class="col-sm-4">
                    <input type="time" class="form-control" name="time" value="{{game['datetime'].split(' ')[1]}}"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите время начала" />
                  </div>
                </div>
                <div class="form-group">
                  <label for="game_add_long" class="col-sm-2 control-label">Длительность</label>
                  <div class="col-sm-10">
                    <input type="text" id="game_add_long" value="{{game['duration']}}" name="duration" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                    <div id="game_add_slider2"></div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="game_add_amount" class="col-sm-2 control-label">Цена</label>
                  <div class="col-sm-10">
                    <input type="text" id="game_add_amount" name="cost" value="{{game['cost']}}" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                    <div id="game_add_slider"></div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="game_add_count" class="col-sm-2 control-label">Количество мест</label>
                  <div class="col-sm-10">
                    <input type="text" id="game_add_count" name="capacity" value="{{game['capacity']}}" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                    <div id="game_add_slider1"></div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="court_add_count" class="col-sm-2 control-label">Описание</label>
                  <div class="col-sm-10">
                    <textarea class="form-control" name="description" value="{{game['description']}}" rows="3"></textarea>
                  </div>
                </div>
                <div class="form-group">
                  <div class="col-sm-offset-2 col-sm-8" style="text-align:center;">
                    <button type="submit" name="submit_edit" class="btn btn-primary">Применить</button>
                  </div>
                </div>
            </form>
          </div>
        </div>
      </div>