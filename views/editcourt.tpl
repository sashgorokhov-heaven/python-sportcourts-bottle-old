% rebase("_basicpage", title="Редактирование площадки")
      <div class="jumbotron">
        <div class="row">
          <div class="col-md-12 registration" style="text-align:left;">
            <h2 class="text-center">Редактирование площадки</h2><br>
            <form id="courtaddForm" method="post" class="form-horizontal"
            data-bv-message="This value is not valid" action="/courts"
            data-bv-feedbackicons-valid="glyphicon glyphicon-ok" enctype="multipart/form-data"
            data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
            data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
                <input type="hidden" name="court_id" value="{{court['court_id']}}">
                <div class="form-group">
                  <label for="first_name" class="col-sm-2 control-label">Название площадки</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="title" placeholder="" value="{{court['title']}}"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите название площадки" />
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="inlineCheckbox" class="col-sm-2 control-label">Вид спорта</label>
                  <div class="col-sm-10">
                  % for sport_type in sport_types:
                    <label class="checkbox-inline">
                      <input type="checkbox" name="sport_type" value="{{sport_type['sport_id']}}"
                      data-bv-message="Пожалуйста, выберите хотябы один вид спорта"
                      {{'checked' if sport_type['sport_id'] in {i['sport_id'] for i in court['sport_types']} else ''}}
                      data-bv-notempty="true"> {{sport_type['title']}}
                    </label>
                  % end
                  </div>
                </div>
                <div class="form-group">
                  <label for="inputCity" class="col-sm-2 control-label">Город</label>
                  <div class="col-sm-10">
                    <select id="city" name="city_id" class="form-control"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите город" <!-- Было бы прикольно onchange="showAddress(this.value);" --> >
                    <option value="{{court['city']['city_id']}}">{{court['city']['title']}}</option>
                    % for city in cities:
                        % if court['city']['city_id']!=city['city_id']:
                            <option value="{{city['city_id']}}">{{city['title']}}</option>
                        % end
                    % end
                    </select>
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="inputCity" class="col-sm-2 control-label">Адрес</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="address" value="court['address']"
                      data-bv-message="Пожалуйста, введите адрес"
                      data-bv-notempty="true"
                      onchange="showAddress(this.value);return false;"
                      id="address">
                    <div id="YMapsID" style="width:450px;height:300px;margin-top:20px;"></div>
                    <input type="hidden" id="geopoint" name="geopoint"/>
                  </div>
                </div>
                <div class="form-group">
                  <label for="sex" class="col-sm-2 control-label">Изображение площадки</label>
                  <div class="col-sm-10">
                    <script type="text/javascript">
                        $('.fileinput').fileinput()
                    </script>
                    <div class="fileinput fileinput-exists" data-provides="fileinput">
                      <div class="fileinput-preview thumbnail" data-trigger="fileinput" style="width: 150px; height: 150px;">
                        <img src="http://sportcourts.ru/images/courts/{{court['court_id']}}" alt="Изображение площадки" width="150">
                      </div>
                        <div>
                          <span class="btn btn-default btn-file">
                          <span class="fileinput-new">Выберите изображение</span>
                          <span class="fileinput-exists">Изменить</span>
                          <input type="file" name="photo" accept="images/*"></span>
                          <a href="#" class="btn btn-default fileinput-exists" data-dismiss="fileinput">Удалить</a>
                        </div>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="court_add_amount" class="col-sm-2 control-label">Аренда</label>
                  <div class="col-sm-10">
                    <input type="text" value="" name="cost" id="court_add_amount" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0); width:150%;">
                    <div id="court_add_slider"></div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="court_add_count" class="col-sm-2 control-label">Вместимость</label>
                  <div class="col-sm-10">
                    <input type="text" value="" name="max_players" id="court_add_count" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                    <div id="court_add_slider1"></div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="first_name" class="col-sm-2 control-label">Время работы</label>
                  <div class="col-sm-10">
                    <input type="text" value="{{court['worktime']}}" class="form-control" name="worktime" placeholder="С 9:00 до 18:30"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Напишите время работы" />
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="first_name" class="col-sm-2 control-label">Тип площадки</label>
                  <div class="col-sm-10">
                    <input type="text"  value="{{court['type']}}" class="form-control" name="type" placeholder="Крытая/откртырая"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Напишите тип площадки" />
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="first_name" class="col-sm-2 control-label">Покрытие</label>
                  <div class="col-sm-10">
                    <input type="text" value="{{court['cover']}}" class="form-control" name="cover" placeholder="Асфальт"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите покрытие площадки" />
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="first_name" class="col-sm-2 control-label">Инфраструктура</label>
                  <div class="col-sm-10">
                    <input type="text"  value="{{court['infrastructure']}}" class="form-control" name="infrastructure" placeholder="Минибар, телевизор, душ"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Ну хоть что нибудь" />
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="first_name" class="col-sm-2 control-label">Телефон</label>
                  <div class="col-sm-10">
                    <input type="text" value="{{court['phone']}}" class="form-control" name="phone" placeholder="355-455"/>
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="court_add_count" class="col-sm-2 control-label">Описание</label>
                  <div class="col-sm-10">
                    <textarea class="form-control" name="description" rows="3">{{court['description']}}</textarea>
                  </div>
                </div>
                <div class="form-group">
                  <div class="col-sm-offset-2 col-sm-8" style="text-align:center;">
                    <button type="submit" name="submit_edit" class="btn btn-primary">Редактировать</button>
                  </div>
                </div>
            </form>
          </div>
        </div>
      </div>
