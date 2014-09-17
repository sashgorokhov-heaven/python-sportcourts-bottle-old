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
              <div class="col-md_6">
                <p class="lead">Списки для игры <a href="/games?game_id={{game['game_id']}}">#{{game['game_id']}}</a></p>
                <small>
                  <p>Ответственный: <a href="/profile?user_id={{game['responsible_user_id']}}">{{game['responsible_user_name']}}</a></p>
                  <p>Вид спорта: {{game['sport_type']['title']}}</p>
                  <p>Тип игры: {{game['game_type']['title']}}</p>
                  <p>Площадка: <a href="/courts?court_id={{game['court']['court_id']}}">{{game['court']['title']}}</a></p>
                  <p>{{game['parsed_datetime'][0]}}, {{game['parsed_datetime'][2]}}, {{game['parsed_datetime'][1]}}</p>
                  <p>Продолжительность: {{game['duration']}} минут</p>
                </small>
              </div>
              <div class="col-md_6">
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
                          <td>Статус</td>
                          <td>Подпись</td>
                        </tr>
                        % last_n = 0
                        % for n, user in enumerate(game['subscribed']['users'], 1):
                          <tr class="user">
                            <td>{{n}}</td>
                            <td><a href="/profile?user_id={{user['user_id']}}">{{user['first_name']}}</a></td>
                            <td><a href="/profile?user_id={{user['user_id']}}">{{user['last_name']}}</a></td>
                            <td>{{user['phone']}}</td>
                            <td></td>
                            <td></td>
                          </tr>
                        % end
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>