% rebase("_adminpage", title="Админка")
% setdefault("games", list())
<h1 class="page-header">Финансы</h1>

<p>
  <a class="h3" href="/admin/finances/10">Октябрь</a>
  &nbsp;&nbsp;
  <a class="h3" href="/admin/finances/11">Ноябрь</a>
  &nbsp;&nbsp;
  <a class="h3" href="/admin/finances/12">Декабрь</a>
</p>


<div class="panel panel-default col-md-6">
  <div class="panel-body">
    <ul class="nav nav-tabs">
      <li class="active"><a href="#home" data-toggle="tab">Площадки</a></li>
      <li><a href="#profile" data-toggle="tab">Финансы</a></li>
      <li><a href="#messages" data-toggle="tab">Прибыль</a></li>
    </ul>

    <!-- Tab panes -->
    <div class="tab-content">
      <div class="tab-pane active" id="home">
        <div id="piechart_div" style="height: 250px;"></div>
      </div>
      <div class="tab-pane" id="profile">
        <div id="linechart_div" style="height: 250px;"></div>
      </div>
      <div class="tab-pane" id="messages">
        <div id="linechart2_div" style="height: 250px;"></div>
      </div>
    </div>
  </div>
</div>

<table class="table table-condensed table-hover" style="font-size:80%;">
  <thead>
    <th>Дата</th>
    <th>Игра</th>
    <th>Вид спорта</th>
    <th>Отчет</th>
    <th>Посещаемость</th>
    <th>Цена</th>
    <th>Доход</th>
    <th>Расход</th>
    <th>Прибыль</th>
    <th>Прибыль с 1 клиента</th>
  </thead>
  <tbody>
    % if len(games)>0:
        % for game in games:
            <tr>
              <td>
                <p>{{str(game.datetime.date())}}</p>
              </td>
              <td>
                <a target="_blank" href="/games/{{game.game_id()}}">{{game.description()}} #{{game.game_id()}}</a>
              </td>
              <td>
                <p>{{sports[game.sport_type()].title()}}</p>
              </td>
              <td>
                <a target="_blank" href="/games/report/{{game.game_id()}}">Отчет</a>
              </td>
              <td>
                % visited = games_counted[game.game_id()]['playedpayed']
                <p>{{round((visited/game.capacity())*100)}}% ({{visited}}/{{game.capacity()}})</p>
                <!-- <div class="btn-group">
                  % visited = games_counted[game.game_id()]['playedpayed']
                  <a type="button" class="btn btn-link dropdown-toggle" data-toggle="dropdown" style="margin-top:-7px;">{{round((visited/game.capacity())*100)}}% ({{visited}}/{{game.capacity()}}) <span class="caret"></span></a>
                  <ul class="dropdown-menu" role="menu">
                    <li><a> зарегестрированных</a></li>
                    <li><a> новых</a></li>
                  </ul>
                </div> -->
              </td>
              <td>
                <p>{{game.cost()}} RUB</p>
              </td>
              <td>
                <p class="text-default">{{games_counted[game.game_id()]['real_income']}} RUB</p>
              </td>
              <td>
                <p class="text-warning">{{games_counted[game.game_id()]['rent_charges']}} RUB</p>
              </td>
              <td>
                <p class="text-{{'danger' if profit<0 else 'success'}}">{{games_counted[game.game_id()]['profit']}} RUB</p>
              </td>
              <td>
                <p>{{round(games_counted[game.game_id()]['profit']/games_counted[game.game_id()]['playedpayed'])}} RUB</p>
              </td>
            </tr>
        % end
    % else:
        <tr><td>Игор нет. (может есть, но это тест)</td></tr>
    % end
  </tbody>
</table>