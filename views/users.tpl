% rebase("_basicpage", title='Пользователи')
% setdefault("myfriends", list())
% setdefault("count", len(allusers))
% setdefault("search", False)
% setdefault("search_q", "")
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
            <form id="searchform" method="POST" class="form-horizontal" action="/users" enctype="multipart/form-data">
              <input type="hidden" name="search" value="all"></input>
              <input id="searchquery" type="text" name="q" class="form-control"
                placeholder="Поиск по имени" {{'value={}'.format(search_q) if search else ''}}></input>
              <br>
              <button id="searchbutton" type="submit" class="btn btn-primary btn-block" value="Найти" {{'' if search else 'disabled'}}>Найти</button>
            </form>
          </div>
        </div>
      </div>
      <div class="col-md-9 column">
        <div class="tabbable" id="tabs-612446">
          <ul class="nav nav-tabs">
            <li class="active">
              <a href="#panel-all" data-toggle="tab">
              % if not search:
                Все пользователи
              % end
              % if search:
                Поиск "{{search_q}}"
              % end
              <span class="badge">{{count}}</span></a>
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
              % if not search:
                % if len(allusers)>0:
                  % for user in allusers:
                    % include("user_row", user=user, myfriends=myfriends)
                    <hr>
                  % end
                  % if len(allusers)==8:
                    <div id="more" onclick="more()"><button type="button" class="btn btn-default btn-sm btn-block">Загрузить еще</button></div>
                  % end
                % end
                % if len(allusers)==0:
                  <div class="alert alert-info fade in">
                    <p class="lead">Пользователей нет.</p>
                  </div>
                % end
              % end
              % if search:
                % if len(allusers)>0:
                  % for user in allusers:
                    % include("user_row", user=user, myfriends=myfriends)
                    <hr>
                  % end
                % end
                % if len(allusers)==0:
                  <div class="alert alert-info fade in">
                    <p class="lead">Никого не найдено.</p>
                  </div>
                % end
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