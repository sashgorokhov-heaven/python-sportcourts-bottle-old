% rebase("_adminpage", title="Админка")
% import datetime
<h2 class="page-header">Финансы -
    <select id="date_select">
        % for date in dates:
            <option value="{{date[0]}}" {{'selected' if date[0]==current_date else ''}}>{{date[1]}}</option>
        % end
    </select>
</h2>
<div class="container">
	<div class="row clearfix">
        <div class="col-md-4 column">
            <p class="text-default">
                Идеальный доход: <span class="label label-info">{{fin.ideal_income}}</span> ({{len(fin.games)}} игр)<br>
                % if fin.lost_empty>0:
                Потеряно изза пустых мест: <span class="label label-danger">{{fin.lost_empty}}</span> ({{fin.empty}})<br>
                % end
                % if fin.lost_notvisited>0:
                Потеряно изза непришедших: <span class="label label-danger">{{fin.lost_notvisited}}</span> ({{fin.notvisited}})<br>
                % end
                % if fin.lost_notpayed>0:
                Потеряно изза неоплативших: <span class="label label-danger">{{fin.lost_notpayed}}</span> ({{fin.notpayed}})<br>
                % end
                Реальный доход: <span class="label label-{{'danger' if fin.real_income<=0 else 'success'}}">{{fin.real_income}}</span><br>
                Расходы на аренду: <span class="label label-danger">{{round(fin.rent_charges)}}</span><br>
                % if fin.additional_charges>0:
                Допрасходы на играх: <span class="label label-danger">{{fin.additional_charges}}</span><br>
                % end
            </p>
            <p class="lead text-{{'danger' if fin.profit<0 else 'success'}}">
                Прибыль: <span class="label label-{{'danger' if fin.profit<0 else 'success'}}">{{round(fin.profit)}}</span><br>
            </p>
            <p class="text-default">
                Зарплаты ответсвенным: <span class="label label-danger">{{fin.responsible_salary}}</span>
                <button style="margin:10px;"  type="button" class="btn btn-info btn-xs" data-toggle="modal" data-target="#responsible_salary_modal">Просмотреть</button>
            </p>
            <p class="lead text-{{'danger' if fin.real_profit<0 else 'success'}}">
                Итого: <span class="label label-{{'danger' if fin.real_profit<0 else 'success'}}">{{round(fin.real_profit)}}</span><br>
                Итого с арендой: <span class="label label-{{'danger' if fin.real_profit-fin.rent_charges<0 else 'success'}}">{{round(fin.real_profit-fin.rent_charges)}}</span><br>
            </p>
            <p class="text-default">
                <h4 style="margin-top:40px; margin-bottom:0">Зарплаты:</h4><br>
                % for user_id in fin.user_salary:
                    % salary = fin.user_salary[user_id]
                    % user = fin.users_get(user_id)
                    {{user.name}}: <span class="label label-{{'danger' if salary<=0 else 'success'}}">{{round(salary)}}</span><br>
                % end
            </p>
		</div>
        <div class="col-md-8 column">
            <div id="sport_money_chart" style="width:322px;"></div>
            <div id="salary_chart" style="width:322px;"></div>
		</div>
    </div>
    <div class="col-md-12 column">
        <div id="game_finances_chart" style="height:350px;max-width:700px"></div>
        <div id="profit_chart" style="height:350px;max-width:700px"></div>
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
                % games = sorted(fin.games, key=lambda x: x.datetime(), reverse=True)
                % for game in games:
                    <tr>
                      <td>
                        <p>{{'.'.join(str(game.datetime.date()).split('-')[::-1])}}</p>
                      </td>
                      <td>
                        <a target="_blank" href="/games/{{game.game_id()}}">#{{game.game_id()}} | {{fin.real_games_dict[game.game_id()]['description']}}</a>
                      </td>
                      <td>
                        <p>{{fin.sports[game.sport_id()].title()}}</p>
                      </td>
                      <td>
                        <a target="_blank" href="/games/report/{{game.game_id()}}">Отчет</a>
                      </td>
                      <td>
                        % p = fin.percents(game.visited(), game.capacity(), 0)
                        <p class="text-{{'danger' if p<80 else 'success'}}">{{p}}% ({{game.visited()}}/{{game.capacity()}})</p>
                      </td>
                      <td>
                        <p>{{game.cost()}} RUB</p>
                      </td>
                      <td>
                        <p class="text-default">{{game.real_income()}} RUB</p>
                      </td>
                      <td>
                        <p class="text-warning">{{game.rent_charges()+game.additional_charges()}} RUB</p>
                      </td>
                      <td>
                        <p class="text-default">
                            <span class="label label-{{'danger' if game.profit()<100 else 'success'}}">{{round(game.profit())}}</span> RUB
                        </p>
                      </td>
                      <td>
                        <p>{{round(game.profit()/game.playedpayed())}} RUB</p>
                      </td>
                    </tr>
                % end
            </tbody>
        </table>
        <h4 class="page_header">Дополнительные затраты и доходы</h4>
        <table class="table table-condensed table-hover" style="font-size:80%; width:800px;">
          <thead>
            <th>Дата</th>
            <th>Название</th>
            <th>Описание</th>
            <th>Сумма</th>
          </thead>
          <tbody>
            % if len(outlays)>0:
            % for i in outlays:
                <tr class="{{'success' if i.cost()>0 else 'danger'}}">
                  <td>{{i.datetime()}}</td>
                  <td>{{i.title()}}</td>
                  <td>{{i.description()}}</td>
                  <td>{{i.cost()}}</td>
                </tr>
            % end
            % else:
            <tr><td>Затрат нет.</td></tr>
            % end
          </tbody>
        </table>
        <button class="btn btn-primary" data-toggle="modal" data-target="#minusModal">Добавить трату</button>
        <button class="btn btn-primary" data-toggle="modal" data-target="#plusModal">Добавить доход</button>
	</div>
