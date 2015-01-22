% rebase("_adminpage", title="Добавить группу")
<div class="row">
  <div class="col-md-6">
    <h2 class="page_header">Рассылка писем</h2>
    <br>
    <p>Неактивных юзеров: <span id="nonactive"></span></p>
    <button type="button" id="sendbutton" class="btn btn-default">Активировать неактивных</button>
    <a id="showbutton" class="btn btn-link btn-sm">Смотреть шаблон</a>
    <br><br><br>
    <p>Кастомная рассылка <input type="text" id="custom_tpl"></p>
    <button type="button" id="sendbutton" class="btn btn-default">Разослать письма</button>
    <a id="showbutton" class="btn btn-link btn-sm">Смотреть шаблон</a>
    <br><br><br>
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