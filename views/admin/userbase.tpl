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