</div>
<div class="modal fade" id="minusModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Добавить затраты</h4>
      </div>
      <div class="modal-body">
        <form action="/admin/outlays/addnegative" method="post" enctype="multipart/form-data">
          <label for="date">Дата</label>
          <input type="date" class="form-control" name="date" value="{{str(datetime.date.today())}}"/>
          <br>
          <label for="time">Время</label>
          <input type="time" class="form-control" name="time" value="{{':'.join(str(datetime.datetime.now().time()).split('.')[0].split(':')[:-1])}}"/>
          <br>
          <label for="title">Назавание</label>
          <input type="text" name="title" class="form-control input-xs">
          <br>
          <label for="description">Описание</label>
          <textarea class="form-control" name="description" rows="3"></textarea>
          <br>
          <label for="">Сумма</label>
          <input type="text" name="cost" class="form-control input-xs">
          <br><br>
          <button type="submit" class="btn btn-success">Добавить трату</button>
        </form>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="plusModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Добавить доход</h4>
      </div>
      <div class="modal-body">
        <form action="/admin/outlays/add" method="post" enctype="multipart/form-data">
          <label for="date">Дата</label>
          <input type="date" class="form-control" name="date" value="{{str(datetime.date.today())}}"/>
          <br>
          <label for="time">Время</label>
          <input type="time" class="form-control" name="time" value="{{':'.join(str(datetime.datetime.now().time()).split('.')[0].split(':')[:-1])}}"/>
          <br>
          <label for="title">Назавание</label>
          <input type="text" name="title" class="form-control input-xs">
          <br>
          <label for="description">Описание</label>
          <textarea class="form-control" name="description" rows="3"></textarea>
          <br>
          <label for="">Сумма</label>
          <input type="text" name="cost" class="form-control input-xs">
          <br><br>
          <button type="submit" class="btn btn-success">Добавить доход</button>
        </form>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="responsible_salary_modal" tabindex="-1" role="dialog" aria-hidden="true">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <h4>Зарплаты ответственным</h4>
      </div>
      <div class="modal-body">
	    <div class="tabbable" id="tabs-548140">
	      <ul class="nav nav-tabs">
            % ordered_ids = sorted(fin.salary.keys(), key=lambda x: len(fin.salary[x]), reverse=True)
            % for n, user_id in enumerate(ordered_ids):
              % user = fin.users_get(user_id)
	      	    <li {{'class=active' if n==0 else ''}}>
	      	    	<a href="#panel-{{user_id}}" data-toggle="tab">{{user.name}} <b>({{len(fin.salary[user_id])}})</b></a>
	      	    </li>
            % end
	      </ul>
	      <div class="tab-content">
            % for n, user_id in enumerate(ordered_ids):
                <div class="tab-pane {{'active' if n==0 else ''}}" id="panel-{{user_id}}">
	      	    	<p>
                        <p>
                            % salary = sum([game_salary['salary'] for game_salary in fin.salary[user_id]])
                            Итого: <span class="label label-{{'danger' if salary<=0 else 'success'}}">{{salary}}</span>
                        </p>
	      	    		<table class="table table-condensed table-hover" id="table-{{user_id}}">
                            <thead>
                              <th>Дата</th>
                              <th>Игра</th>
                              <th>Вид спорта</th>
                              <th>Доход</th>
                              <th>Аренда</th>
                              <th>Допрасход</th>
                              <th>Прибыль</th>
                              <th>Зарплата</th>
                            </thead>
                            <tbody>
                              % for game_salary in fin.salary[user_id]:
                                % game = fin.games_dict[game_salary['game_id']]
                                  <tr class="{{'success' if game_salary['salary']>0 else 'danger'}}">
                                    <td>{{'.'.join(str(game.datetime.date()).split('-')[::-1])}}</td>
                                    <td><a target="_blank" href="/games/{{game.game_id()}}">#{{game.game_id()}} | {{fin.real_games_dict[game.game_id()]['description']}}</a></td>
                                    <td>{{fin.sports[game.sport_id()].title()}}</td>
                                    <td class="{{'success' if game.real_income()>0 else 'danger'}}">{{game.real_income()}}</td>
                                    <td>{{game.rent_charges()}}</td>
                                    <td class="{{'danger' if game.additional_charges()>0 else 'success'}}">{{game.additional_charges()}}</td>
                                    <td class="{{'success' if game.profit()>0 else 'danger'}}">{{round(game.profit())}}</td>
                                    <td class="{{'success' if game.responsible_salary()>0 else 'danger'}}">{{game.responsible_salary()}} ({{game_salary['percents']}}%)</td>
                                  </tr>
                              % end
                            </tbody>
	      	    		</table>
	      	    	</p>
	      	    </div>
            % end
	      </div>
	    </div>
      </div>
    </div>
  </div>
</div>