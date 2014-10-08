% rebase("_basicpage", title="Отчет по игре")
% setdefault("showreport", False)
    <div class="row">
      <div class="col-md-12"  style="margin-top:50px;">
        &nbsp;
      </div>
    </div>
    <div class="row list">
      <div class="col-md-12">
        <div class="panel panel-default">
          <div class="panel-body">
            <div class="row">
              <div class="col-md-3">
                <div class="row">
                  <div class="col-md-12 col-sm-6 col-xs-6">
                    <p class="lead">Игра <a href="/games?game_id={{game.game_id()}}">#{{game.game_id()}}</a></p>
                    <small>
                      <p>Ответственный: {{game.responsible_user_id(True).name}}</p>
                      <p>Вид спорта: {{game.sport_type(True).title()}}</p>
                      <p>Тип игры: {{game.game_type(True).title()}}</p>
                      <p>Площадка: {{game.court_id(True).title()}}</p>
                    </div>
                    <div class="col-md-12 col-sm-6 col-xs-6">
                      <p>{{game.datetime.beautiful}}</p>
                      <p>Продолжительность: {{game.duration()}} минут</p>
                      <p>Цена: {{game.cost()}}</p>
                      <br>
                      <br>
                      <p>______________________</p>
                      <p>Подпись ответственного</p>
                    </small>
                  </div>
                </div>
              </div>
              <div class="col-md-9">
                <div class="row">
                  <div class="col-md-12">
                    <p>Список участников</p>
                  </div>
                  <div class="col-md-12">
                    <div class="table-responsive">
                      <table class="table table-hover table-bordered table-condensed" id="userstable" style="font-size:90%">
                        <tr class="success">
                          <td>№</td>
                          <td>Имя</td>
                          <td>Фамилия</td>
                          <td>Телефон</td>
                          <td>Статус</td>
                          <td>Подпись</td>
                        </tr>
                      % for n, user in enumerate(game.subscribed(True), 1):
                        <tr class="user">
                          <td>{{n}}</td>
                          <td>{{user.name.first()}}</td>
                          <td>{{user.name.last()}}</td>
                          <td>{{user.phone()}}</td>
                          <td></td>
                          <td></td>
                        </tr>
                      % end
                      % if len(game.subscribed()) < game.capacity():
                        % for n in range(len(game.subscribed())+1, game.capacity()+1):
                          <tr class="user">
                            <td>{{n}}</td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                          </tr>
                        % end
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