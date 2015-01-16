<script>
$(document).on('change','#date_select',function(){
    var date = $('#date_select').val();
    location.href='/admin/finances/'+date;
});
</script>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load('visualization', '1', {packages:['corechart']});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Вид спорта');
        data.addColumn('number', 'Прибыль');
        data.addRows([
          % for n, sport_id in enumerate(fin.sport_money):
               ['{{fin.sports[sport_id].title()}}', {{fin.sport_money[sport_id] if fin.sport_money[sport_id]>0 else 0}}] {{',' if n<len(fin.sport_money) else ''}}
          % end
         ]);
        var options = {
          title: 'Прибыль по видам спорта'
        };

        var piechart = new google.visualization.PieChart(document.getElementById('sport_money_chart'));
        piechart.draw(data, options);


        data = new google.visualization.DataTable();
        data.addColumn('string', 'Человек');
        data.addColumn('number', 'Зарплата');
        data.addRows([
          % for n, user_id in enumerate(fin.user_salary):
               % user, salary = fin.user_salary[user_id]
               ['{{user.name}}', {{salary}}] {{',' if n<len(fin.user_salary) else ''}}
          % end
         ]);
        var options = {
          title: 'Зарплаты'
        };

        piechart = new google.visualization.PieChart(document.getElementById('salary_chart'));
        piechart.draw(data, options);


        data = new google.visualization.DataTable();
        data.addColumn('string', 'ID игры');
        data.addColumn('number', 'Идеальный доход');
        data.addColumn('number', 'Потери изза пустых мест');
        data.addColumn('number', 'Потери изза непришедших');
        data.addColumn('number', 'Реальный доход');
        data.addColumn('number', 'Аренда');
        data.addColumn('number', 'Доптраты');
        data.addColumn('number', 'Прибыль');
        % games = sorted(fin.games, key=lambda x: x.datetime(), reverse=True)
        data.addRows([
          % for n, game in enumerate(games):
            ['{{game.game_id()}}',
            {{game.ideal_income()}},
            -{{game.lost_empty()}},
            -{{game.lost_notvisited()}},
            {{game.real_income()}},
            -{{game.rent_charges()}},
            -{{game.additional_charges()}},
            {{game.profit()}}] {{',' if n<len(games) else ''}}
          % end
         ]);
        var options = {
          title: 'Линейный график финансов по играм'
        };

        var linechart = new google.visualization.LineChart(document.getElementById('game_finances_chart'));
        linechart.draw(data, options);

        data = new google.visualization.DataTable();
        data.addColumn('string', 'ID игры');
        data.addColumn('number', 'Потери изза пустых мест');
        data.addColumn('number', 'Потери изза непришедших');
        data.addColumn('number', 'Допрасходы');
        data.addColumn('number', 'Прибыль');
        data.addRows([
          % lost_empty = 0
          % lost_notvisited = 0
          % additional_charges = 0
          % profit = 0
          % for n, game in enumerate(games):
            % lost_empty += game.lost_empty()
            % lost_notvisited += game.lost_notvisited()
            % additional_charges += game.additional_charges()
            % profit += game.profit()
            ['{{game.game_id()}}',
             {{lost_empty}},
             {{lost_notvisited}},
             {{additional_charges}},
             {{profit}}] {{',' if n<len(games) else ''}}
          % end
         ]);
        var options = {
          title: 'Линейный график общей прибыли и расходов'
        };

        linechart = new google.visualization.LineChart(document.getElementById('profit_chart'));
        linechart.draw(data, options);

      }
    </script>