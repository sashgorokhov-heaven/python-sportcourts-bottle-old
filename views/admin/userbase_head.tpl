<script>
  var users = {{!users}};

  function initusertable (res, item) {
    $('#userssearchtable').html(' ');

    var l = res.length;
    if (l > 30) {
      l = 30;
    }

    if (item == false) {
      for (var i = 0; i < l; i++) {
        $('#userssearchtable').append('<tr><td><a target="_blank" href="/profile/' + res[i]["user_id"] + '">' + res[i]["user_id"] + '</a></td><td>' + res[i]["first_name"] + ' ' + res[i]["last_name"] + '</td><td>' + res[i]["phone"] + '</td><td><a href="mailto:' + res[i]["email"] + '">Написать</a></td><td><div class="btn-group"><button type="button" class="btn btn-default btn-xs dropdown-toggle" data-toggle="dropdown">Действие <span class="caret"></span></button><ul class="dropdown-menu" role="menu"><li><a href="#">Забанить</a></li><li><a href="#">Пригласить на игру</a></li><li><a href="#">Записать на игру</a></li></ul></div></td><td><span class="glyphicon glyphicon-remove"></span></td></tr>');
      }
    }
    else
    {
      console.log(l);
      for (var i = 0; i < l; i++) {
        $('#userssearchtable').append('<tr><td><a target="_blank" href="/profile/' + res[i]["item"]["user_id"] + '">' + res[i]["item"]["user_id"] + '</a></td><td>' + res[i]["item"]["first_name"] + ' ' + res[i]["item"]["last_name"] + '</td><td>' + res[i]["item"]["phone"] + '</td><td><a href="mailto:' + res[i]["item"]["email"] + '">Написать</a></td><td><div class="btn-group"><button type="button" class="btn btn-default btn-xs dropdown-toggle" data-toggle="dropdown">Действие <span class="caret"></span></button><ul class="dropdown-menu" role="menu"><li><a href="#">Забанить</a></li><li><a href="#">Пригласить на игру</a></li><li><a href="#">Записать на игру</a></li></ul></div></td><td><span class="glyphicon glyphicon-remove"></span></td></tr>');
      }
    }
  }

  $( document ).ready(function() {
    initusertable(users,false);
  });

  $(document).on('input','#searchTextbox',function(){
    var len = $("#searchTextbox").val().length;
    if (len > 0) {
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
    } else {
      initusertable(users,false);
    };
  });

</script>