      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
          <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                  <span class="sr-only">Toggle navigation</span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="/">SportCourts</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li><a class="topmenu" href="/games">Игры</a></li>
                    <li><a class="topmenu" href="/users">Игроки</a></li>
                    <li><a class="topmenu" href="/about">О нас</a></li>
                    % if loggedin:
                        <li>
                          <a class="topmenu" href="/profile">
                            <!-- <img src="/avatars/{{userinfo['user_id']}}" class="round" width="30">
                            &nbsp; -->
                            Мой профиль
                          </a>
                        </li>
                        <li>
                            <a class="topmenu" href="/notifications">
                                <span class="glyphicon glyphicon-envelope"></span>
                                % if userinfo['notifycount']>0:
                                <span class="badge notify">{{userinfo['notifycount']}}
                                % end
                            </span>
                            </a>
                        </li>
                        <li><a class="topmenu" href="/logout">Выход</a></li>
                        % end
                        % if not loggedin:
                        <li><a class="topmenu" href="#" data-toggle="modal" data-target="#loginModal">Вход</a></li>
                    % end
                </ul>
            </div>
          </div>
      </div>