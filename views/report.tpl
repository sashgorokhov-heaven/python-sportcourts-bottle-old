% rebase("_basicpage", title="Отчет по игре")
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
                <p class="lead">Отчет по игре <a href="/games?game_id={{game['game_id']}}">#{{game['game_id']}}</a></p>
              </div>
            </div>
            <div class="row">
              <div class="col-md-4">
                <small>
                  <p>Ответственный: <a href="/profile?user_id={{game['responsible_user_id']}}">{{game['responsible_user_name']}}</a></p>
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
                      % for n, user in enumerate(game['subscribed']['users'], 1):
                        <tr class="user">
                          <td>{{n}}</td>
                          <td><a href="/profile?user_id={{user['user_id']}}">{{user['first_name']}}</a></td>
                          <td><a href="/profile?user_id={{user['user_id']}}">{{user['last_name']}}</a></td>
                          <td>{{user['phone']}}</td>
                          <td colspan="2">
                            <select class="form-control input-sm user_status" name="status={{user['user_id']}}">
                              <option value="0"></option>
                              <option value="1">Оплатил</option>
                              <option value="2">Не оплатил</option>
                              <option value="3">Не пришел</option>
                            </select>
                          </td>
                        </tr>
                      % end
                    </table>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6">
                  <a id="more" class="btn btn-default" role="button">+ добавить незарегистрированного юзера</a>
                </div>
                <div class="col-md-6 text-right">
                  <input class="btn btn-success" type="submit">Отправить отчет</a>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>