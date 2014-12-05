% rebase("_adminpage", title="Админка")
<h1 class="page-header">База клиентов</h1>

<div class="row">
  <div class="col-xs-12 col-sm-6">
    <form>
      <input id="searchTextbox" type="text" class="form-control col-sm-6" placeholder="Search..." style="max-width:60%;">
      <!-- <a href="" class="btn btn-link">Найти</a> -->
    </form>
    <div class="table-responsive">
      <table class="table table-hover" style="font-size:80%">
        <thead>
          <td>ID</td>
          <td>Имя</td>
          <td>Телефон</td>
          <td>Email</td>
          <td>Функции</td>
          <td>Бан</td>
        </thead>
        <tbody id="userssearchtable">
        </tbody>
      </table>
    </div>
  </div>
</div>

<div class="modal fade" id="writeModal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title">Записать игрока на игру</h4>
      </div>
      <div class="modal-body">
        <p>Записать игрока id<span id="userid"></span> на игру:
        <input type="text" id="gameid" class="form-control input-sm" style="width: 100px; display: inline;">
        </p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Закрыть</button>
        <button type="button" id="writeuser" class="btn btn-primary">Записать</button>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="banModal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title">Забанить игрока</h4>
      </div>
      <div class="modal-body">
        <p>Забанить игрока id<span id="banuserid"></span> по причине:
        <input type="text" id="reason" class="form-control input-sm">
        </p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Закрыть</button>
        <button type="button" id="banuser" class="btn btn-primary">Забанить</button>
      </div>
    </div>
  </div>
</div>