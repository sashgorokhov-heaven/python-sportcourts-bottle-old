% rebase("_basicpage", title=user['first_name']+' '+user['last_name'])
      <div class="row profile">
        <div class="col-md-3">
           <img src="http://sportcourts.ru/avatars/{{str(user['user_id'])}}" alt="User avatar" width="150" style="max-width:100%">
        </div>
        <div class="col-md-4">
          {{user['first_name']+' '+user['last_name']}}
          % if int(user['user_id'])==int(user_id):
            &nbsp;&nbsp;<small><span class="glyphicon glyphicon-pencil"></span>&nbsp;<a href="/profile?edit">Ред.</a></small>
          % end
          <br>
          {{user['bdate']+', '+user['city']['title']}}<br>
          Рост: {{user['height']}} см.<br>
          Вес: {{user['weight']}} кг.<br>
          % if user['vkuserid']:
            <a href="http://vk.com/id{{user['vkuserid']}}">Профиль вконтакте</a>
          % end
        </div>
      </div>