    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);

      % sorted_dates = sorted(logs.logs_by_date, key=lambda x: int(x.split('-')[2]))

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['День', 'Посещений в день', 'Уникальных посещений в день'],
          % for n, date in enumerate(sorted_dates):
            ['{{date}}', {{len(logs.logs_by_date[date])}}, {{len({logs.logs_dict[id]['ipad']  for id in logs.logs_by_date[date]})}}] {{',' if n<len(sorted_dates) else ''}}
          % end
          ]);

        var options = {
          title: 'График посещений'
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

        chart.draw(data, options);
      }
    </script>