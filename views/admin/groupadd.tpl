% rebase("_adminpage", title="Добавить группу")
<div class="row">
  <div class="col-md-6">
    <label for="group_id">Введите ссылку на группу</label>
    <input type="text" id="group_id" class="form-control input-xs">
    <br>
    <label for="group_id">Выберите вид спорта</label>
    <select id="sporttype" name="sport_type" class="form-control input-xs" data-bv-notempty="true"
    data-bv-notempty-message="Укажите вид спорта">
      % for sport_type in sports:
        <option value="{{sport_type.sport_id()}}">{{sport_type.title()}}</option>
      % end
    </select>
    <br>
    <label for="">Опции</label>
    <br>
    <input type="checkbox" id="city" value="1" checked> Не из Екатеринбурга
    <br>
    <input type="checkbox" id="msg" value="1"> С заблокироваными личками
    <br><br>
    <button type="button" id="sendbutton" class="btn btn-success">Отправить запрос</button>
  </div>
</div>

<div class="modal fade" id="resultModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Добавить юзеров:</h4>
      </div>
      <div class="modal-body">
        <div class="table-responsive">
          <p>Название группы: <span id="group_name"></span></p>
          <p>Участников: <span id="group_count"></span></p>
          <p>Подходят по критериям: <span id="group_count1"></span></p>
          <p>Мужчин\женщин: <span id="group_male"></span>\<span id="group_female"></span></p>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" id="addbutton" class="btn btn-success">Добавить в базу</button>
      </div>
    </div>
  </div>
</div>