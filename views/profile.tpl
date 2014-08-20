% rebase("_basicpage", title=user['first_name']+' '+user['last_name'])
      <div class="row profile">
        <div class="col-md-2">
           <img src="http://sportcourts.ru/avatars/{{str(user['user_id'])}}" alt="User avatar" width="120" style="max-width:170%">
        </div>
        <div class="col-md-1"></div>
        <div class="col-md-4">
          {{user['first_name']+' '+user['last_name']}}<br>
          {{user['bdate']+', '+user['city']['title']}}<br>
          Рост: {{user['height'}}<br>
          Рост: {{user['weight'}}<br>
          % if int(user['user_id'])==int(user_id):
            <a href="/profile?edit"><button type="button" class="btn btn-default btn-xs">Редактировать</button></a>
          % end
        </div>
      </div>