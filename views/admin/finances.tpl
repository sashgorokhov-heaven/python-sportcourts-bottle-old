% rebase("_adminpage", title="Админка")
% setdefault("games", list())
<h1 class="page-header">Финансы</h1>

<table class="table table-condensed table-hover">
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
                <p>{{str(game['datetime'].date())}}</p>
              </td>
              <td>
                <a href="/games?game_id={{game['game_id']}}">{{game['description']}} #{{game['game_id']}}</a>
              </td>
              <td>
                <p>{{sports[game['sport_type']].title()}}</p>
              </td>
              <td>
                <a href="/report?game_id={{game['game_id']}}">Отчет</a>
              </td>
              <td>
                <div class="btn-group">
                  % visited = list(filter(lambda x: x['status']==2, reports_dict[game['game_id']]))
                  <a type="button" class="btn btn-link dropdown-toggle" data-toggle="dropdown" style="margin-top:-7px;">{{round((len(visited)/game['capacity'])*100)}}% ({{len(visited)}}/{{game['capacity']}}) <span class="caret"></span></a>
                  <ul class="dropdown-menu" role="menu">
                    <li><a>{{len(list(filter(lambda x: x['user_id']!=0, visited)))}} зарегестрированных</a></li>
                    <li><a>{{len(list(filter(lambda x: x['user_id']==0, visited)))}} новых</a></li>
                  </ul>
                </div>
              </td>
              <td>
                <p>{{game['cost']}} RUB</p>
              </td>
              <td>
                % income = len(visited)*game['cost']
                <p class="text-default">{{income}} RUB</p>
              </td>
              <td>
                % rent_charge = courts_dict[game['court_id']]['cost']*(game['duration']/60)
                <p class="text-warning">{{rent_charge}} RUB</p>
              </td>
              <td>
                % profit = income - rent_charge
                <p class="text-{{'danger' if profit<0 else 'success'}}">{{profit}} RUB</p>
              </td>
              <td>
                <p>{{round(income/len(visited))}} RUB</p>
              </td>
            </tr>
        % end
    % else:
        <tr><td>Игор нет. (может есть, но это тест)</td></tr>
    % end
  </tbody>
</table>