% rebase("_basicpage", title="Восстановление пароля")
      <div class="jumbotron">
        <div class="row">
          <div class="col-md-12 registration" style="text-align:left;">
            <h2 class="text-center">Восстановить пароль</h2><br>
            <form id="recoveryForm" method="post" class="form-horizontal" action="/recovery"
            data-bv-message="This value is not valid" enctype="multipart/form-data"
            data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
            data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
            data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
                <div class="container theme-showcase">
                  <br>
                  <p class="bg-danger" style="padding:20px;">Для восстановления пароля, пожалуйста, введите адрес совей электронной почты.</p>
                </div>
                <div class="form-group">
                  <label for="email" class="col-sm-2 control-label">Email</label>
                  <div class="col-sm-10">
                    <input type="email" class="form-control" name="email" placeholder="example@mail.com" id="email" value="{{email}}"></input>
                    <span id="valid"></span>
                  </div>
                </div>
                <div class="form-group">
                  <div class="col-sm-offset-2 col-sm-8" style="text-align:center;">
                    <button type="submit" class="btn btn-primary" name="submit_recovery">Восстановить пароль</button>
                  </div>
                </div>
            </form>
          </div>
        </div>
      </div> 