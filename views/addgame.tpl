% rebase("_basicpage", title="Добавить игру")
      <div class="jumbotron">
        <div class="row">
          <div class="col-md-12 registration" style="text-align:left;">
            <h2 class="text-center">Новая игра</h2><br>
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
                    % for sport_id, title in sports:
                      <option value="{{sport_id}}">{{title}}</option>
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
                    % for type_id, title in game_types:
                      <option value="{{type_id}}">{{title}}</option>
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
                    % for city_id, title in cities:
                      <option value="{{city_id}}">{{title}}</option>
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
                      % for court_id, title in courts:
                      <option value="{{court_id}}">{{title}}</option>
                      % end
                    </select>
                  </div>
                </div>
                <div class="form-group">
                  <label for="inputBirght" class="col-sm-2 control-label">Дата</label>
                  <div class="col-sm-10">
                    <input type="date" class="form-control" name="date"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите время проведения" />
                  </div>
                </div>
                <div class="form-group">
                  <label for="inputBirght" class="col-sm-2 control-label">Начало</label>
                  <div class="col-sm-4">
                    <input type="time" class="form-control" name="time"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите время начала" />
                  </div>
                </div>
                <div class="form-group">
                  <label for="game_add_long" class="col-sm-2 control-label">Длительность</label>
                  <div class="col-sm-10">
                    <input type="text" id="game_add_long" name="duration" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                    <div id="game_add_slider2"></div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="game_add_amount" class="col-sm-2 control-label">Цена</label>
                  <div class="col-sm-10">
                    <input type="text" id="game_add_amount" name="cost" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                    <div id="game_add_slider"></div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="game_add_count" class="col-sm-2 control-label">Количество мест</label>
                  <div class="col-sm-10">
                    <input type="text" id="game_add_count" name="capacity" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                    <div id="game_add_slider1"></div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="court_add_count" class="col-sm-2 control-label">Описание</label>
                  <div class="col-sm-10">
                    <textarea class="form-control" name="description" rows="3"></textarea>
                  </div>
                </div>
                <div class="form-group">
                  <div class="col-sm-offset-2 col-sm-8" style="text-align:center;">
                    <button type="submit" name="submit_game_add" class="btn btn-primary">Создать</button>
                  </div>
                </div>
            </form>
          </div>
        </div>
      </div>