% rebase("_basicpage", title="Регистрация")
% setdefault("sex", "")
% setdefault("first_name", "")
% setdefault("middle_name", "")
% setdefault("last_name", "")
% setdefault("city", "Екатеринбург")
% setdefault("bdate", "")
% setdefault("height", "")
% setdefault("weight", "")
% setdefault("email", "")

      <div class="jumbotron">
        <div class="row">
          <div class="col-md-12 registration" style="text-align:left;">
            <h2 class="text-center">Регистрация</h2><br>
            <div class="row">
              <div class="col-sm-10 col-sm-offset-2">
                <p>
                  <a href="https://oauth.vk.com/authorize?client_id=4436558&scope=email&redirect_uri=http://sportcourts.ru:80/registration&response_type=code&v=5.21">Использовать данные из ВКонтакте
                  <img src="http://zhacker.net/uploads/posts/2014-06/1401795821_vk_com.png" height="38"/>
                  </a>
                </p>
              </div>
            </div>
            <form id="registrationForm" method="post" class="form-horizontal" action="/registration"
            data-bv-message="This value is not valid"
            data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
            data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
            data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
                <div class="form-group">
                  <label for="sex" class="col-sm-2 control-label">Пол</label>
                  <div class="col-sm-10">
                    <label class="checkbox-inline" style="margin-left:-17px;">
                      <input type="radio" name="sex" value="male" data-bv-message="Пожалуйста, выберите ваш пол" data-bv-notempty="true" {{'checked' if sex=='male' else ''}}> Мужской
                    </label>
                    <label class="checkbox-inline">
                      <input type="radio" name="sex" value="female" {{'checked' if sex=='female' else ''}}> Женский
                    </label>
                  </div>
                </div>
                <div class="form-group">
                  <label for="first_name" class="col-sm-2 control-label">Имя</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="first_name" placeholder="" value="{{first_name}}"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Поле имени не может быть пустым" />
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="last_name" class="col-sm-2 control-label">Фамилия</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="last_name" placeholder="" value="{{last_name}}"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Поле фамилии не может быть пустым" />
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="middle_name" class="col-sm-2 control-label">Отчество</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="middle_name" placeholder="" value="{{middle_name}}"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Поле отчества не может быть пустым" />
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="city" class="col-sm-2 control-label">Город</label>
                  <div class="col-sm-10">
                    <p class="form-control-static" style="font-size:1em;">{{city}}</p>
                    <!-- <input type="text" class="form-control" name="city" placeholder="" value=""
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите город" />
                    <span id="valid"></span> -->
                  </div>
                </div>
                <div class="form-group">
                  <label for="bdate" class="col-sm-2 control-label">Дата рождения</label>
                  <div class="col-sm-10">
                    <input type="date" class="form-control" name="bdate" value="{{bdate}}"
                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите дату рождения" />
                  </div>
                </div>
                <div class="form-group">
                  <label for="height" class="col-sm-2 control-label">Рост</label>
                  <div class="col-sm-2">
                    <input type="text" class="form-control" name="height" value="{{height}}"
                    min="150"
                    data-bv-greaterthan-inclusive="true"
                    data-bv-greaterthan-message="Это мало"

                    max="230"
                    data-bv-lessthan-inclusive="false"
                    data-bv-lessthan-message="Ты гигант?)"

                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите рост"

                    pattern="[0-9]"
                    data-bv-regexp-message="Рост указывается числом" />
                  </div>
                </div>
                <div class="form-group">
                  <label for="weight" class="col-sm-2 control-label">Вес</label>
                  <div class="col-sm-2">
                    <input type="text" class="form-control" name="weight" value="{{weight}}"
                    min="30"
                    data-bv-greaterthan-inclusive="true"
                    data-bv-greaterthan-message="Это мало"

                    max="230"
                    data-bv-lessthan-inclusive="false"
                    data-bv-lessthan-message="Ты гигант?)"

                    data-bv-notempty="true"
                    data-bv-notempty-message="Укажите вес"

                    pattern="[0-9]"
                    data-bv-regexp-message="Вес указывается числом" />
                  </div>
                </div>
                <div class="form-group">
                  <label for="email" class="col-sm-2 control-label">Email</label>
                  <div class="col-sm-10">
                    <input type="email" class="form-control" name="email" placeholder="example@mail.com" id="email" value="{{email}}"></input>
                    <span id="valid"></span>
                </div>
                </div>
                <div class="form-group">
                  <label for="passwd" class="col-sm-2 control-label">Пароль</label>
                  <div class="col-sm-10">
                    <input type="password" class="form-control" name="passwd" 
                    data-bv-notempty="true"
                    data-bv-notempty-message="Пароль обязателен и не может быть пустым"
                    data-bv-identical="true"
                    data-bv-identical-field="confirm_passwd"
                    data-bv-identical-message="Пароль и его подтверждение различаются">
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="confirm_passwd" class="col-sm-2 control-label">Подтвердите</label>
                  <div class="col-sm-10">
                    <input type="password" class="form-control" name="confirm_passwd" 
                    data-bv-notempty="true"
                    data-bv-notempty-message="Пароль обязателен и не может быть пустым"
                    data-bv-identical="true"
                    data-bv-identical-field="passwd"
                    data-bv-identical-message="Пароль и его подтверждение различаются">
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <div class="col-sm-offset-2 col-sm-8" style="text-align:center;">
                    <button type="submit" class="btn btn-primary" name="submit_order">Зарегистрироваться</button>
                  </div>
                </div>
            </form>
          </div>
        </div>
      </div> 