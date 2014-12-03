<script>
  var users = {{!users}};

  function initusertable (res, item) {
    $('#userssearchtable').html(' ');

    if (item == false) {
      for (var i = 0; i < 30; i++) {
        $('#userssearchtable').append('<tr><td>' + res[i]["user_id"] + '</td><td>' + res[i]["first_name"] + ' ' + res[i]["last_name"] + '</td><td>' + res[i]["phone"] + '</td><td><a href="mailto:' + res[i]["email"] + '">Написать</a></td><td><div class="btn-group"><button type="button" class="btn btn-default btn-xs dropdown-toggle" data-toggle="dropdown">Действие <span class="caret"></span></button><ul class="dropdown-menu" role="menu"><li><a href="#">Забанить</a></li><li><a href="#">Пригласить на игру</a></li><li><a href="#">Записать на игру</a></li></ul></div></td><td><span class="glyphicon glyphicon-remove"></span></td></tr>');
      }
    }
    else
    {
      var l = res.length;
      if (l > 30) {
        l = 30;
      }
      console.log(l);
      for (var i = 0; i < l; i++) {
        $('#userssearchtable').append('<tr><td>' + res[i]["item"]["user_id"] + '</td><td>' + res[i]["item"]["first_name"] + ' ' + res[i]["item"]["last_name"] + '</td><td>' + res[i]["item"]["phone"] + '</td><td><a href="mailto:' + res[i]["item"]["email"] + '">Написать</a></td><td><div class="btn-group"><button type="button" class="btn btn-default btn-xs dropdown-toggle" data-toggle="dropdown">Действие <span class="caret"></span></button><ul class="dropdown-menu" role="menu"><li><a href="#">Забанить</a></li><li><a href="#">Пригласить на игру</a></li><li><a href="#">Записать на игру</a></li></ul></div></td><td><span class="glyphicon glyphicon-remove"></span></td></tr>');
      }
    }
  }

  $( document ).ready(function() {
    initusertable(users,false);
  });

  $(document).on('input','#searchTextbox',function(){
    var options = {
      caseSensitive: false,
      includeScore: true,
      shouldSort: true,
      threshold: 0.3,
      maxPatternLength: 32,
      keys: ["first_name","last_name"]
    };
    var fuse = new Fuse(users, options); // "list" is the item array
    var result = fuse.search("");
    var f = new Fuse(users, options);
    query = $('#searchTextbox').val();
    var result = f.search(query);
    initusertable (result,true);
  });

</script>

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
  }
</script>