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
                    <div class="fileinput fileinput-{{'exists' if haveavatar else 'new'}}" data-provides="fileinput">
                      <div class="fileinput-preview thumbnail" data-trigger="fileinput" style="width: 150px; height: 150px;">
                      % if haveavatar:
                          <img src="/images/avatars/{{str(user['user_id'])}}" alt="User avatar" width="150" >
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
                <!-- <div class="form-group">
                  <label for="sex" class="col-sm-2 control-label">Пол</label>
                  <div class="col-sm-10">
                    <label class="checkbox-inline" style="margin-left:-17px;">
                      <input type="radio" name="sex" value="male" {{'checked' if user['sex']=='male' else ''}}
                      data-bv-message="Пожалуйста, выберите пол"
                      data-bv-notempty="true"> Мужской
                    </label>
                    <label class="checkbox-inline">
                      <input type="radio" name="sex" value="female" {{'checked' if user['sex']=='female' else ''}}> Женский
                    </label>
                  </div>
                </div>
                <div class="form-group">
                  <label for="last_name" class="col-sm-2 control-label">Фамилия</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="last_name" placeholder="" value="{{user['last_name']}}"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Поле фамилии не может быть пустым" />
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="first_name" class="col-sm-2 control-label">Имя</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="first_name" placeholder="" value="{{user['first_name']}}"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Поле имени не может быть пустым" />
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="middle_name" class="col-sm-2 control-label">Отчество</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="middle_name" value="{{user['middle_name']}}"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Поле отчества не может быть пустым" />
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="city" class="col-sm-2 control-label">Город</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control typeahead" name="city" value="{{user['city']['title'] if user['city']['title'] in {i['title'] for i in cities} else 'Екатеринбург'}}" data-provide="typeahead" data-bv-notempty="true" data-bv-notempty-message="Укажите город"/>
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="bdate" class="col-sm-2 control-label">Дата рождения</label>
                  <div class="col-sm-10">
                    <input type="date" class="form-control" name="bdate" value="{{user['bdate']}}"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите дату рождения" />
                  </div>
                </div> -->
                <div class="form-group">
                  <label for="height" class="col-sm-2 control-label">Рост</label>
                  <div class="col-sm-2">
                    <input type="text" class="form-control" name="height" value="{{user['height']}}"
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
                    <input type="text" class="form-control" name="weight" value="{{user['weight']}}"
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
                    <input type="text" class="form-control phonemask" name="phone" placeholder="" id="phone" value="{{user['phone']}}" data-bv-notempty="true" data-bv-notempty-message="Укажите телефон"></input>
                    <span id="valid"></span>
                  </div>
                </div>
                <!-- -webkit-appearance: none;
                -webkit-box-shadow: rgba(0, 0, 0, 0.0745098) 0px 1px 1px 0px inset;
                -webkit-rtl-ordering: logical;
                -webkit-transition-delay: 0s, 0s;
                -webkit-transition-duration: 0.15s, 0.15s;
                -webkit-transition-property: border-color, box-shadow;
                -webkit-transition-timing-function: ease-in-out, ease-in-out;
                -webkit-user-select: text;
                -webkit-writing-mode: horizontal-tb;
                background-color: rgb(255, 255, 255);
                background-image: none;
                border-bottom-color: rgb(204, 204, 204);
                border-bottom-left-radius: 4px;
                border-bottom-right-radius: 4px;
                border-bottom-style: solid;
                border-bottom-width: 1px;
                border-image-outset: 0px;
                border-image-repeat: stretch;
                border-image-slice: 100%;
                border-image-source: none;
                border-image-width: 1;
                border-left-color: rgb(204, 204, 204);
                border-left-style: solid;
                border-left-width: 1px;
                border-right-color: rgb(204, 204, 204);
                border-right-style: solid;
                border-right-width: 1px;
                border-top-color: rgb(204, 204, 204);
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border-top-style: solid;
                border-top-width: 1px;
                box-shadow: rgba(0, 0, 0, 0.0745098) 0px 1px 1px 0px inset;
                box-sizing: border-box;
                color: rgb(85, 85, 85);
                cursor: auto;
                display: block;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-size: 14px;
                font-style: normal;
                font-variant: normal;
                font-weight: normal;
                height: 34px;
                letter-spacing: normal;
                line-height: 20px;
                margin-bottom: 0px;
                margin-left: 0px;
                margin-right: 0px;
                margin-top: 0px;
                padding-bottom: 6px;
                padding-left: 12px;
                padding-right: 42.5px;
                padding-top: 6px;
                text-align: start;
                text-indent: 0px;
                text-shadow: none;
                text-transform: none;
                transition-delay: 0s, 0s;
                transition-duration: 0.15s, 0.15s;
                transition-property: border-color, box-shadow;
                transition-timing-function: ease-in-out, ease-in-out;
                width: 786.65625px;
                word-spacing: 0px;
                writing-mode: lr-tb;


                -webkit-box-shadow: rgba(0, 0, 0, 0.298039) 0px 0px 5px 0px;
                background-color: rgb(255, 255, 255);
                background-image: linear-gradient(rgb(238, 238, 238) 1%, rgb(255, 255, 255) 15%);
                border-bottom-color: rgb(88, 151, 251);
                border-bottom-style: solid;
                border-bottom-width: 1px;
                border-image-outset: 0px;
                border-image-repeat: stretch;
                border-image-slice: 100%;
                border-image-source: none;
                border-image-width: 1;
                border-left-color: rgb(88, 151, 251);
                border-left-style: solid;
                border-left-width: 1px;
                border-right-color: rgb(88, 151, 251);
                border-right-style: solid;
                border-right-width: 1px;
                border-top-color: rgb(88, 151, 251);
                border-top-style: solid;
                border-top-width: 1px;
                box-shadow: rgba(0, 0, 0, 0.298039) 0px 0px 5px 0px;
                box-sizing: border-box;
                color: rgb(51, 51, 51);
                cursor: text;
                display: block;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-size: 13px;
                height: 29px;
                line-height: 18.571430206298828px;
                list-style-type: disc;
                margin-bottom: 0px;
                margin-left: 0px;
                margin-right: 0px;
                margin-top: 0px;
                overflow-x: hidden;
                overflow-y: hidden;
                padding-bottom: 0px;
                padding-left: 5px;
                padding-right: 5px;
                padding-top: 0px;
                position: relative;
                width: 787px;
                zoom: 1; -->
                <div class="form-group">
                  <label for="" class="col-sm-2 control-label">Амплуа</label>
                  <div class="col-sm-10">
                    <select data-placeholder="Выберите любимые амплуа"  multiple="" class="form-control chosen-select chosen-select-1" tabindex="-1">
                      <option value=""></option>
                      <optgroup label="Баскетбол">
                        <option value="1_1">Баскетбол: Центровой</option>
                        <option value="1_2">Баскетбол: Форвард</option>
                        <option value="1_3">Баскетбол: Атакующий защитник</option>
                        <option value="1_4">Баскетбол: Разыгрывающий</option>
                      </optgroup>
                      <optgroup label="Футбол">
                        <option value="2_1">Футбол: Нападающий</option>
                        <option value="2_2">Футбол: Форвард</option>
                        <option value="2_3">Футбол: Атакующий защитник</option>
                        <option value="2_4">Футбол: Разыгрывающий</option>
                      </optgroup>
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