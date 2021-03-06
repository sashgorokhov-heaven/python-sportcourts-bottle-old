% rebase("_basicpage", title=user.name)
% setdefault('myfriend', False)
% setdefault('views', 0)
% setdefault('uviews', 0)
      <div class="row">
        <div class="col-md-12"  style="margin-top:50px;">
          &nbsp;
        </div>
      </div>
      <div class="row">
        <div class="col-md-3">
          <img src="/images/avatars/{{user.user_id()}}" class="profile-avatar img-thumbnail" alt="User avatar" width="300">
          <br>
          % if user.banned():
            <br>
              <a class="btn btn-warning btn-block profile-avatar" >
               Забанен
              </a>
          % end
          % if current_user.userlevel.admin():
            <br>
              <a href="mailto:{{user.email()}}" class="btn btn-primary btn-block profile-avatar" >
                {{user.email()}}
              </a>
          % end
          % if loggedin and user.user_id()!=current_user.user_id():
          <br>
            <a class="friendsbutton btn btn-default btn-block profile-avatar" id="{{'addfriend' if not myfriend else 'removefriend'}}-{{user.user_id()}}">
              {{'добавить в друзья' if not myfriend else 'убрать из друзей'}}
            </a>
          % end
          % if user.gameinfo()['total']>0:
          <br>
          <div class="panel-group" id="accordion1" style="max-width:300px;">
            <div class="panel panel-default">
              <div class="panel-heading" style="padding: 6px 15px 6px 15px; background: none; text-align: center;">
                  <a data-toggle="collapse" data-parent="#accordion1" href="#collapseTime">
                    <span class="glyphicon glyphicon-stats"></span> В игре: {{user.gameinfo()['beautiful']['total']}}
                  </a>
              </div>
              <div id="collapseTime" class="panel-collapse collapse">
                <div class="panel-body" style="padding:10px 0 0 10px;">
                  % for sport_id in user.gameinfo()['sport_types']:
                    <p>
                      {{user.gameinfo()['sport_types'][sport_id]}}: {{user.gameinfo()['beautiful'][sport_id]}}
                    </p>
                  % end
                </div>
              </div>
            </div>
          </div>
          % end
          <br>
          <br>
        </div>
        <div class="col-md-9">
          <strong>{{user.name}}</strong>
          &nbsp;
            % if user.userlevel.admin():
                <span id="badge1" class="glyphicon glyphicon-exclamation-sign" data-toggle="tooltip" data-placement="bottom" title="Администратор"></span>
                <script>$('#badge1').tooltip();</script>
                &nbsp;
            % end
            % if user.userlevel.organizer():
                <span id="badge2" class="glyphicon glyphicon-star" data-toggle="tooltip" data-placement="bottom" title="Организатор"></span>
                <script>$('#badge2').tooltip();</script>
                &nbsp;
            % end
            % if user.userlevel.responsible():
                <span id="badge3" class="glyphicon glyphicon-star-empty" data-toggle="tooltip" data-placement="bottom" title="Ответственный"></span>
                <script>$('#badge3').tooltip();</script>
                &nbsp;
            % end
            % if current_user.userlevel.admin() and views>0:
                <span id="views" class="glyphicon glyphicon-eye-open" data-toggle="tooltip" data-placement="bottom" title="Просмотров: {{'{} всего, {} уникальных ({}%)'.format(views, uviews, round((uviews/views)*100))}}"></span>
                <script>$('#views').tooltip();</script>
            % end
          % if user.user_id()==current_user.user_id():
            &nbsp;
            &nbsp;
            &nbsp;
            <small>
              <span class="glyphicon glyphicon-pencil"></span>
              <a href="/profile/edit">Ред.</a>
              &nbsp;
              &nbsp;
              &nbsp;
              <span class="glyphicon glyphicon-cog"></span>
              <a href="/profile/settings">Настройки</a>
            </small>
            <br>
          % end
          % if user.user_id()!=current_user.user_id():
            &nbsp;
            &nbsp;
            <small>Последний раз заходил{{'a' if user.sex()=='female' else ''}}: {{user.lasttime}}</small><br>
          % end
          <br>
          {{str(user.bdate)+', '+user.city_id(True).title()}}<br>
            <br>
          % if user.height() > 0:
            Рост: {{user.height()}} см.<br>
          % elif user.user_id()==current_user.user_id():
            Рост: <small><a href="/profile/edit">Заполнить...</a></small><br>
          % elif user.user_id()!=current_user.user_id():
            Рост: не указан
            <br>
          % end
          % if user.weight() > 0:
            Вес: {{user.weight()}} кг.<br>
          % elif user.user_id()==current_user.user_id():
            Вес: <small><a href="/profile/edit">Заполнить...</a></small><br>
          % elif user.user_id()!=current_user.user_id():
            Вес: не указан<br>
          % end
          <br>
          % if loggedin and (user.user_id()==current_user.user_id() or current_user.userlevel.resporgadmin() or user.settings.show_phone()):
          Телефон: {{user.phone()}}
          % end
          <br>
          % if len(user.ampluas())>0:
            <br>
            {{!'<br>'.join(['{}: {}'.format(amplua.sport_type(True).title(), amplua.title()) for amplua in user.ampluas(True)])}}
            <br>
          % end
          <br>
          % if loggedin:
            % if user.vkuserid():
              <a href="http://vk.com/id{{user.vkuserid()}}" target="_blank" style="text-decoration:none;">
                <img src="/images/static/vk.png" width="32"/>
              </a>
            % end
          % end

          % if user.user_id()==current_user.user_id():
            % if not user.vkuserid():
              <a href="https://oauth.vk.com/authorize?client_id=4436558&scope=&redirect_uri=http://{{serverinfo['ip']}}:{{serverinfo['port']}}/setvkid&response_type=code&v=5.21" target="_blank">
                + связать свой аккаунт с вконтакте
              </a>
            % end
          % end
          <br>
          <br>

          % if user.user_id()==current_user.user_id() and not current_user.userlevel.admin():
            <div class="panel-group" id="accordion">
              % if len(user_games)>0:
                <div class="panel panel-default">
                  <div class="panel-heading">
                    <h4 class="panel-title">
                      <a data-toggle="collapse" data-parent="#accordion" href="#collapseOne">
                        Мои игры
                      </a>
                    </h4>
                  </div>
                  <div id="collapseOne" class="panel-collapse collapse">
                    <div class="panel-body">
                      <div class="row">
                        <div class="col-md-12">
                          <div class="table-responsive">
                            <table class="table table-hover table-bordered" style="font-size:90%; margin-bottom:0px;">
                              <tr class="active">
                                <td>№ игры</td>
                                <td>Дата</td>
                                <td>Название</td>
                                <td>Вид спорта</td>
                                <td>Площадка</td>
                                <td>Время на площадке</td>
                              </tr>
                              % for game in user_games:
                                <tr>
                                  <td><a href="/games/{{game.game_id()}}" target="_blank">{{game.game_id()}}</a></td>
                                  <td>{{game.datetime.beautiful.day_month()}}</td>
                                  <td>{{game.description()}}</td>
                                  <td>{{game.sport_type(True).title()}}</td>
                                  <td>{{game.court_id(True).title()}}</td>
                                  <td>{{game.duration()}} мин.</td>
                                </tr>
                              % end
                            </table>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              % end
              % if len(responsible_games)>0:
                <div class="panel panel-warning">
                  <div class="panel-heading">
                    <h4 class="panel-title">
                      <a data-toggle="collapse" data-parent="#accordion" href="#collapseTwo">
                        Игры, на которых я был ответственным.
                      </a>
                    </h4>
                  </div>
                  <div id="collapseTwo" class="panel-collapse collapse">
                    <div class="panel-body">
                      <div class="row">
                        <div class="col-md-12">
                          <div class="table-responsive">
                            <table class="table table-hover table-bordered" style="font-size:90%; margin-bottom:0px;">
                              <tr class="warning">
                                <td>№ игры</td>
                                <td>Дата</td>
                                <td>Название</td>
                                <td>Вид спорта</td>
                                <td>Площадка</td>
                                <td>Статус отчета</td>
                              </tr>
                              % for game in responsible_games:
                                % if game.deleted():
                                    % continue
                                % end
                                <tr {{'class=active' if not game.reported() else ''}}>
                                  <td><a href="/games/{{game.game_id()}}" target="_blank">{{game.game_id()}}</a></td>
                                  <td>{{game.datetime.beautiful.day_month()}}</td>
                                  <td>{{game.description()}}</td>
                                  <td>{{game.sport_type(True).title()}}</td>
                                  <td>{{game.court_id(True).title()}}</td>
                                  <td>
                                   % if game.reported():
                                        <a href="/games/report/{{game.game_id()}}">Отправлен</a>
                                   % end
                                   % if not game.reported():
                                        % if game.datetime.passed:
                                            <a href="/games/report/{{game.game_id()}}">Ожидается</a>
                                        % end
                                        % if not game.datetime.passed:
                                            <a href="/games/list/{{game.game_id()}}">Распечатать списки</a>
                                        % end
                                   % end
                                  </td>
                                </tr>
                              % end
                            </table>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              % end
              % if len(organizer_games)>0:
                <div class="panel panel-danger">
                  <div class="panel-heading">
                    <h4 class="panel-title">
                      <a data-toggle="collapse" data-parent="#accordion" href="#collapseThree">
                        Игры моего направления
                      </a>
                    </h4>
                  </div>
                  <div id="collapseThree" class="panel-collapse collapse">
                    <div class="panel-body">
                      <div class="row">
                        <div class="col-md-12">
                          <div class="table-responsive">
                            <table class="table table-hover table-bordered" style="font-size:90%; margin-bottom:0px;">
                              <tr class="danger">
                                <td>№ игры</td>
                                <td>Дата</td>
                                <td>Название</td>
                                <td>Вид спорта</td>
                                <td>Площадка</td>
                                <td>Статус отчета</td>
                                <td>Передача денег</td>
                              </tr>
                              % for game in organizer_games:
                                % if game.deleted():
                                    % continue
                                % end
                                <tr {{'class=active' if not game.reported() else ''}}>
                                  <td><a href="/games/{{game.game_id()}}" target="_blank">{{game.game_id()}}</a></td>
                                  <td>{{game.datetime.beautiful.day_month()}}</td>
                                  <td>{{game.description()}}</td>
                                  <td>{{game.sport_type(True).title()}}</td>
                                  <td>{{game.court_id(True).title()}}</td>
                                  <td>{{!'<a href="/report?game_id={}">Отправлен</a>'.format(game.game_id()) if game.reported() else 'Ожидается'}}</td>
                                  <td> --- </td>
                                </tr>
                              % end
                            </table>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              % end
            </div>
          % end

          % if current_user.userlevel.admin():
            <div class="panel-group" id="accordion">
              % if len(user_games)>0:
                <div class="panel panel-default">
                  <div class="panel-heading">
                    <h4 class="panel-title">
                      <a data-toggle="collapse" data-parent="#accordion" href="#collapseOne">
                        Игры пользователя
                      </a>
                    </h4>
                  </div>
                  <div id="collapseOne" class="panel-collapse collapse">
                    <div class="panel-body">
                      <div class="row">
                        <div class="col-md-12">
                          <div class="table-responsive">
                            <table class="table table-hover table-bordered" style="font-size:90%; margin-bottom:0px;">
                              <tr class="active">
                                <td>№ игры</td>
                                <td>Дата</td>
                                <td>Название</td>
                                <td>Вид спорта</td>
                                <td>Площадка</td>
                                <td>Время на площадке</td>
                              </tr>
                              % for game in user_games:
                                <tr>
                                  <td><a href="/games/{{game.game_id()}}" target="_blank">{{game.game_id()}}</a></td>
                                  <td>{{game.datetime.beautiful.day_month()}}</td>
                                  <td>{{game.description()}}</td>
                                  <td>{{game.sport_type(True).title()}}</td>
                                  <td>{{game.court_id(True).title()}}</td>
                                  <td>{{game.duration()}} мин.</td>
                                </tr>
                              % end
                            </table>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              % end
              % if len(responsible_games)>0:
                <div class="panel panel-warning">
                  <div class="panel-heading">
                    <h4 class="panel-title">
                      <a data-toggle="collapse" data-parent="#accordion" href="#collapseTwo">
                        Игры, на которых пользователь был ответственным
                      </a>
                    </h4>
                  </div>
                  <div id="collapseTwo" class="panel-collapse collapse">
                    <div class="panel-body">
                      <div class="row">
                        <div class="col-md-12">
                          <div class="table-responsive">
                            <table class="table table-hover table-bordered" style="font-size:90%; margin-bottom:0px;">
                              <tr class="warning">
                                <td>№ игры</td>
                                <td>Дата</td>
                                <td>Название</td>
                                <td>Вид спорта</td>
                                <td>Площадка</td>
                                <td>Статус отчета</td>
                              </tr>
                              % for game in responsible_games:
                                <tr {{'class=active' if not game.reported() else ''}}>
                                  <td><a href="/games/{{game.game_id()}}" target="_blank">{{game.game_id()}}</a></td>
                                  <td>{{game.datetime.beautiful.day_month()}}</td>
                                  <td>{{game.description()}}</td>
                                  <td>{{game.sport_type(True).title()}}</td>
                                  <td>{{game.court_id(True).title()}}</td>
                                  <td>
                                   % if game.reported():
                                        <a href="/games/report/{{game.game_id()}}">Отправлен</a>
                                   % end
                                   % if not game.reported():
                                        % if game.datetime.passed:
                                            <a href="/games/report/{{game.game_id()}}">Ожидается</a>
                                        % end
                                        % if not game.datetime.passed:
                                            <a href="/games/list/{{game.game_id()}}">Распечатать списки</a>
                                        % end
                                   % end
                                  </td>
                                </tr>
                              % end
                            </table>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              % end
              % if len(organizer_games)>0 and user.user_id()==current_user.user_id():
                <div class="panel panel-danger">
                  <div class="panel-heading">
                    <h4 class="panel-title">
                      <a data-toggle="collapse" data-parent="#accordion" href="#collapseThree">
                        Созданные пользователем игры
                      </a>
                    </h4>
                  </div>
                  <div id="collapseThree" class="panel-collapse collapse">
                    <div class="panel-body">
                      <div class="row">
                        <div class="col-md-12">
                          <div class="table-responsive">
                            <table class="table table-hover table-bordered" style="font-size:90%; margin-bottom:0px;">
                              <tr class="danger">
                                <td>№ игры</td>
                                <td>Дата</td>
                                <td>Название</td>
                                <td>Вид спорта</td>
                                <td>Площадка</td>
                                <td>Статус отчета</td>
                                <td>Передача денег</td>
                              </tr>
                              % for game in organizer_games:
                                <tr {{'class=active' if not game.reported() else ''}}>
                                  <td><a href="/games/{{game.game_id()}}" target="_blank">{{game.game_id()}}</a></td>
                                  <td>{{game.datetime.beautiful.day_month()}}</td>
                                  <td>{{game.description()}}</td>
                                  <td>{{game.sport_type(True).title()}}</td>
                                  <td>{{game.court_id(True).title()}}</td>
                                  <td>{{!'<a href="/report?game_id={}">Отправлен</a>'.format(game.game_id()) if game.reported() else 'Ожидается'}}</td>
                                  <td> --- </td>
                                </tr>
                              % end
                            </table>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              % end
            </div>
          % end
        </div>
      </div>