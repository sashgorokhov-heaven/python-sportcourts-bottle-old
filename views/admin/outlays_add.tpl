% rebase("_adminpage", title="Добавить затраты")
% import datetime
<div class="row">
  <div class="col-md-6">
    <form action="/admin/outlays/add" method="post" enctype="multipart/form-data">
      <h2 class="page_header">Добавить дополнительные затраты</h2>
      <br>
      <label for="date">Дата</label>
      <input type="date" class="form-control" name="date" value="{{str(datetime.date.today())}}"/>
      <br>
      <label for="time">Время</label>
      <input type="time" class="form-control" name="time" value="{{':'.join(str(datetime.datetime.now().time()).split('.')[0].split(':')[:-1])}}"/>
      <br>
      <label for="title">Назавание</label>
      <input type="text" name="title" class="form-control input-xs">
      <br>
      <label for="description">Описание</label>
      <textarea class="form-control" name="description" rows="3"></textarea>
      <br>
      <label for="">Сумма</label>
      <input type="text" name="cost" class="form-control input-xs">
      <br><br>
      <button type="submit" class="btn btn-success">Добавить трату</button>
    </form>
  </div>
</div>