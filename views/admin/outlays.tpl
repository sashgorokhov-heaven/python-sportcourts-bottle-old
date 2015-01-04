% rebase("_adminpage", title="Добавить затраты")
<div class="row">
  <div class="col-md-6">
    <form action="/admin/outlays/add" method="post"></form>
      <h2 class="page_header">Добавить дополнительные затраты</h2>
      <br>
      <label for="datetime">Дата</label>
      <input type="date" class="form-control" name="datetime"/>
      <br>
      <label for="title">Назавание</label>
      <input type="text" name="title" class="form-control input-xs">
      <br>
      <label for="description">Описание</label>
      <textarea class="form-control" name="description" rows="3"></textarea>
      <br>
      <label for="">Сумма</label>
      <input type="text" name="title" class="form-control input-xs">
      <br><br>
      <button id="sendbutton" type="submit" class="btn btn-success">Добавить трату</button>
    </form>
  </div>
</div>