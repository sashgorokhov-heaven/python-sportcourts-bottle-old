% rebase("_basicpage", title="Регистрация")
% setdefault("vkphoto", "")
% setdefault("sex", "")
% setdefault("first_name", "")
% setdefault("last_name", "")
% setdefault("city", "Екатеринбург")
% setdefault("bdate", "")
% setdefault("phone", "")

<div class="jumbotron">
  <div class="row">
    <div class="col-md-12 registration" style="text-align:left;">
      <h2 class="text-center">Регистрация</h2><br>

    % if not defined("vkuserid"):
        <div class="row">
          <div class="col-sm-10 col-sm-offset-2">
            <p class="lead">
              <a href="https://oauth.vk.com/authorize?client_id=4436558&scope=&redirect_uri=http://{{serverinfo['ip']}}:{{serverinfo['port']}}/registration&response_type=code&v=5.21">
                <img src="/images/static/vk.png" width="32" style="margin-top:-19px;"/>
                Использовать данные из ВКонтакте
              </a>
            </p>
          </div>
        </div>
    % end

    <form id="registrationForm" method="post" class="form-horizontal" action="/registration/reg"
            data-bv-message="This value is not valid" enctype="multipart/form-data"
            data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
            data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
            data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
    % if defined("token"):
        <input type="hidden" name="token" value="{{token}}">
    % end
        <div class="form-group">
          <label for="sex" class="col-sm-2 control-label">Фото</label>
          <div class="col-sm-10">
            <script type="text/javascript">
                $('.fileinput').fileinput()
            </script>
            <div class="fileinput fileinput-{{'exists' if vkphoto else 'new'}}" data-provides="fileinput">
              <div class="fileinput-preview thumbnail" data-trigger="fileinput" style="width: 150px; height: 150px;">
              % if vkphoto:
                <img src="{{vkphoto}}" height="150" width="150"/>
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
          <label for="last_name" class="col-sm-2 control-label">Фамилия</label>
          <div class="col-sm-10">
            <input type="text" class="form-control" name="last_name" placeholder="" value="{{last_name}}"
            data-bv-notempty="true"
            data-bv-notempty-message="Поле фамилии не может быть пустым"
            pattern="^[a-zA-Zа-яА-ЯёЁ]+$"
            data-bv-regexp-message="Имя может содержать только буквы русского или английского алфавита"/>
            <span id="valid"></span>
          </div>
        </div>
        <div class="form-group">
          <label for="first_name" class="col-sm-2 control-label">Имя</label>
          <div class="col-sm-10">
            <input type="text" class="form-control" name="first_name" placeholder="" value="{{first_name}}"
            data-bv-notempty="true"
            data-bv-notempty-message="Поле имени не может быть пустым"
            pattern="^[a-zA-Zа-яА-ЯёЁ]+$"
            data-bv-regexp-message="Имя может содержать только буквы русского или английского алфавита"/>
            <span id="valid"></span>
          </div>
        </div>

        <!--<div class="form-group">
          <label for="city" class="col-sm-2 control-label">Город</label>
          <div class="col-sm-10">
            <input type="text" class="form-control typeahead" name="city" value="{{city if city in {i.title() for i in cities} else 'Екатеринбург'}}" data-provide="typeahead" data-bv-notempty="true" data-bv-notempty-message="Укажите город"/>
            <span id="valid"></span>
          </div>
        </div>
        <script type="text/javascript">
          $('.typeahead').typeahead({
            source: [{{!', '.join(['"{}"'.format(i.title()) for i in cities])}}],
            items: {{len(cities)}},
            minLength: 1
          })
        </script>-->

        <div class="form-group">
          <label for="bdate" class="col-sm-2 control-label">Дата рождения</label>
          <div class="col-sm-10">
            <input id="bdate" class="form-control bdatemask" name="bdate" value="{{bdate}}"
            data-bv-notempty="true"
            data-bv-notempty-message="Укажите дату рождения" />
          </div>
        </div>

        <script type="text/javascript">
          $('.bdatemask').inputmask({
            mask: '99.99.9999'
          });
          $('#bdate').tooltip();
        </script>

        <div class="form-group">
          <label for="phone" class="col-sm-2 control-label">Телефон</label>
          <div class="col-sm-10">
            <input type="text" class="form-control" name="phone" placeholder="" id="phone" value="+7" data-toggle="tooltip" data-placement="bottom" title="Телефон необходим для координаторов игр" data-bv-notempty="true" data-bv-notempty-message="Укажите телефон" data-bv-stringlength="true" data-bv-stringlength-min="17" data-bv-stringlength-message="Введите полный номер"></input>
            <span id="valid"></span>
          </div>
        </div>

        <div class="form-group">
          <label for="email" class="col-sm-2 control-label">Email</label>
          <div class="col-sm-10">
            <input type="email" class="form-control" name="email" placeholder="example@mail.com" id="email" value="{{email}}" disabled></input>
            <span id="valid"></span>
          </div>
        </div>

        <div class="form-group">
          <label for="passwd" class="col-sm-2 control-label">Пароль</label>
          <div class="col-sm-10">
            <input type="password" class="form-control" name="passwd" 
            data-bv-notempty="true"
            data-bv-notempty-message="Пароль обязателен и не может быть пустым"
            data-bv-stringlength="true"
            data-bv-stringlength-min="6"
            data-bv-stringlength-max="30"
            data-bv-stringlength-message="Пароль должен иметь длину от 6 до 30 символов">
            <span id="valid"></span>
          </div>
        </div>
        <div class="form-group">
          <label for="confirm_passwd" class="col-sm-2 control-label">Подтвердите</label>
          <div class="col-sm-10">
            <input type="password" class="form-control"
            data-bv-notempty="true" name="confirm_passwd"
            data-bv-notempty-message="Пароль обязателен и не может быть пустым"
            data-bv-identical="true"
            data-bv-identical-field="passwd"
            data-bv-identical-message="Пароль и его подтверждение различаются">
            <span id="valid"></span>
          </div>
        </div>

        <div class="form-group">
          <div class="col-sm-offset-2 col-sm-8" style="text-align:center;">
            <button type="submit" class="btn btn-primary">Зарегистрироваться</button>
            <small>
              <p class="lead text-muted" style="font-size:100%;">
                Регистрируясь, вы принимаете условия
                <br>
                <a class="btn btn-primary btn-link" data-toggle="modal" data-target="#myModal" style="margin:0; font-size:100%;">пользовательского соглашения</a>
              </p>
            </small>
          </div>
        </div>
       </form>
     </div>
   </div>
 </div> 


 <!-- Modal -->
 <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
   <div class="modal-dialog modal-lg">
     <div class="modal-content">
       <div class="modal-header">
         <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
         <h4 class="modal-title">Пользовательское соглашение</h4>
       </div>
       <div class="modal-body">
         % include("user_agreement")
       </div>
       <div class="modal-footer">
         <button type="button" class="btn btn-default" data-dismiss="modal">Закрыть</button>
       </div>
     </div>
   </div>
 </div>