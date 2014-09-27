% rebase("_basicpage", title=user['first_name']+' '+user['last_name'])
      <div class="row profile">
        <div class="col-md-3">
          <img src="/images/avatars/{{str(user['user_id'])}}" class="img-thumbnail profile-avatar" alt="User avatar" width="300">
          <br>
          <br>
          % if user['gameinfo']['total']>0:
          <div class="btn-group">
            <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" style="margin-top:-7px;"><span class="glyphicon glyphicon-stats"></span> Всего сыграно: {{user['gameinfo']['beautiful']['total'][0]}} {{user['gameinfo']['beautiful']['total'][1]}}</button>
              <ul class="dropdown-menu" role="menu">
              % for sport_id in user['gameinfo']['sport_types']:
                <li>
                  <a href="">{{user['gameinfo']['sport_types'][sport_id]}}: {{' '.join(user['gameinfo']['beautiful'][sport_id])}}</a>
                </li>
              % end
              </ul>
          </div>
          % end
          <br>
          <br>
        </div>
        <div class="col-md-9">
          <strong>{{user['first_name']+' '+user['last_name']}}</strong>
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
          % if len({0,1,2}.intersection(user['userlevel']))>0:
            <br>
            % if 0 in user['userlevel']:
                <span class="label label-default">Админ</span>&nbsp;
            % end
            % if 1 in user['userlevel']:
                <span class="label label-primary">Организатор</span>&nbsp;
            % end
            % if 2 in user['userlevel']:
                <span class="label label-info">Ответственный</span>
            % end
            <br>
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
                                <td>Название</td>
                                <td>Вид спорта</td>
                                <td>Площадка</td>
                                <td>Время на площадке</td>
                              </tr>
                              % for game in user_games:
                                <tr>
                                  <td><a href="/games?game_id={{game['game_id']}}" target="_blank">{{game['game_id']}}</a></td>
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
                                <td>Название</td>
                                <td>Вид спорта</td>
                                <td>Площадка</td>
                                <td>Статус отчета</td>
                              </tr>
                              % for game in responsible_games:
                                <tr {{'class=active' if not game['report']['reported'] else ''}}>
                                  <td><a href="/games?game_id={{game['game_id']}}" target="_blank">{{game['game_id']}}</a></td>
                                  <td>{{game['description']}}</td>
                                  <td>{{game['sport_type']['title']}}</td>
                                  <td>{{game['court']['title']}}</td>
                                  <td>{{'Отправлен' if game['report']['reported'] else 'Ожидается'}}</td>
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
                                <td>Название</td>
                                <td>Вид спорта</td>
                                <td>Площадка</td>
                                <td>Статус отчета</td>
                                <td>Передача денег</td>
                              </tr>
                              % for game in organizer_games:
                                <tr {{'class=active' if not game['report']['reported'] else ''}}>
                                  <td><a href="/games?game_id={{game['game_id']}}" target="_blank">{{game['game_id']}}</a></td>
                                  <td>{{game['description']}}</td>
                                  <td>{{game['sport_type']['title']}}</td>
                                  <td>{{game['court']['title']}}</td>
                                  <td>{{'Отправлен' if game['report']['reported'] else 'Ожидается'}}</td>
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