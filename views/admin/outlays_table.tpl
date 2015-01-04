% rebase("_adminpage", title="Добавить затраты")
<div class="row">
  <div class="col-md-6">
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
  </div>
</div>