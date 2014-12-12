% rebase("_basicpage", title="Настройки")
      <div class="row">
        <div class="col-md-12"  style="margin-top:50px;">
          &nbsp;
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <h1>Настройки профиля</h1>
          <br>
          <form id="settingsForm" method="post" class="form-horizontal" action="/profile/settings"
            data-bv-message="This value is not valid"
            data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
            data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
            data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
            <div class="form-group">
              <label for="sex" class="col-sm-2 control-label">Уведомления</label>
              <div class="col-sm-10">
                <label class="checkbox-inline">
                  <input type="checkbox" name="email_notify" {{'checked' if current_user.settings.send_mail() else ''}}> Отправлять важные уведомления на email
                </label>
              </div>
            </div>
            <div class="form-group">
              <label for="sex" class="col-sm-2 control-label">Приватность</label>
              <div class="col-sm-10">
                <div class="radio">
                  <label>
                    <input type="radio" name="phone" value="organizers" {{'checked' if not current_user.settings.show_phone() else ''}}>
                    Мой телефон видят только администраторы
                  </label>
                </div>
                <div class="radio">
                  <label>
                    <input type="radio" name="phone" value="all" {{'checked' if current_user.settings.show_phone() else ''}}>
                    Мой телефон видят все пользователи
                  </label>
                </div>
                <hr>
                <button type="button" data-toggle="modal" data-target="#deleteGameModal" class="btn btn-link">Удалить профиль</button>
                <div class="modal fade" id="deleteGameModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                  <div class="modal-dialog modal-sm">
                    <div class="modal-content">
                      <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                        <h4 class="modal-title" id="myModalLabel">Подтвердите действие</h4>
                      </div>
                      <div class="modal-body">
                        <p>Вы действительно хотите удалить профиль?</p>
                      </div>
                      <div class="modal-footer">
                        <a class="btn btn-danger" href="">Удалить</a>
                        <button type="button" data-dismiss="modal" class="btn btn-primary">Отмена</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <hr>
            <div class="form-group">
              <div class="col-sm-offset-2 col-sm-8">
                <button type="submit" class="btn btn-primary">Редактировать настройки</button>
              </div>
            </div>
            <br>
          </form>
        </div>
      </div>