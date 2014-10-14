% rebase("_basicpage", title='Пользователи')
% setdefault("myfriends", list())
    <div class="row">
      <div class="col-md-12"  style="margin-top:50px;">
        &nbsp;
      </div>
    </div>
    <div class="row clearfix">
      <div class="col-md-3 column">
        <div class="panel panel-default">
          <div class="panel-body">
            <p class="lead">Наши люди</p>
            <div class="form-group">
              <input type="text" class="form-control" placeholder="Поиск по имени"></input>
            </div>
<!--             <div class="form-group">
              <select id="city" name="city_id" class="form-control">
                <option value="0">Город</option>
                <option value="1">Екатеринбург</option>
              </select>
            </div> -->
            <div class="form-group">
              <button type="button" class="btn btn-primary btn-block">Найти</button>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-9 column">
        <div class="tabbable" id="tabs-612446">
          <ul class="nav nav-tabs">
            <li class="active">
              <a href="#panel-all" data-toggle="tab">Все пользователи <span class="badge">{{count}}</span></a>
            </li>
            % if loggedin:
            <li>
              <a href="#panel-friends" data-toggle="tab">
                Мои друзья <span class="badge friendscount">{{len(myfriends)}}</span>
              </a>
            </li>
            % end
          </ul>
          <div class="tab-content">
            <div class="tab-pane active" id="panel-all">
              <br>
              <div class="user_cards_all" id='all'>
              % for user in allusers:
                % include("user_row", user=user, myfriends=myfriends)
                <hr>
              % end
              % if len(allusers)==8:
                <div id="more"><button type="button" class="btn btn-default btn-sm btn-block">Загрузить еще</button></div>
              % end
              </div>
            </div>
            % if loggedin:
            <div class="tab-pane" id="panel-friends">
              <div class="panel panel-deafult">
                <br>
                <div class="user_cards_friends" id='friends'>
                % for user in myfriends:
                  % include("user_row", user=user, myfriend=True)
                  <hr>
                % end
                </div>
              </div>
            </div>
            % end
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