    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load('visualization', '1', {packages:['corechart']});
      google.setOnLoadCallback(drawChart);
      % sorted_games = sorted(games, key=lambda x: x.game_id())
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'ID игры');
        data.addColumn('number', 'Идеальный доход');
        data.addColumn('number', 'Потери изза пустых мест');
        data.addColumn('number', 'Потери изза непришедших');
        data.addColumn('number', 'Реальный доход');
        data.addColumn('number', 'Аренда');
        data.addColumn('number', 'Прибыль');
        data.addRows([
          % for n, game in enumerate(sorted_games):
            ['{{game.game_id()}}',
            {{games_counted[game.game_id()]['ideal_income']}},
            -{{games_counted[game.game_id()]['lost_empty']}},
            -{{games_counted[game.game_id()]['lost_notvisited']}},
            {{games_counted[game.game_id()]['real_income']}},
            -{{games_counted[game.game_id()]['rent_charges']}},
            {{games_counted[game.game_id()]['profit']}}] {{',' if n<len(sorted_games) else ''}}
          % end
         ]);
        var options = {
          title: 'График финансов'
        };

        var linechart = new google.visualization.LineChart(document.getElementById('linechart_div'));
        linechart.draw(data, options);


        data = new google.visualization.DataTable();
        data.addColumn('string', 'Название площадки');
        data.addColumn('number', 'Прибыль с площадки');
        data.addRows([
          % for n, court_id in enumerate(games_by_courts):
            % profit = sum([games_counted[game.game_id()]['profit'] for game in games_by_courts[court_id]])
            % if profit>0:
                ['{{!courts_dict[court_id].title()}}', {{profit}}] {{',' if n<len(games_by_courts) else ''}}
            % end
          % end
         ]);
        var options = {
          title: 'Прибыль по площадкам'
        };

        var piechart = new google.visualization.PieChart(document.getElementById('piechart_div'));
        piechart.draw(data, options);

        data = new google.visualization.DataTable();
        data.addColumn('string', 'ID игры');
        data.addColumn('number', 'Потери изза пустых мест');
        data.addColumn('number', 'Потери изза непришедших');
        data.addColumn('number', 'Прибыль');
        data.addRows([
          % lost_empty = 0
          % lost_notvisited = 0
          % profit = 0
          % for n, game in enumerate(sorted_games):
            % lost_empty += games_counted[game.game_id()]['lost_empty']
            % lost_notvisited += games_counted[game.game_id()]['lost_notvisited']
            % profit += games_counted[game.game_id()]['profit']
            ['{{game.game_id()}}', {{lost_empty}}, {{lost_notvisited}}, {{profit}}] {{',' if n<len(sorted_games) else ''}}
          % end
         ]);
        var options = {
          title: 'Прибыль'
        };

        var linechart2 = new google.visualization.LineChart(document.getElementById('linechart2_div'));
        linechart2.draw(data, options);
      }
    </script>