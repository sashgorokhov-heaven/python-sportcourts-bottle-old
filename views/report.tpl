% rebase("_basicpage", title="Отчет по игре")
% setdefault("showreport", False)
    <div class="row">
      <div class="col-md-12"  style="margin-top:50px;">
        &nbsp;
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <div class="panel panel-default">
          <div class="panel-body">
            <div class="row">
              <div class="col-md-12">
                <p class="lead">Отчет по игре <a href="/games?game_id={{game['game_id']}}">#{{game['game_id']}}</a> {{'[ОТПРАВЛЕН]' if showreport else ''}}</p>
              </div>
            </div>
            <div class="row">
              <div class="col-md-4">
                <small>
                  <p>Ответственный: <a href="/profile?user_id={{game['responsible_user']['user_id']}}">{{game['responsible_user']['first_name']+' '+game['responsible_user']['last_name']}}</a></p>
                  <p>Вид спорта: {{game['sport_type']['title']}}</p>
                  <p>Тип игры: {{game['game_type']['title']}}</p>
                </small>
              </div>
              <div class="col-md-4">
                <small>
                  <p>Площадка: <a href="/courts?court_id={{game['court']['court_id']}}">{{game['court']['title']}}</a></p>
                  <p>{{game['parsed_datetime'][0]}}, {{game['parsed_datetime'][2]}}, {{game['parsed_datetime'][1]}}</p>
                  <p>Продолжительность: {{game['duration']}} минут</p>
                </small>
              </div>
              <div class="col-md-4"></div>
            </div>
            <form id="reportForm" method="post" class="form-horizontal" action="/report"
              data-bv-message="This value is not valid" enctype="multipart/form-data"
              data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
              data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
              data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
              <input type="hidden" name="game_id" value="{{game['game_id']}}">
              <div class="row">
                <div class="col-md-12">
                  <br>
                  <p>Список участников</p>
                </div>
                <div class="col-md-12">
                  <div class="table-responsive">
                    <table class="table table-hover table-bordered" id="userstable" style="font-size:90%">
                      <tr class="success">
                        <td>№</td>
                        <td>Имя</td>
                        <td>Фамилия</td>
                        <td>Телефон</td>
                        <td colspan="2">Статус</td>
                      </tr>
                      % last_n = 0
                      % for n, user in enumerate(game['subscribed']['users'], 1):
                        <tr class="user">
                          <td>{{n}}</td>
                          <td><a href="/profile?user_id={{user['user_id']}}">{{user['first_name']}}</a></td>
                          <td><a href="/profile?user_id={{user['user_id']}}">{{user['last_name']}}</a></td>
                          <td>{{user['phone']}}</td>
                          <td colspan="2">
                          % if not showreport:
                            <select class="form-control input-sm user_status" name="status={{user['user_id']}}">
                              <option value="0">Не пришел</option>
                              <option value="2">Оплатил</option>
                              <option value="1">Не оплатил</option>
                            </select>
                          % end
                          % if showreport:
                            % status = int(game['report']['registered']['users'][str(user['user_id'])]['status'])
                            % if status==1:
                               Не оплатил
                            % end
                            % if status==2:
                                Оплатил
                            % end
                            % if status==0:
                                Не пришел
                            % end
                          % end
                          </td>
                        </tr>
                        % last_n = n
                      % end
                      % if showreport:
                        % import base64
                        % for n, user_id in enumerate(game['report']['unregistered']['users'], last_n+1):
                          % user = game['report']['unregistered']['users'][user_id]
                          % user['first_name'] = base64.b64decode(user['first_name'].encode()).decode()
                          % user['last_name'] = base64.b64decode(user['last_name'].encode()).decode()
                          <tr class="user">
                            <td>{{n}}</td>
                            <td>{{user['first_name']}}</td>
                            <td>{{user['last_name']}}</td>
                            <td>{{user['phone']}}</td>
                            <td colspan="2">
                                % value = int(user['status'])
                                % if value==1:
                                   Не оплатил
                                % end
                                % if value==2:
                                    Оплатил
                                % end
                                % if value==0:
                                    Не пришел
                                % end
                            </td>
                          </tr>
                        % end
                      % end
                    </table>
                  </div>
                </div>
              </div>
              % if not showreport:
                <div class="row">
                  <div class="col-md-12">
                    <a id="more" class="btn btn-default" role="button">+ добавить незарегистрированного юзера</a>
                  </div>
                  <div class="col-md-12">
                    <p class="text-right amount"></p>
                    <input type="hidden" class="amount_input" name="amount" value="">
                  </div>
                  <div class="col-md-12">
                    <p class="text-right dolg_amount"></p>
                  </div>
                  <div class="col-md-12 text-right">
                      <div class="fileinput fileinput-new" data-provides="fileinput">
                        <span class="btn btn-success btn-file">
                        <span class="fileinput-new">Прикрепить списки</span>
                        <span class="fileinput-exists">Изменить</span>
                        <input type="file" name="photo" accept="images/*"></span>
                        <span class="fileinput-filename"></span>
                        <a href="#" class="close fileinput-exists" data-dismiss="fileinput" style="float: none">&times;</a>
                      </div>
                      <script type="text/javascript">
                          $('.fileinput').fileinput()
                      </script>
                      &nbsp;&nbsp;&nbsp;
                      <input class="btn btn-success" type="submit" value="Отправить отчет">
                  </div>
                </div>
              % end
              % if showreport:
                  <img src="/images/reports/{{game['game_id']}}" class="img-thumbnail" alt="Game report">
              % end
            </form>
          </div>
        </div>
      </div>
    </div>