<script src="/view/js/fuse.min.js"></script>

<script>
  var courts = {{!courts}};

  console.log(courts);

  function initcourtstable (res, item) {
    $('#courtssearchtable').html(' ');

    var l = res.length;
    console.log(l);
    if (l > 30) {
      l = 30;
    };

    if (item == false) {
      for (var i = 0; i < l; i++) {
        $('#courtssearchtable').append('<tr><td><a target="_blank" href="/courts/' + res[i]["court_id"] + '">' + res[i]["court_id"] + '</a></td><td><a target="_blank" href="/courts/' + res[i]["court_id"] + '">' + res[i]["title"] + '</a></td><td>' + res[i]["phone"] + '</td><td>' + res[i]["cost"] + '</td><td>' + res[i]["admin_description"] + '</td></tr>');
      }
    }
    else
    {
      console.log(l);
      for (var i = 0; i < l; i++) {
        $('#courtssearchtable').append('<tr><td><a target="_blank" href="/courts/' + res[i]["item"]["court_id"] + '">' + res[i]["item"]["court_id"] + '</a></td><td><a target="_blank" href="/courts/' + res[i]["item"]["court_id"] + '">' + res[i]["item"]["title"] + '</a></td><td>' + res[i]["item"]["phone"] + '</td><td>' + res[i]["item"]["cost"] + '</td><td>' + res[i]["item"]["admin_description"] + '</td></tr>');
      }
    }
  }

  $( document ).ready(function() {
    initcourtstable(courts,false);
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
        keys: ["title"]
      };
      var fuse = new Fuse(courts, options); // "list" is the item array
      var result = fuse.search("");
      var f = new Fuse(courts, options);
      query = $('#searchTextbox').val();
      var result = f.search(query);
      initcourtstable(result,true);
    } else {
      initcourtstable(courts,false);
    };
  });

</script>