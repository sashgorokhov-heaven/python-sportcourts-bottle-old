% rebase("_adminpage", title="Добавить группу")
<div class="row">
  <div class="col-md-6">
    <h2 class="page_header">Рассылка приглашений</h2>
    <br>
    <label for="group_id">Выберите шаблон сообщения</label>
    <select id="sporttype" name="tpl_id" class="form-control input-xs" data-bv-notempty="true"
    data-bv-notempty-message="Укажите вид шаблона">
      % for sport_type in sports:
        <option value="{{sport_type.sport_id()}}">{{sport_type.title()}}</option>
      % end
    </select>
    <button type="button" id="showbutton" class="btn btn-link">Показать шаблон</button>
    <br>
    <br>
    <label for="group_id">Выберите вид спорта</label>
    <select id="sporttype" name="sport_type" class="form-control input-xs" data-bv-notempty="true"
    data-bv-notempty-message="Укажите вид спорта">
      % for sport_type in sports:
        <option value="{{sport_type.sport_id()}}">{{sport_type.title()}}</option>
      % end
    </select>
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