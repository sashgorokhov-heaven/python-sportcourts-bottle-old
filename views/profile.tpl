% rebase("_basicpage", title=user['first_name']+' '+user['last_name'])
      <div class="row profile">
        <div class="col-md-3">
          <img src="/images/avatars/{{str(user['user_id'])}}" class="img-thumbnail profile-avatar" alt="User avatar" width="300">
        </div>
        <div class="col-md-9">
          <strong>{{user['first_name']+' '+user['last_name']}}</strong>
          % if int(user['user_id'])==int(userinfo['user_id']):
            &nbsp;
            &nbsp;
            &nbsp;
            <small>
              <span class="glyphicon glyphicon-pencil"></span>
              <a href="/profile?edit">Ред.</a>
              &nbsp;
              &nbsp;
              &nbsp;
              <span class="glyphicon glyphicon-cog"></span>
              <a href="/settings">Настройки</a>
            </small>
            <br>
          % end
          % if int(user['user_id'])!=int(userinfo['user_id']):
            &nbsp;
            &nbsp;
            <small>Последний раз заходил{{'a' if user['sex']=='female' else ''}}: {{user['lasttime']}}</small><br>
          % end
          <br>
          {{user['parsed_bdate']+', '+user['city']['title']}}<br>
          <br>
          Рост: {{user['height']}} см.<br>
          Вес: {{user['weight']}} кг.<br>
          <br>
          % if user['gameinfo']['total']>0:
            <span class="label  label-info dropdown-toggle" data-toggle="dropdown">Сыграно: <span class="badge">{{user['gameinfo']['beautiful']['total'][0]}}</span> {{user['gameinfo']['beautiful']['total'][1]}}</span>
            <ul class="dropdown-menu" role="menu">
            % for sport_id in user['gameinfo']['sport_types']:
                <li>{{user['gameinfo']['sport_types'][sport_id]}}: {{' '.join(user['gameinfo']['beautiful'][sport_id])}}</li>
            % end
            </ul>
            <br>
            <br>
          % end
          % if int(user['user_id'])==int(userinfo['user_id']) or userinfo['responsible'] or user['settings'].show_phone()=='all' or len(user['userlevel'].intersection({0,1}))>0:
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