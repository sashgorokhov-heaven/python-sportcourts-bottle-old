% rebase("_basicpage", title=user['first_name']+' '+user['last_name'])
      <div class="row profile">
        <div class="col-md-3">
           <img src="http://sportcourts.ru/avatars/{{str(user['user_id'])}}" alt="User avatar" width="150" style="min-width:100%">
        </div>
        <div class="col-md-9">
          <strong>{{user['first_name']+' '+user['last_name']}}</strong>
          % if int(user['user_id'])==int(user_id):
            &nbsp;&nbsp;<small><span class="glyphicon glyphicon-pencil"></span>&nbsp;<a href="/profile?edit">Ред.</a></small><br>
          % end
          % if int(user['user_id'])!=int(user_id):
            &nbsp;&nbsp;<small>Последний раз заходил: {{user['lasttime']}}</small><br>
          % end
          <br>
          {{user['bdate']+', '+user['city']['title']}}<br>
          <br>
          Рост: {{user['height']}} см.<br>
          Вес: {{user['weight']}} кг.<br>
          <br>
          Телефон: {{user['phone']}}<br>
          % if user['vkuserid']:
            <a href="http://vk.com/id{{user['vkuserid']}}">Профиль вконтакте</a>
          % end
          % if int(user['user_id'])==int(user_id) and not activated:
            <p>Вы не активировали свой профиль!</p>
          % end
        </div>
      </div>