% rebase("_basicpage", title='Группы игр')
    <div class="row">
      <div class="col-md-12"  style="margin-top:50px;">
        &nbsp;
      </div>
    </div>
    <div class="row clearfix">
      <div class="col-md-4 column">
        <div class="panel panel-default">
          <div class="panel-body">
            <p class="lead">Наши люди</p>
            <div class="form-group">
              <input type="text" class="form-control" placeholder="Поиск по имени"></input>
            </div>
            <div class="form-group">
              <select id="city" name="city_id" class="form-control">
                <option value="0">Город</option>
                <option value="1">Екатеринбург</option>
              </select>
            </div>
            <div class="form-group">
              <button type="button" class="btn btn-primary btn-block">Найти</button>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-8 column">
        <!-- <div class="page-header">
          <br>
          <h1>
            Пользователи <small>типо маленький текст</small>
          </h1>
        </div> -->
        <div class="tabbable" id="tabs-612446">
          <ul class="nav nav-tabs">
            <li class="active">
              <a href="#panel-all" data-toggle="tab">Все группы</a>
            </li>
            <li>
              <a href="#panel-friends" data-toggle="tab">Мои группы</a>
            </li>
            <!-- <li>
              <a href="#panel-judges" data-toggle="tab">Судьи</a>
            </li>
            <li>
              <a href="#panel-organizators" data-toggle="tab">Организаторы</a>
            </li>
            <li>
              <a href="#panel-responsibles" data-toggle="tab">Ответсвенные</a>
            </li>  -->                  
          </ul>
          <div class="tab-content">
            <div class="tab-pane active" id="panel-all">
              <div class="panel panel-deafult">
                <br>

                <div class="user_card" onclick="window.open('/profile');">
                  <div class="row">
                    <div class="col-md-2">
                      <a href="/profile" target="_blank">
                        <img src="/images/courts/8" class="img-thumbnail profile-avatar" alt="User avatar" width="120">
                      </a>
                    </div>
                    <div class="col-md-6">
                      <a href="/profile" target="_blank">
                        <p class="lead">ФОК Железнодорожный</p>
                      </a>
                      <p>21 год, Екатеринбург</p>
                    </div>
                    <div class="col-md-4 text-right">
                      <a href="/profile" target="_blank">
                        <p class="lead">+ добавить в друзья</p>
                      </a>
                      <p>21 год, Екатеринбург</p>
                    </div>
                  </div>
                </div>
                <hr>

                <div>
                  <div class="row">
                    <div class="col-md-2">
                      <a href="/profile" target="_blank">
                        <img src="/images/courts/1" class="img-thumbnail profile-avatar" alt="User avatar" width="120">
                      </a>
                    </div>
                    <div class="col-md-10">
                      <a href="/profile" target="_blank">
                        <p class="lead">ФОК Факел</p>
                      </a>
                      <p>20 лет, Екатеринбург</p>
                    </div>
                  </div>
                </div>
                <hr>

              </div>
            </div>
            <div class="tab-pane" id="panel-friends">
            </div>
            <!-- <div class="tab-pane" id="panel-judges">
            </div>
            <div class="tab-pane" id="panel-organizators">
            </div>
            <div class="tab-pane" id="panel-responsibles">
            </div> -->
          </div>
        </div>
      </div>
    </div>