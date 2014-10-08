% setdefault("myfriend", False)

<div class="row">
  <div class="col-md-2 col-sm-2 col-xs-2">
    <a href="/profile?user_id={{user.user_id()}}" target="_blank">
      <img src="/images/avatars/{{user.user_id()}}" class="img-thumbnail profile-avatar" alt="User {{user.user_id()}} avatar" width="120" >
    </a>
  </div>
  <div class="col-md-6 col-sm-6 col-xs-6">
    <a href="/profile?user_id={{user.user_id()}}" target="_blank">
      <p class="lead">{{user.name}}</p>
    </a>
    <p>{{str(user.bdate)+', '+user.city_id(True).title()}}</p>
  </div>
  <div class="col-md-4 col-sm-4 col-xs-4 text-right">
    % if loggedin and user.user_id() not in {friend.user_id() for friend in myfriends} and user.user_id()!=current_user.user_id() or myfriend:
    <a class="friendsbutton" id="{{'addfriend' if not myfriend else 'removefriend'}}-{{user.user_id()}}">
      <p>{{'+ добавить в друзья' if not myfriend else '- удалить'}}</p>
    </a>
    % end
  </div>
</div>