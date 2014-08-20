% rebase("_basicpage", title=user['first_name']+' '+user['last_name'])
      <div class="row profile">
        <div class="col-md-3">
           <img src="http://sportcourts.ru/avatars/{{str(user['user_id'])}}" alt="User avatar" width="240" style="max-width:100%">
        </div>
        <div class="col-md-4">
          {{user['first_name']+' '+user['last_name']}}
          % if int(user['user_id'])==int(user_id):
            &nbsp;&nbsp;<a href="/profile?edit"><button type="button" class="btn btn-default btn-xs">Редактировать</button></a>
          % end
          <br>
          {{user['bdate']+', '+user['city']['title']}}<br>
          Рост: {{user['height']}} см.<br>
          Вес: {{user['weight']}} кг.<br>
        </div>
      </div>