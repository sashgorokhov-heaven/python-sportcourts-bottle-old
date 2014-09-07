      <div class="row profile">
        <div class="col-md-12">
          <h1>Настройки профиля</h1>
          <form id="settingsForm" method="post" class="form-horizontal" action="/settings"
            data-bv-message="This value is not valid"  enctype="multipart/form-data"
            data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
            data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
            data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
                <div class="form-group">
                  <label for="sex" class="col-sm-12 control-label">Уведомления</label>
                  <hr>
                  <div class="col-sm-12">
                    <label class="checkbox-inline" style="margin-left:-17px;">
                      <input type="checkbox" name="email_notify" value="1" {{'checked' if user['sex']=='male' else ''}}> Отправлять важные уведомления на email
                    </label>
                  </div>
                  <div class="col-sm-12">
                    <label class="checkbox-inline" style="margin-left:-17px;">
                      <input type="radio" name="email_notify" value="1" {{'checked' if user['sex']=='male' else ''}}> Мой телефон видят только администраторы
                      <input type="radio" name="email_notify" value="1" {{'checked' if user['sex']=='male' else ''}}> ОМой телефон видят все пользователи
                    </label>
                  </div>
                </div>
                <div class="form-group">
                  <div class="col-sm-offset-2 col-sm-8" style="text-align:center;">
                    <button type="submit" class="btn btn-primary" name="submit_profile">Редактировать настройки</button>
                  </div>
                </div>
            </form>
        </div>
      </div>