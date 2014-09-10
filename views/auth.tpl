% rebase("_basicpage", title="Авторизация")
% setdefault("email", "")
      <div class="jumbotron">
        <div class="row">
          <div class="col-md-12 registration" style="text-align:left;">
            <h2 class="text-center">Авторизация</h2><br>
            %if defined("error"):
              <div class="bs-example">
                <div class="alert alert-danger fade in">
                  <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                  <strong>{{error}}</strong><br>{{error_description}}.
                </div>
              </div>
              <script type="text/javascript">
                  setInterval(function() 
                    {$(".alert").alert('close')}
                    , 5000
                  );
              </script>
              % error = ""
              % error_description = ""
            % end
            <div class="row">
              <form id="loginForm" method="post" class="form-horizontal" action="/auth">
                  <div class="form-group" id="passwd">
                    <label class="col-sm-2 control-label">&nbsp;</label>
                    <div class="col-sm-10">
                      <a href="https://oauth.vk.com/authorize?client_id=4436558&scope=email&redirect_uri=http://{{serverinfo['ip']}}:{{serverinfo['port']}}/auth&response_type=code&v=5.21">
                      <img src="/images/static/vk.png" width="32"/></a>
                    </div>
                  </div>
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
                          <button type="submit" class="btn btn-default">Войти</button> &nbsp; или &nbsp; <a href="/registration">Зарегистрироваться</a>
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