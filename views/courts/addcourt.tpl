% rebase("_basicpage", title="Добавить площадку")
      <div class="jumbotron">
        <div class="row">
          <div class="col-md-12 registration" style="text-align:left;">
            <h2 class="text-center">Новая площадка</h2><br>
            <form id="courtaddForm" method="post" class="form-horizontal"
            data-bv-message="This value is not valid" action="/courts/add"
            data-bv-feedbackicons-valid="glyphicon glyphicon-ok" enctype="multipart/form-data"
            data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
            data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
                <div class="form-group">
                  <label for="first_name" class="col-sm-2 control-label">Название площадки</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="title" placeholder=""
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
                      <input type="checkbox" name="sport_type" value="{{sport_type.sport_id()}}" data-bv-message="Пожалуйста, выберите хотябы один вид спорта"
                      data-bv-notempty="true">
                      {{sport_type.title()}}
                    </label>
                  % end
                  </div>
                </div>
                <div class="form-group">
                  <label for="inputCity" class="col-sm-2 control-label">Город</label>
                  <div class="col-sm-10">
                    <select id="city" name="city_id" class="form-control"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите город">
                    % for city in cities:
                      <option value="{{city.city_id()}}">{{city.title()}}</option>
                    % end
                    </select>
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="inputCity" class="col-sm-2 control-label">Адрес</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="address"
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
                    <div class="fileinput fileinput-new" data-provides="fileinput">
                      <div class="fileinput-preview thumbnail" data-trigger="fileinput" style="width: 150px; height: 150px;">
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
                    <input type="text" name="cost" id="court_add_amount" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0); width:150%;">
                    <div id="court_add_slider"></div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="court_add_count" class="col-sm-2 control-label">Вместимость</label>
                  <div class="col-sm-10">
                    <input type="text" name="max_players" id="court_add_count" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                    <div id="court_add_slider1"></div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="first_name" class="col-sm-2 control-label">Время работы</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="worktime" placeholder="С 9:00 до 18:30"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Напишите время работы" />
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="inlineCheckbox" class="col-sm-2 control-label">Тип площадки</label>
                  <div class="col-sm-10">
                    <select id="courttype" name="type" class="form-control" data-bv-notempty="true"
                    data-bv-notempty-message="Укажите тип площадки">
                      <option value="">--</option>
                      % for type in court_types:
                        <option value="{{type.type_id()}}">{{type.title()}}</option>
                      % end
                    </select>
                  </div>
                </div>
                <div class="form-group">
                  <label for="first_name" class="col-sm-2 control-label">Покрытие</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="cover" placeholder="Асфальт"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите покрытие площадки" />
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="first_name" class="col-sm-2 control-label">Инфраструктура</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="infrastructure" placeholder="Минибар, телевизор, душ"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Ну хоть что нибудь" />
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="first_name" class="col-sm-2 control-label">Телефон</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="phone" placeholder="355-455"/>
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="court_add_count" class="col-sm-2 control-label">Описание</label>
                  <div class="col-sm-10">
                    <textarea class="form-control" name="description" rows="3"></textarea>
                  </div>
                </div>
                <div class="form-group panel panel-primary">
                  <label for="court_add_count" class="col-sm-2 control-label">Комментарии админа</label>
                  <div class="col-sm-10">
                    <textarea class="form-control" name="admin_description" rows="3"></textarea>
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
