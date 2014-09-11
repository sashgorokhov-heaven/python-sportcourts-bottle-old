% rebase("_basicpage", title='Пользователи')
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
              <a href="#panel-all" data-toggle="tab">Все пользователи</a>
            </li>
            <li>
              <a href="#panel-friends" data-toggle="tab">Мои друзья</a>
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
                <div class="user_card">
                % for user in allusers:
                  <div class="row" onclick="window.open('/profile?user_id={{user['user_id']}}');">
                    <div class="col-md-2">
                      <a href="/profile?user_id={{user['user_id']}}" target="_blank">
                        <img src="/images/avatars/{{user['user_id']}}" class="img-thumbnail profile-avatar" alt="User {{user['user_id']}} avatar" width="120">
                      </a>
                    </div>
                    <div class="col-md-6">
                      <a href="/profile?user_id={{user['user_id']}}" target="_blank">
                        <p class="lead">{{user['first_name']+' '+user['last_name']}}</p>
                      </a>
                      <p>{{user['parsed_bdate']+', '+user['city']['title']}}</p>
                    </div>
                    % if loggedin and user['user_id'] not in {friend['user_id'] for friend in myfriends}:
                        <div class="col-md-4 text-right">
                          <a href="/profile?addfriend={{user['user_id']}}">
                            <p>+ добавить в друзья</p>
                          </a>
                        </div>
                    % end
                  </div>
                  <hr>
                % end
                </div>
              </div>
            </div>
            <div class="tab-pane" id="panel-friends">
                % for user in myfriends:
                  <div class="row" onclick="window.open('/profile?user_id={{user['user_id']}}');">
                    <div class="col-md-2">
                      <a href="/profile?user_id={{user['user_id']}}" target="_blank">
                        <img src="/images/avatars/{{user['user_id']}}" class="img-thumbnail profile-avatar" alt="User {{user['user_id']}} avatar" width="120">
                      </a>
                    </div>
                    <div class="col-md-6">
                      <a href="/profile?user_id={{user['user_id']}}" target="_blank">
                        <p class="lead">{{user['first_name']+' '+user['last_name']}}</p>
                      </a>
                      <p>{{user['parsed_bdate']+', '+user['city']['title']}}</p>
                    </div>
                  </div>

                % end
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