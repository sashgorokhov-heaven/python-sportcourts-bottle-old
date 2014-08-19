% rebase("_basicpage", title="Авторизация")
% setdefault("email", "")
      <div class="jumbotron">
        <div class="row">
          <div class="col-md-12 registration" style="text-align:left;">
            <h2 class="text-center">Авторизация</h2><br>
            %if defined("error"):
                <p>{{error}}</p>
                <p>{{error_description}}</p>
                % error = ""
                % error_description = ""
            % end
            <div class="row">
              <form id="loginForm" method="post" class="form-horizontal" action="/auth">
                  <div class="form-group" id="passwd">
                      <label class="col-sm-2 control-label">Email</label>
                      <div class="col-sm-10">
                          <input type="email" class="form-control" name="email" data-bv-emailaddress="true"
                          data-bv-notempty="true"
                          data-bv-notempty-message="Введите email" value="{{email}}"/>
                      </div>
                  </div>
                  <div class="form-group" id="passwd1">
                      <label class="col-sm-2 control-label">Password</label>
                      <div class="col-sm-10">
                          <input type="password" class="form-control" name="password" 
                          data-bv-notempty="true"
                          data-bv-notempty-message="Пароль обязателен и не может быть пустым"/>
                      </div>
                  </div>
                  <div class="form-group">
                      <div class="col-sm-10 col-sm-offset-2">
                          <button type="submit" class="btn btn-default" name="submit_reg">Войти</button> &nbsp; или &nbsp; <a href="/registration">Зарегистрироваться</a>
                          <br>
                          <br>
                          <a href="">Восстановить пароль</a>
                      </div>
                  </div>
              </form>
            </div>
          </div>
        </div>
      </div> 