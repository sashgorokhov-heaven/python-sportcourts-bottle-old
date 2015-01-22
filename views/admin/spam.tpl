% rebase("_adminpage", title="Добавить группу")
<div class="row">
  <div class="col-md-6">
    <h2 class="page_header">Рассылка приглашений</h2>
    <br>
    <label>Аккаунты</label>
    <p id="adminslist"></p>
    <br><br>
    <label for="group_id">Выберите вид спорта</label>
    <select id="sporttype" name="sport_type" class="form-control input-xs" data-bv-notempty="true"
    data-bv-notempty-message="Укажите вид спорта">
      <option value="">---</option>
      <option value="100">Test</option>
      % for sport_type in sports:
        <option value="{{sport_type.sport_id()}}">{{sport_type.title()}}</option>
      % end
    </select>
    <br>
    <p id="userslist"></p>
    <br>
    <!-- <label for="tpl_id">Выберите шаблон сообщения</label>
    <select id="tpl_id" name="tpl_id" class="form-control input-xs" data-bv-notempty="true"
    data-bv-notempty-message="Укажите вид шаблона">
      % for sport_type in sports:
        <option value="{{sport_type.sport_id()}}">{{sport_type.title()}}</option>
      % end
      <option value="100">Test</option>
    </select> -->
    <button type="button" id="showbutton" class="btn btn-default">Показать шаблон</button>
    <br>
    <br>
    <br>
    <button type="button" id="sendbutton" class="btn btn-success">Начать рассылку</button>
  </div>
</div>

<div class="modal fade" id="showModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Демонстрация шаблона</h4>
      </div>
      <div class="modal-body">
        <p id="tpl_show"></p>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="adminModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Авторизация</h4>
      </div>
      <div class="modal-body">
        <p>Подождите, идет авторизация...</p>
        <span id="authinfo"></span>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Закрыть</button>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="sendModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Идет отсылка сообщений</h4>
      </div>
      <div class="modal-body">
        <div class="table-responsive">
          <table id="sendtable" class="table table-hover table-bordered">
          </table>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Закрыть</button>
      </div>
    </div>
  </div>
</div>