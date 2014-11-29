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

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>