% rebase("_adminpage", title="Админка")
<h1 class="page-header">База площадок</h1>

<div class="row">
  <div class="col-md-12">
    <form>
      <input id="searchTextbox" type="text" class="form-control col-sm-6" placeholder="Search..." style="max-width:60%;">
      <!-- <a href="" class="btn btn-link">Найти</a> -->
    </form>
    <div class="table-responsive">
      <table class="table table-hover" style="font-size:80%">
        <thead>
          <td>ID</td>
          <td>Название</td>
          <td>Телефон</td>
          <td>Стоимость</td>
          <td>Комментарии</td>
        </thead>
        <tbody id="courtssearchtable">
        </tbody>
      </table>
    </div>
  </div>
</div>