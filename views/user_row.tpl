% setdefault("myfriends", list())
% myfriend = user.user_id() in {friend.user_id() for friend in myfriends}

<div class="row">
  <div class="col-md-2 col-sm-3 col-xs-3">
    <a href="/profile/{{user.user_id()}}" target="_blank">
      <img src="/images/avatars/{{user.user_id()}}" class="img-thumbnail profile-avatar" alt="User {{user.user_id()}} avatar" width="120" >
    </a>
    % if user.gameinfo()['total']>0:
    <p  class="text-center">
      <small>
      <!-- <span class="glyphicon glyphicon-stats"></span> --> В игре: {{user.gameinfo()['beautiful']['total']}}
      </small>
    </p>
    % end
  </div>
  <div class="col-md-6 col-sm-5 col-xs-5">
    <p class="lead">
      <a href="/profile/{{user.user_id()}}" target="_blank">{{user.name}}</a>
    </p>
    <p>
      {{str(user.bdate)+', '+user.city_id(True).title()}}
    </p>
    % if len(user.ampluas())>0:
      <p>
      {{!'<br>'.join(['{}: {}'.format(amplua.sport_type(True).title(), amplua.title()) for amplua in user.ampluas(True)])}}
      </p>
    % end
  </div>
  <div class="col-md-4 col-sm-4 col-xs-4 text-right">
    % if loggedin and user.user_id()!=current_user.user_id():
    <a class="friendsbutton" id="{{'addfriend' if not myfriend else 'removefriend'}}-{{user.user_id()}}">
      <p>{{'+ добавить в друзья' if not myfriend else '- удалить'}}</p>
    </a>
    % end
  </div>
</div>