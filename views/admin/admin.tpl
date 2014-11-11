% rebase("_adminpage", title="Админка")
<h1 class="page-header">Обзор месяца</h1>

<div class="row">
  <div class="col-xs-12 col-sm-6">
    <h2><a href="/admin/finances">Финансы</a></h2>
    <div class="table-responsive">
      <table class="table table-hover">
        <tr>
          <td>
            <small>
              <strong>
                Идеальный доход:
              </strong>
            </small>
          </td>
          <td>
            <small>{{fin.ideal_income}} ({{len(fin.games)}} игр)</small>
          </td>
        </tr>
        <tr>
          <td>
            <small>
              <strong>
                Реальный доход:
              </strong>
            </small>
          </td>
          <td>
            <small>{{fin.real_income}} ({{fin.percents(fin.real_income, fin.ideal_income)}}%)</small>
          </td>
        </tr>
        <tr>
          <td>
            <small>
              <strong>
                Расходы на аренду:
              </strong>
            </small>
          </td>
          <td>
            <small>{{fin.rent_charges}} ({{fin.percents(fin.rent_charges, fin.real_income)}}%)</small>
          </td>
        </tr>
        <tr class="{{'success' if fin.profit>0 else 'danger'}}">
          <td>
            <small>
              <strong>
                Прибыль
              </strong>
            </small>
          </td>
          <td>
            <small>{{fin.profit}} ({{fin.percents(fin.profit, fin.real_income)}}%)</small>
          </td>
        </tr>
        % for sport_id in fin.sport_games:
            <tr class="{{'success' if fin.sport_money[sport_id]>0 else 'danger'}}">
              <td>
                <small>
                  <strong>
                    {{fin.sports[sport_id].title()}} ({{len(fin.sport_games[sport_id])}} игр)
                  </strong>
                </small>
              </td>
              <td>
                <small>{{fin.sport_money[sport_id]}} ({{round((fin.sport_money[sport_id]/fin.profit)*100)}} %)</small>
              </td>
            </tr>
        % end
      </table>
    </div>
  </div>
  <div class="col-xs-12 col-sm-6">
    <h2><a href="/admin/logs">Посещаемость</a></h2>
    <div class="table-responsive">
      <table class="table table-hover">
        <tr>
          <td>
            <small>
              <strong>
                Уникальных посетителей за месяц
              </strong>
            </small>
          </td>
          <td>
            <small>{{len(log.ips)}}</small>
          </td>
        </tr>
        <tr>
          <td>
            <small>
              <strong>
                Уников в день
              </strong>
            </small>
          </td>
          <td>
            <small>len({log.logs_dict[i]['ip'] for i in log.today})</small>
          </td>
        </tr>
        <tr>
          <td>
            <small>
              <strong>
                Новых пользователей
              </strong>
            </small>
          </td>
          <td>
            <small># TODO</small>
          </td>
        </tr>
        <tr>
          <td>
            <small>
              <strong>
                Записей на игры
              </strong>
            </small>
          </td>
          <td>
            <small># TODO</small>
          </td>
        </tr>
      </table>
    </div>
  </div>
</div>

<div class="row">
  <div class="col-xs-12 col-sm-6">
    <h2>Технические функции</h2>

    <a href="/admin/logs" class="btn btn-link">Просмотр логов</a>
    <br>
    <br>
    <a href="/admin/reload" class="btn btn-link">Перезагрузка сервера</a>
    <br>
    <a href="/admin/clear_cache" class="btn btn-link">Сброс кеша</a>
    <br>
    <a href="/admin/dump" class="btn btn-link">Общий дамп</a>
    <br>
    <a href="" class="btn btn-link">Тестовый режим</a>
    <input type="checkbox">
  </div>
  <div class="col-xs-12 col-sm-6">
    <h2>Пользователи</h2>
    <div class="table-responsive">
      <form>
        <input type="text" class="form-control col-sm-6" placeholder="Search..." style="max-width:60%;">
        <a href="" class="btn btn-link">Найти</a>
      </form>
      <hr>
      <table class="table table-hover" style="font-size:80%">
        <thead>
          <td>ID</td>
          <td>Имя</td>
          <td>Телефон</td>
          <td>Email</td>
          <td>Функции</td>
          <td>Бан</td>
        </thead>
        <tr>
          <td>1</td>
          <td>Виталий Харченко</td>
          <td>+7 (982) 646 94 54</td>
          <td><a href="mailto:harchenko.grape@gmail.com">Написать</a></td>
          <td>
            <div class="btn-group">
              <button type="button" class="btn btn-default btn-xs dropdown-toggle" data-toggle="dropdown">Действие <span class="caret"></span></button>
              <ul class="dropdown-menu" role="menu">
                <li><a href="#">Забанить</a></li>
                <li><a href="#">Пригласить на игру</a></li>
                <li><a href="#">Записать на игру</a></li>
              </ul>
            </div>
          </td>
          <td>
            <span class="glyphicon glyphicon-remove"></span>
          </td>
        </tr>
      </table>
    </div>
    
  </div>
</div>