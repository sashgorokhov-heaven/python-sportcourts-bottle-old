% rebase("_basicpage", title=user['first_name']+' '+user['last_name'])
      <div class="row profile">
        <div class="col-md-3">
          <img src="/images/avatars/{{str(user['user_id'])}}" class="img-thumbnail profile-avatar" alt="User avatar" width="300">
        </div>
        <div class="col-md-9">
          <strong>{{user['first_name']+' '+user['last_name']}}</strong>
          % if int(user['user_id'])==int(userinfo['user_id']):
            &nbsp;&nbsp;<small><span class="glyphicon glyphicon-pencil"></span>&nbsp;<a href="/profile?edit">Ред.</a></small><br>
          % end
          % if int(user['user_id'])!=int(userinfo['user_id']):
            &nbsp;&nbsp;<small>Последний раз заходил{{'a' if user['sex']=='female' else ''}}: {{user['lasttime']}}</small><br>
          % end
          <br>
          {{user['parsed_bdate']+', '+user['city']['title']}}<br>
          <br>
          Рост: {{user['height']}} см.<br>
          Вес: {{user['weight']}} кг.<br>
          <br>
          <!-- <span class="label  label-info dropdown-toggle" data-toggle="dropdown">Сыграно: <span class="badge">42</span> часа</span>
          <ul class="dropdown-menu" role="menu">
              <li>Футбол: 3 часа</li>
              <li>Баскетбол: 6 часов</li>
              <li>Воллейбол: 30 часов</li>
          </ul>
          <br>
          <br> -->
          % if int(user['user_id'])==int(userinfo['user_id']) or userinfo['responsible'] or userinfo['usersettings'].show_phone()=='all':
          Телефон: {{user['phone']}}
          % end
          <br>
          <br>
          % if user['vkuserid']:
            <a href="http://vk.com/id{{user['vkuserid']}}" target="_blank">
              <img src="/images/static/vk.png" width="32"/>
            </a>
          % end
          % if int(user['user_id'])==int(userinfo['user_id']) and not activated:
            <p>Вы не активировали свой профиль!</p>
          % end
        </div>
      </div>