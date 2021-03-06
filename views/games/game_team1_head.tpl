<style>
  @font-face {
    font-family: SportRelief; /* Гарнитура шрифта */
    src: url(/fonts/sportrelief.ttf); /* Путь к файлу со шрифтом */
  }
  h6 {
    font-family: SportRelief, 'Comic Sans MS', cursive;
  }

  .hidden{
    display:none;
  }

  .show{
    display:block;
  }

  .panel-title a{
    text-decoration: none;
  }

  .editname{
    color: rgb(66, 139, 202);;
  }

  .editname:hover{
    text-decoration: underline;
  }
</style>

<script>
  function init () 
  {
    $('<div class="col-md-6"><div class="panel-group" id="accordion"><div class="panel panel-default"><div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" data-parent="#accordion" href="#collapseOne">Команда 1</a></h4></div><div id="collapseOne" class="panel-collapse collapse in"><div class="panel-body" style="padding:0px;"><!-- Table --><table class="table table-condensed table-hover" style="margin-bottom:0px;"><tbody><tr><td valign="middle" style="padding-bottom:0px; padding-top:10px;"><p style="padding-left:10px;">1</p></td><td valign="middle" style="padding-bottom:0px; padding-top:10px;"><p><img src="/images/avatars/blank.jpg?sq" class="img-circle header_avatar" width="30" height="30" >  <a class="btn btn-xs btn-success">Занять место</a></td></tr><tr><td valign="middle" style="padding-bottom:0px; padding-top:10px;"><p style="padding-left:10px;">2</p></td><td valign="middle" style="padding-bottom:0px; padding-top:10px;"><p><img src="/images/avatars/blank.jpg?sq" class="img-circle header_avatar" width="30" height="30" >  </td></tr><tr><td valign="middle" style="padding-bottom:0px; padding-top:10px;"><p style="padding-left:10px;">3</p></td><td valign="middle" style="padding-bottom:0px; padding-top:10px;"><p><img src="/images/avatars/blank.jpg?sq" class="img-circle header_avatar" width="30" height="30" >  </td></tr><tr><td valign="middle" style="padding-bottom:0px; padding-top:10px;"><p style="padding-left:10px;">4</p></td><td valign="middle" style="padding-bottom:0px; padding-top:10px;"><p><img src="/images/avatars/blank.jpg?sq" class="img-circle header_avatar" width="30" height="30" >  </td></tr><tr><td valign="middle" style="padding-bottom:0px; padding-top:10px;"><p style="padding-left:10px;">5</p></td><td valign="middle" style="padding-bottom:0px; padding-top:10px;"><p><img src="/images/avatars/blank.jpg?sq" class="img-circle header_avatar" width="30" height="30" >  </td></tr></tbody></table></div></div></div></div></div>').insertBefore(".addteam-panel");
  };

  $(document).on('click','.editname',function(){

    arr = $(this).attr("id").split('-');
    var game_id = arr[1],
      team_id = arr[2];

    $("#nameinput-"+arr[1]+"-"+arr[2]).removeClass("hidden");
    $("#nameinput-"+arr[1]+"-"+arr[2]).addClass("show");

    var poleVvoda = $("#nameinput-"+arr[1]+"-"+arr[2]);
    val = poleVvoda.val();
    poleVvoda.focus().val("").val(val);

    $("#name-"+arr[1]+"-"+arr[2]).addClass("hidden");
    $("#editname-"+arr[1]+"-"+arr[2]).addClass("hidden");

  });

  $(document).on('click','.removeplayer',function(){

    arr = $(this).attr("id").split('-');
    var game_id = arr[1],
      team_id = arr[2],
      player_id = parseFloat(arr[3]);

    $("#player-"+arr[1]+"-"+arr[2]+"-"+arr[3]).remove();

    var Players = $('.player-'+game_id+'-'+team_id).size();

    Teamsize = 5;

    for(var i=(player_id+1); i<(Teamsize+2); i++) {
      val = $(".number-"+game_id+"-"+team_id+"-"+i).html();
      val -= 1;
      $(".number-"+game_id+"-"+team_id+"-"+i).html(val);
    }

  });

  $(document).on('click','.addplayer',function(){

    arr = $(this).attr("id").split('-');
    var game_id = arr[1],
      team_id = arr[2],
      player_id = parseFloat(arr[3]);

    $("#player-"+arr[1]+"-"+arr[2]+"-"+arr[3]).html('<td valign="middle" style="padding-bottom:0px; padding-top:10px;"><p style="padding-left:10px;" class="number-'+game_id+'-'+team_id+'-'+player_id+'">'+player_id+'</p></td><td valign="middle" style="padding-bottom:0px; padding-top:10px;"><p><img src="/images/avatars/blank.jpg?sq" class="img-circle header_avatar" width="30" height="30" >&nbsp;Anonymous</td><td valign="middle" style="padding-bottom:0px; padding-top:10px;"><a href=""><span class="glyphicon glyphicon-remove"></span></a></td>');

  });

  $(document).on('focusout','.nameinput',function(){

    arr = $(this).attr("id").split('-');
    var game_id = arr[1],
      team_id = arr[2];

    val = $("#nameinput-"+arr[1]+"-"+arr[2]).val();
    $("#nameinput-"+arr[1]+"-"+arr[2]).removeClass("show");
    $("#nameinput-"+arr[1]+"-"+arr[2]).addClass("hidden");
    $("#name-"+arr[1]+"-"+arr[2]).html(team_id+". "+val+" &nbsp;<span id='editname-"+game_id+"-"+team_id+"' class='editname glyphicon glyphicon-pencil'></span>");
    $("#name-"+arr[1]+"-"+arr[2]).removeClass("hidden");
    $("#name-"+arr[1]+"-"+arr[2]).addClass("show");

  });
</script>