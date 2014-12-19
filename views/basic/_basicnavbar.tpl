
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
                    <li><a class="topmenu" href="/courts"><span class="glyphicon glyphicon-globe"></span> Карта</a></li>
                    % if tplname=='2015':
                    <li><a class="topmenu topmenu-promo-act" href="/2015"><span class="glyphicon glyphicon-tree-conifer"></span>Конкурс</a></li>
                    % end
                    % if tplname!='2015':
                    <li><a class="topmenu" href="/2015" style="background-image: linear-gradient(to bottom, rgb(200,15,25) 0, #222 100%) !important; color:#bbb !important; height:52px !important; margin-bottom: -2px !important;"><span class="glyphicon glyphicon-tree-conifer"></span>Конкурс</a></li>
                    % end
                    <!-- <li><a class="topmenu" href="/blog">Блог</a></li> -->
                    % if loggedin:
                        <li>
                          <a class="topmenu" href="/profile">

                            <img src="/images/avatars/{{current_user.user_id()}}?sq_sm" class="img-circle header_avatar" width="30" height="30" >
                            &nbsp;
                            Мой профиль
                          </a>
                        </li>
                        % if current_user.userlevel.admin():
                        <li>
                          <a class="topmenu" href="/admin">
                            Админка
                          </a>
                        </li>
                        % end
                        <li>
                            <a class="topmenu" href="/notifications">
                                <span class="glyphicon glyphicon-bell"></span>
                                % if notifycount>0:
                                    <span class="badge notify">{{notifycount}}
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