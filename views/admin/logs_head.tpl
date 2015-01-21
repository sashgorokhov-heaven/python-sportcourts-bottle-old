    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);

      % sorted_dates = sorted(logs.logs_by_date, key=lambda x: int(x.split('-')[2]))

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['День', 'Посещений в день', 'Уникальных посещений в день'],
          % for n, date in enumerate(sorted_dates):
            ['{{date}}', {{len(logs.logs_by_date[date])}}, {{len({logs.logs_dict[id]['ip']  for id in logs.logs_by_date[date]})}}] {{',' if n<len(sorted_dates) else ''}}
          % end
          ]);
        var options = {
          title: 'График посещений'
        };
        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);

        % sorted_visits = sorted(prob_den['visits_val'])
        data = google.visualization.arrayToDataTable([
          ['Посещенных игр', 'Кол-во юзеров'],
            [0, {{prob_den['notplayed']}}],
          % for n, val in enumerate(sorted_visits):
            [{{val}}, {{prob_den['density'][val]}}] {{',' if n<len(sorted_visits) else ''}}
          % end
          ]);
        options = {
          title: 'Плотность вероятности'
        };
        var probability_density_chart = new google.visualization.LineChart(document.getElementById('probability_density_div'));
        probability_density_chart.draw(data, options);

        % total = 0
        data = google.visualization.arrayToDataTable([
          ['Дата', 'Регистраций'],
          % for n, date in enumerate(daterange(start_date, end_date)):
            % if str(date) in dates_dict:
                % total += dates_dict[str(date)]
            % end
            ['{{'.'.join(str(date).split('-'))}}', {{total}}] {{',' if n<len(list(daterange(start_date, end_date))) else ''}}
          % end
          ]);
        options = {
          title: '{{'Регистрации с {} по {}'.format(start_date, end_date)}}'
        };
        var reg_chart = new google.visualization.LineChart(document.getElementById('dates_div'));
        reg_chart.draw(data, options);


        % total = 0
        data = google.visualization.arrayToDataTable([
          ['Дата', 'Регистраций'],
          % for n, date in enumerate(daterange(start_date, end_date)):
            % if str(date) in dates_dict:
                % total += dates_dict[str(date)]
            % end
            ['{{'.'.join(str(date).split('-'))}}', {{total}}] {{',' if n<len(list(daterange(start_date, end_date))) else ''}}
          % end
        ]);
        options = {
          title: '{{'Регистрации с {} по {}'.format(start_date, end_date)}}'
        };
        var persent_chart = new google.visualization.LineChart(document.getElementById('persent_growth_div'));
        persent_chart.draw(data, options);

      }
    </script>