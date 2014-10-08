% rebase("_basicpage", title="Изменение профиля")

      <div class="row profile">
        <div class="col-md-12">
          <form id="profileForm" method="post" class="form-horizontal" action="/profile"
            data-bv-message="This value is not valid"  enctype="multipart/form-data"
            data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
            data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
            data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
                <div class="form-group">
                  <label for="sex" class="col-sm-2 control-label">Фото</label>
                  <div class="col-sm-10">
                    <div class="fileinput fileinput-{{!'exists' if haveavatar else 'new'}}" data-provides="fileinput">
                      <div class="fileinput-preview thumbnail" data-trigger="fileinput" style="width: 150px; height: 150px;">
                      % if haveavatar:
                          <img src="/images/avatars/{{user.user_id()}}" alt="avatar" width="150" >
                      % end
                      </div>
                        <div>
                          <span class="btn btn-default btn-file">
                          <span class="fileinput-new">Выберите изображение</span>
                          <span class="fileinput-exists">Изменить</span>
                          <input type="file" name="avatar" accept="images/*"></span>
                          <a href="#" class="btn btn-default fileinput-exists" data-dismiss="fileinput">Удалить</a>
                        </div>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="height" class="col-sm-2 control-label">Рост</label>
                  <div class="col-sm-2">
                    <input type="text" class="form-control" name="height" value="{{user.height()}}"
                    min="150"
                    data-bv-greaterthan-inclusive="true"
                    data-bv-greaterthan-message="Это мало"

                    max="230"
                    data-bv-lessthan-inclusive="false"
                    data-bv-lessthan-message="Ты гигант?)"

                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите рост"

                    pattern="[0-9]"
                    data-bv-regexp-message="Рост указывается числом"
                    />
                  </div>
                </div>
                <div class="form-group">
                  <label for="weight" class="col-sm-2 control-label">Вес</label>
                  <div class="col-sm-2">
                    <input type="text" class="form-control" name="weight" value="{{user.weight()}}"
                    min="30"
                    data-bv-greaterthan-inclusive="true"
                    data-bv-greaterthan-message="Это мало"

                    max="230"
                    data-bv-lessthan-inclusive="false"
                    data-bv-lessthan-message="Ты гигант?)"

                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите вес"

                    pattern="[0-9]"
                    data-bv-regexp-message="Вес указывается числом"
                    />
                  </div>
                </div>
                <div class="form-group">
                  <label for="phone" class="col-sm-2 control-label">Телефон</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control phonemask" name="phone" placeholder="" id="phone" value="{{user.phone()}}" data-bv-notempty="true" data-bv-notempty-message="Укажите телефон"></input>
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="city" class="col-sm-2 control-label">Город</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control typeahead" name="city" value="{{user.city_id(True).title() if user.city_id(True).title() in {i.title() for i in cities} else 'Екатеринбург'}}" data-provide="typeahead" data-bv-notempty="true" data-bv-notempty-message="Укажите город"/>
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="" class="col-sm-2 control-label">Амплуа</label>
                  <div class="col-sm-10">
                    <select data-placeholder="Выберите любимые амплуа"  multiple="multiple" class="form-control chosen-select chosen-select-1" tabindex="-1" name="ampluas[]">
                      <option value=""></option>
                      % for sport_type_title in ampluas:
                        <optgroup label="{{sport_type_title}}">
                        % for amplua in ampluas[sport_type_title]:
                            <option value="{{amplua.amplua_id()}}" {{!'selected' if amplua.amplua_id() in set(user.ampluas()) else ''}}>{{sport_type_title}}: {{amplua.title()}}</option>
                        % end
                      % end
                    </select>
                    <script>
                      $(".chosen-select").chosen({
                        disable_search: true,
                        max_selected_options: 5
                      });
                    </script>
                  </div>
                </div>
                <br>
                <hr>
                <br>
                <div class="form-group">
                  <div class="col-sm-offset-2 col-sm-8" style="text-align:center;">
                    <button type="submit" class="btn btn-primary">Редактировать информацию</button>
                  </div>
                </div>
            </form>
        </div>
      </div>