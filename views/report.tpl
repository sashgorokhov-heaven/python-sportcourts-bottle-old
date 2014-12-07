% rebase("_basicpage", title="Отчет по игре №"+str(game.game_id()))
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
                <p class="lead">Отчет по игре <a href="/games/{{game.game_id()}}">#{{game.game_id()}}</a> {{'[ОТПРАВЛЕН]' if showreport else ''}}</p>
              </div>
            </div>
            <div class="row">
              <div class="col-md-4">
                <small>
                  <p>Ответственный: <a href="/profile/{{game.responsible_user_id()}}">{{game.responsible_user_id(True).name}}</a></p>
                  <p>Вид спорта: {{game.sport_type(True).title()}}</p>
                  <p>Тип игры: {{game.game_type(True).title()}}</p>
                </small>
              </div>
              <div class="col-md-4">
                <small>
                  <p>Площадка: <a href="/courts/{{game.court_id()}}">{{game.court_id(True).title()}}</a></p>
                  <p>{{game.datetime.beautiful}}</p>
                  <p>Продолжительность: {{game.duration()}} минут</p>
                </small>
              </div>
              <div class="col-md-4"></div>
            </div>
            <form id="reportForm" method="post" class="form-horizontal" action="/games/report/{{game.game_id()}}"
              data-bv-message="This value is not valid" enctype="multipart/form-data"
              data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
              data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
              data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
              <input type="hidden" name="game_id" value="{{game.game_id()}}">
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
                        <td>Цена</td>
                      </tr>
                      % last_n = 0
                      % for n, user in enumerate(game.subscribed(True), 1):
                        <tr class="user">
                          <td>{{n}}</td>
                          <td><a href="/profile/{{user.user_id()}}">{{user.name.first()}}</a></td>
                          <td><a href="/profile/{{user.user_id()}}">{{user.name.last()}}</a></td>
                          <td>{{user.phone()}}</td>
                          <td colspan="2">
                          % if not showreport:
                            <select class="form-control input-sm user_status" name="status={{user.user_id()}}">
                              <option value="0">Не пришел</option>
                              <option value="1">Не оплатил</option>
                              <option value="2">Оплатил</option>
                            </select>
                          % end
                          % if showreport:
                            % status = int(game.report()['registered'][user.user_id()])
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
                          <td>
                            {{game.cost()}}
                          </td>
                        </tr>
                        % last_n = n
                      % end
                      % if showreport:
                        % for n, name in enumerate(game.report()['unregistered'], last_n+1):
                          % status, phone = game.report()['unregistered'][name]
                          % first_name, last_name = name.split(' ')[0], name.split(' ')[1]
                          <tr class="user">
                            <td>{{n}}</td>
                            <td>{{first_name}}</td>
                            <td>{{last_name}}</td>
                            <td>{{phone}}</td>
                            <td colspan="2">
                                % if status==1:
                                   Не оплатил
                                % end
                                % if status==2:
                                    Оплатил
                                % end
                                % if status==0:
                                    Не пришел
                                % end
                            </td>
                            <td>
                            {{game.cost()}}
                          </td>
                          </tr>
                        % end
                      % end
                    </table>
                  </div>
                </div>
                % if not showreport:
                <div class="col-md-12">
                  <a id="more" class="btn btn-default" role="button">+ добавить незарегистрированного юзера</a>
                </div>
                % end
              </div>
              <div class="row">
                <div class="col-md-12">
                  <br>
                  <p>Дополнительные затраты</p>
                </div>
                <div class="col-md-6">
                  <div class="table-responsive">
                    <table class="table table-hover table-bordered" id="chargestable" style="font-size:90%">
                      <tr class="success">
                        <td>№</td>
                        <td>Описание</td>
                        <td colspan="2">Сумма</td>
                      </tr>
                      % if showreport:
                        % for n, i in enumerate(game.report()['additional'], 1):
                            <tr>
                                <td>{{n}}</td>
                                <td>{{i[0]}}</td>
                                <td>{{i[1]}}</td>
                            </tr>
                        % end
                      % end
                    </table>
                  </div>
                </div>
                % if not showreport:
                <div class="col-md-12">
                  <a id="morecharge" class="btn btn-default" role="button">+ добавить затраты</a>
                </div>
                % end
              </div>
              % if not showreport:
                <div class="row">
                  <div class="col-md-12">
                    <p class="text-right amount"></p>
                    <input type="hidden" class="amount_input" value="">
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
                  <img src="/images/reports/{{game.game_id()}}" class="img-thumbnail" alt="Game report">
              % end
            </form>
          </div>
        </div>
      </div>
    </div>