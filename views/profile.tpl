% rebase("_basicpage", title=user['first_name']+' '+user['last_name'])
% setdefault('myfriend', False)
      <div class="row profile">
        <div class="col-md-3">
          <img src="/images/avatars/{{str(user['user_id'])}}" class="img-thumbnail profile-avatar" alt="User avatar" width="300">
          <br>
          % if loggedin and user['user_id']!=userinfo['user_id']:
          <br>
            <a class="friendsbutton btn btn-default btn-block profile-avatar" id="{{'addfriend' if not myfriend else 'removefriend'}}-{{user['user_id']}}">
              {{'добавить в друзья' if not myfriend else 'убрать из друзей'}}
            </a>
          % end
          % if user['gameinfo']['total']>0:
          <br>
          <div class="panel-group" id="accordion1">
            <div class="panel panel-default">
              <div class="panel-heading" style="padding: 6px 15px 6px 15px; background: none; text-align: center;">
                  <a data-toggle="collapse" data-parent="#accordion1" href="#collapseTime">
                    <span class="glyphicon glyphicon-stats"></span> В игре: {{user['gameinfo']['beautiful']['total'][0]}} {{user['gameinfo']['beautiful']['total'][1]}}
                  </a>
              </div>
              <div id="collapseTime" class="panel-collapse collapse">
                <div class="panel-body" style="padding:10px 0 0 10px;">
                  % for sport_id in user['gameinfo']['sport_types']:
                    <p>
                      {{user['gameinfo']['sport_types'][sport_id]}}: {{' '.join(user['gameinfo']['beautiful'][sport_id])}}
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
          <strong>{{user['first_name']+' '+user['last_name']}}</strong>
          &nbsp;
          % if len({0,1,2}.intersection(user['userlevel']))>0:
            % if 0 in user['userlevel']:
                <span id="badge1" class="glyphicon glyphicon-exclamation-sign" data-toggle="tooltip" data-placement="bottom" title="Администратор"></span>
                <script>$('#badge1').tooltip();</script>
                &nbsp;
            % end
            % if 1 in user['userlevel']:
                <span id="badge2" class="glyphicon glyphicon-star" data-toggle="tooltip" data-placement="bottom" title="Организатор"></span>
                <script>$('#badge2').tooltip();</script>
                &nbsp;
            % end
            % if 2 in user['userlevel']:
                <span id="badge3" class="glyphicon glyphicon-star-empty" data-toggle="tooltip" data-placement="bottom" title="Ответственный"></span>
                <script>$('#badge3').tooltip();</script>
                &nbsp;
            % end
          % end
          % if int(user['user_id'])==int(userinfo['user_id']):
            &nbsp;
            &nbsp;
            &nbsp;
            <small>
              <span class="glyphicon glyphicon-pencil"></span>
              <a href="/profile?edit">Ред.</a>
              &nbsp;
              &nbsp;
              &nbsp;
              <span class="glyphicon glyphicon-cog"></span>
              <a href="/settings">Настройки</a>
            </small>
            <br>
          % end
          % if int(user['user_id'])!=int(userinfo['user_id']):
            &nbsp;
            &nbsp;
            <small>Последний раз заходил{{'a' if user['sex']=='female' else ''}}: {{user['lasttime']}}</small><br>
          % end
          <br>
          {{user['parsed_bdate']+', '+user['city']['title']}}<br>
          <br>
          Рост: {{user['height']}} см.<br>
          Вес: {{user['weight']}} кг.<br>
          <br>
          % if int(user['user_id'])==int(userinfo['user_id']) or userinfo['responsible'] or user['settings'].show_phone()=='all' or len(user['userlevel'].intersection({0,1}))>0:
          Телефон: {{user['phone']}}
          % end
          <br>
          <br>
          % if user['vkuserid']:
            <a href="http://vk.com/id{{user['vkuserid']}}" target="_blank">
              <img src="/images/static/vk.png" width="32"/>
            </a>
          % end
          % if int(user['user_id'])==int(userinfo['user_id']) and not activated:
            <p>Вы не активировали свой профиль!</p>
          % end

          <br>
          <br>

          % if int(user['user_id'])==int(userinfo['user_id']):
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
                                  <td><a href="/games?game_id={{game['game_id']}}" target="_blank">{{game['game_id']}}</a></td>
                                  <td>{{game['parsed_datetime'][0]}}</td>
                                  <td>{{game['description']}}</td>
                                  <td>{{game['sport_type']['title']}}</td>
                                  <td>{{game['court']['title']}}</td>
                                  <td>{{game['duration']}} мин.</td>
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
                                <tr {{'class=active' if not game['report']['reported'] else ''}}>
                                  <td><a href="/games?game_id={{game['game_id']}}" target="_blank">{{game['game_id']}}</a></td>
                                  <td>{{game['parsed_datetime'][0]}}</td>
                                  <td>{{game['description']}}</td>
                                  <td>{{game['sport_type']['title']}}</td>
                                  <td>{{game['court']['title']}}</td>
                                  <td>{{!'<a href="/report?game_id={}">Отправлен</a>'.format(game['game_id']) if game['report']['reported'] else 'Ожидается'}}</td>
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
                                <tr {{'class=active' if not game['report']['reported'] else ''}}>
                                  <td><a href="/games?game_id={{game['game_id']}}" target="_blank">{{game['game_id']}}</a></td>
                                  <td>{{game['parsed_datetime'][0]}}</td>
                                  <td>{{game['description']}}</td>
                                  <td>{{game['sport_type']['title']}}</td>
                                  <td>{{game['court']['title']}}</td>
                                  <td>{{!'<a href="/report?game_id={}">Отправлен</a>'.format(game['game_id']) if game['report']['reported'] else 'Ожидается'}}</td>
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