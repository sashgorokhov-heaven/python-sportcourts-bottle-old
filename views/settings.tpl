% rebase("_basicpage", title="Настройки")
      <div class="row profile">
        <div class="col-md-12">
          <h1>Настройки профиля</h1>
          <br>
          <form id="settingsForm" method="post" class="form-horizontal" action="/settings"
            data-bv-message="This value is not valid"
            data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
            data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
            data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
            <div class="form-group">
              <label for="sex" class="col-sm-2 control-label">Уведомления</label>
              <div class="col-sm-10">
                <label class="checkbox-inline">
                  <input type="checkbox" name="email_notify" {{'checked' if settings.send_email() else ''}}> Отправлять важные уведомления на email
                </label>
              </div>
            </div>
            <div class="form-group">
              <label for="sex" class="col-sm-2 control-label">Приватность</label>
              <div class="col-sm-10">
                <div class="radio">
                  <label>
                    <input type="radio" name="phone_visible" value="phone_organizers" {{'checked' if settings.show_phone()=='organizers' else ''}}>
                    Мой телефон видят только администраторы
                  </label>
                </div>
                <div class="radio">
                  <label>
                    <input type="radio" name="phone_visible" value="phone_all" {{'checked' if settings.show_phone()=='all' else ''}}>
                    Мой телефон видят все пользователи
                  </label>
                </div>
                <hr>
                <a data-toggle="modal" data-target="#deleteUserModal" class="btn btn-link">Удалить профиль</button>
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


<div class="modal fade" id="deleteUserModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
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