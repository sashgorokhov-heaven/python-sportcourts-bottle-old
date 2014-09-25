% rebase("_basicpage", title="Добавить игру")
      <div class="jumbotron">
        <div class="row">
          <div class="col-md-12 registration" style="text-align:left;">
            <h2 class="text-center">Новая игра</h2><br>
            <form id="gameaddForm" method="post" class="form-horizontal" action="/games"
            data-bv-message="This value is not valid" enctype="multipart/form-data"
            data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
            data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
            data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
                <div class="form-group">
                  <label for="court_add_count" class="col-sm-2 control-label">Название</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="description" />
                  </div>
                </div>
                <div class="form-group">
                  <label for="inlineCheckbox" class="col-sm-2 control-label">Вид спорта</label>
                  <div class="col-sm-10">
                    <select id="sporttype" name="sport_type" class="form-control" data-bv-notempty="true"
                    data-bv-notempty-message="Укажите вид спорта">
                      <option value="">--</option>
                      % for sport_type in sports:
                          <option value="{{sport_type['sport_id']}}">{{sport_type['title']}}</option>
                      % end
                    </select>
                  </div>
                </div>
                <div class="form-group">
                  <label for="inlineCheckbox" class="col-sm-2 control-label">Тип игры</label>
                  <div class="col-sm-10">
                    <select id="gametype" name="game_type" class="form-control" data-bv-notempty="true"
                    data-bv-notempty-message="Укажите тип игры">
                      <option value="">--</option>
                      % for type in game_types:
                        <option value="{{type['type_id']}}" class="{{type['sport_type']}}">{{type['title']}}</option>
                      % end
                    </select>
                  </div>
                </div>
                <script>
                  $("#gametype").chained("#sporttype");
                </script>
                <div class="form-group">
                  <label for="inputCity" class="col-sm-2 control-label">Город</label>
                  <div class="col-sm-10">
                    <select id="city" name="city_id" class="form-control"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите город">
                    % for city in cities:
                      <option value="{{city['city_id']}}">{{city['title']}}</option>
                    % end
                    </select>
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="inputBirght" class="col-sm-2 control-label">Площадка</label>
                  <div class="col-sm-10">
                    <select id="court" name="court_id" class="form-control"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите площадку">
                      <option value="">--</option>
                      % for court in courts:
                        <option value="{{court['court_id']}}" class="{{court['city_id']}}">{{court['title']}}</option>
                      % end
                    </select>
                    <small><a href="/courts?add">Создать новую...</a></small>
                  </div>
                </div>
                <script>
                  $("#court").chained("#city");
                </script>
                <div class="form-group">
                  <label for="inputBirght" class="col-sm-2 control-label">Дата</label>
                  <div class="col-sm-10">
                    <input type="date" class="form-control" name="date"
                    data-bv-notempty="true" value="{{str(current.date())}}"
                    data-bv-notempty-message="Укажите дату проведения" />
                  </div>
                </div>
                <div class="form-group">
                  <label for="inputBirght" class="col-sm-2 control-label">Начало</label>
                  <div class="col-sm-4">
                    <input type="time" class="form-control" name="time"
                    data-bv-notempty="true" value="{{str(current.time()).split('.')[0]}}"
                    data-bv-notempty-message="Укажите время начала" />
                  </div>
                </div>
                <div class="form-group">
                  <label for="game_add_long" class="col-sm-2 control-label">Длительность</label>
                  <div class="col-sm-10">
                    <input type="text" id="game_add_long_visible" name="duration" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                    <div id="game_add_slider2"></div>
                    <input type="hidden" id="game_add_long" name="capacity" readonly>
                  </div>
                </div>
                <div class="form-group">
                  <label for="game_add_amount" class="col-sm-2 control-label">Цена</label>
                  <div class="col-sm-10">
                    <input type="text" id="game_add_amount_visible" name="cost" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                    <div id="game_add_slider"></div>
                    <input type="hidden" id="game_add_amount" name="capacity" readonly>
                  </div>
                </div>
                <div class="form-group">
                  <label for="game_add_count" class="col-sm-2 control-label">Количество мест</label>
                  <div class="col-sm-10">
                    <input type="text" id="game_add_count_visible" name="capacity" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                    <div id="game_add_slider1"></div>
                    <input type="hidden" id="game_add_count" name="capacity" readonly>
                    <div class="checkbox">
                      <label>
                        <input type="checkbox" id="unlimit" name="unlimit" value="-1" onchange="showOrHide();">Безлимитно
                      </label>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="game_add_count" class="col-sm-2 control-label">Ответственный</label>
                  <div class="col-sm-10">
                      <select name="responsible_user_id" class="form-control">
                      <option value="{{userinfo["user_id"]}}" selected>Я сам{{'а' if userinfo["usersex"]=='female' else ''}}</option>
                        % for user in responsibles:
                          % if user['user_id']!=userinfo["user_id"]:
                            <option value="{{user['user_id']}}">{{user['first_name']}} {{user['last_name']}}</option>
                          % end
                        % end
                      </select>
                  </div>
                </div>
                <div class="form-group">
                  <div class="col-sm-offset-2 col-sm-8" style="text-align:center;">
                    <button type="submit" name="submit_add" class="btn btn-primary">Создать</button>
                  </div>
                </div>
            </form>
          </div>
        </div>
      </div>