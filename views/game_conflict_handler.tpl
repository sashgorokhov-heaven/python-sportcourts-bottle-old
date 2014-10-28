<div class="modal fade" id="GameMsg{{game.game_id()}}Modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Ошибка</h4>
      </div>
      <div class="modal-body">
        % if conflict == 1:
          <p>Вы не смогли записаться на игру, так как вы уже записаны на другую в это же время</p>
          <ul>
            <li>проверьте свои заявки на другие игры</li>
            <li>сделайте наилучший выбор =)</li>
          </ul>
          <p>Если вы нашли неточности и ошибки в описании игры, свяжитесь с администраторами сервиса.</p>
        % end
        % if conflict == 2:
          <p>Вы не смогли записаться на игру, так как получили бан от администраторов. Скорее всего вы:</p>
          <ul>
            <li>пропустили игру без предупреждения</li>
            <li>нарушали правила сервиса</li>
          </ul>
          <p>Чтобы снять бан, свяжитесь с администраторами сервиса.</p>
        % end
        % if conflict == 3:
          <p>Вы не можете записаться игру, пока ваш аккаунт не активирован</p>
          <ul>
            <li>проверьте свою почту, в том числе вкладку "Спам"</li>
            <li>активируйте аккаунс, перейдя по ссылке в письме</li>
            <li>Profit =)</li>
          </ul>
          <p>Если вы нашли неточности и ошибки в описании игры, свяжитесь с администраторами сервиса.</p>
        % end
        % if conflict == 4:
          <p>Вы не можете записаться игру, все места уже заняты</p>
          <ul>
            <li>вы можете подождать, пока освободится место</li>
          </ul>
          <p>Если вы нашли неточности и ошибки в описании игры, свяжитесь с администраторами сервиса.</p>
        % end
        % if conflict == 5:
          <p>Вы уже подписаны на данную игру =)</p>
          <br>
          <p>Спасибо за то, что играете с нами!</p>
          <br>
          <p>Если вы нашли неточности и ошибки в описании игры, свяжитесь с администраторами сервиса.</p>
        % end
        % if conflict == 6:
          <p>Вы уже отписались от данной игры или никогда на нее не подписывались</p>
        % end
      </div>
      <div class="modal-footer">
        <a class="btn btn-success" href="/profile?user_id=1">Написать администраторам</a>
        <button type="button" data-dismiss="modal" class="btn btn-primary">Закрыть</button>
      </div>
    </div>
  </div>
</div>
<script>
  $('#GameMsg{{game.game_id()}}Modal').modal('show');
</script>