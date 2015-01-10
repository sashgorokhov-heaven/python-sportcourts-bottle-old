% rebase("_adminpage", title="Добавить затраты")
% import datetime
<div class="row">
    <h2 class="page_header">Дополнительные затраты</h2>
    <table class="table table-condensed table-hover" style="font-size:80%;">
      <thead>
        <th>Дата</th>
        <th>Название</th>
        <th>Описание</th>
        <th>Сумма</th>
      </thead>
      <tbody>
        % if len(outlays)>0:
        % for i in outlays:
            <tr>
              <td>{{i.datetime()}}</td>
              <td>{{i.title()}}</td>
              <td>{{i.description()}}</td>
              <td>{{i.cost()}}</td>
            </tr>
        % end
        % else:
        <tr><td>Затрат нет.</td></tr>
        % end
      </tbody>
    </table>
    <button class="btn btn-primary" data-toggle="modal" data-target="#minusModal">Добавить трату</button>
    <button class="btn btn-primary" data-toggle="modal" data-target="#plusModal">Добавить доход</button>
</div>

<div class="modal fade" id="minusModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Добавить затраты</h4>
      </div>
      <div class="modal-body">
        <form action="/admin/outlays/addnegative" method="post" enctype="multipart/form-data">
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
  </div>
</div>

<div class="modal fade" id="plusModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Добавить доход</h4>
      </div>
      <div class="modal-body">
        <form action="/admin/outlays/add" method="post" enctype="multipart/form-data">
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
          <button type="submit" class="btn btn-success">Добавить доход</button>
        </form>
      </div>
    </div>
  </div>
</div>