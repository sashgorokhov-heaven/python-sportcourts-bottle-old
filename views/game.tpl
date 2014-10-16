% setdefault("standalone", False)
% setdefault("conflict", 0)
% setdefault("conflict_data", None)

% if standalone:
%   rebase("_basicpage", title=game.description())
% end

% setdefault("tab_name", "none")

% if standalone:
<div class="row">
  <div class="col-md-12"  style="margin-top:50px;">
    &nbsp;
  </div>
</div>
% end

% if standalone:
<div class="row">
  <div class="col-md-3">
    <div class="panel panel-default">
      <div class="panel-body">
        <p class="lead">Поделиться</p>
        <script type="text/javascript" src="//yandex.st/share/share.js"
        charset="utf-8"></script>
        <div class="yashare-auto-init" data-yashareL10n="ru"
         data-yashareQuickServices="vkontakte,facebook,twitter,odnoklassniki,gplus" data-yashareTheme="counter"

        ></div> 
      </div>
    </div>
  </div>
  <div class="col-md-9">
% end
    <div id="gamepane-{{game.game_id()}}-{{tab_name}}">
      <div class="panel panel-default {{'panel-success' if current_user.user_id()==game.created_by() else 'panel-default'}} "><a name="{{game.game_id()}}"></a>
        <div class="panel-heading">
          <div class="panel_head">
            <div style="float:left; max-width:45%;">
              <a href="/games?game_id={{game.game_id()}}">#{{game.game_id()}} | {{game.description()}}</a>
            </div>
            <div class="organizer" style="float:right; max-width:45%;">
              <p class="text-right">
                % if current_user.user_id()==game.created_by() or current_user.user_id()==game.responsible_user_id() or current_user.userlevel.admin():
                <a href="/games?edit={{game.game_id()}}"><span class="glyphicon glyphicon-pencil"></span></a>
                % end
                % if current_user.user_id()!=game.created_by():
                &nbsp;&nbsp;
                <a href="/profile?user_id={{game.created_by()}}" target="_blank">
                  {{game.created_by(True).name}}
                </a>
                &nbsp;
                <img src="/images/avatars/{{game.created_by()}}?sq" class="round" width="30" height="30" >
                % end
              </p>
            </div>
          </div>
        </div>
        <div class="panel-body" style="padding-bottom:0px;">
          <div class="row">
            <div class="col-md-2">
              <div class="panel panel-warning" style="max-width:150px; margin: 0 auto 15px auto;">
                <div class="panel-heading" style="padding:4px; text-align:center;"><small>{{game.datetime.beautiful.month()}}</small></div>
                <div class="panel-body" style="padding:4px; padding-bottom:0; text-align:center;">
                  <p style="margin-top:-4px; font-size: 180%;">{{game.datetime.beautiful.day()}}</p>
                  <small><p style="margin-top:-11px;">{{game.datetime.beautiful.day_name()}}</p></small>
                  <p style="margin-top:-7px;">{{game.datetime.beautiful.time()}}</p>
                  % if game.datetime.tommorow:
                    <p><span class="label label-info">Завтра</span></p>
                  % end
                  % if game.datetime.today:
                    <p><span class="label label-info">Сегодня</span></p>
                  % end
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <p>{{game.sport_type(True).title()}} - {{game.game_type(True).title()}}</p>
              <p><a href="/courts?court_id={{game.court_id()}}" target="_blank">{{game.court_id(True).title()}}</a></p>

              % if conflict>0:
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
              % end

              % if standalone:
                <p>
                  Ответственный:
                  <a href="/profile?user_id={{game.responsible_user_id()}}" target="_blank">
                    {{game.responsible_user_id(True).name}}
                  </a>
                  &nbsp;
                  <img src="/images/avatars/{{str(game.responsible_user_id())}}?sq" class="round" width="30" >
                </p>
                <p style="margin-top:-5px; margin-bottom:15px;">{{game.responsible_user_id(True).phone()}}</p>
              % end
              % if game.capacity()>0:
              <div class="progress">
                <div class="progress-bar{{' progress-bar-success' if len(game.subscribed()) == game.capacity() else ''}}" role="progressbar" style="width:{{round((len(game.subscribed())/game.capacity())*100)}}%">
                    <span class="">{{str(len(game.subscribed()))+'/'+str(game.capacity())}}</span>
                </div>
              </div>
              % end
              % if game.capacity() < 0:
              <p><span class="glyphicon glyphicon-user"></span> Заявок: {{len(game.subscribed())}}</p>
              % end
              % if len(game.subscribed()) > 0:
              % if loggedin:
              <div class="panel-group" id="accordion" style="margin-bottom:15px;">
                <div class="panel panel-default">
                  <div class="panel-heading" style="text-align: center">
                    <h5 class="panel-title" style="font-size:1em;">
                      <a data-toggle="collapse" data-parent="#accordion" href="#collapse-{{game.game_id()}}-{{tab_name}}">Список участников <span class="caret"></span>
                    </h5>
                  </div>
                  <div id="collapse-{{game.game_id()}}-{{tab_name}}" class="panel-collapse collapse">
                    <div class="panel-body" style="padding-bottom:5px;">
                      % for n, user in enumerate(game.subscribed(True), 1):
                      <p><a target="_blank" href="/profile?user_id={{user.user_id()}}">{{'{}. {}'.format(n, user.name)}}</a></p>
                      % end
                    </div>
                  </div>
                </div>
              </div>
              % end
              % end
            </div>
            <div class="col-md-2">
              <p>{{'FREE' if game.cost() == 0 else str(game.cost())+' RUB'}}</p>
              <p>{{game.duration()}} минут</p>
            </div>
            <div class="col-md-2">
              <div class="btn-group" style="float:right;">
              % if loggedin and game.can_subscribe():
                % if len(game.subscribed()) == game.capacity():
                  <button type="button" class="btn btn-default btn-xs dropdown-toggle button-{{game.game_id()}}-{{current_user.user_id()}}-u" {{'disabled="disabled"' if not game.is_subscribed() else ''}} data-toggle="dropdown">Места заполнены</button>
                  % if game.reserved()>0 and len(game.reserved_people())<game.reserved() and current_user.user_id() not in set((game.reserved_people()):
                    <ul class="dropdown-menu ul-{{game.game_id()}}-{{current_user.user_id()}}" role="menu">
                      <li id="{{game.game_id()}}-{{current_user.user_id()}}">
                        <a style="cursor:pointer;">Записаться в резерв</a>
                      </li>
                    </ul>
                  % end

                  % if current_user.user_id() in set((game.reserved_people()):
                    <ul class="dropdown-menu ul-{{game.game_id()}}-{{current_user.user_id()}}-u" role="menu">
                      <li id="{{game.game_id()}}-{{current_user.user_id()}}-u">
                        <a style="cursor:pointer;">Не пойду</a>
                      </li>
                    </ul>
                  % end

                  % if game.is_subscribed():
                    <ul class="dropdown-menu ul-{{game.game_id()}}-{{current_user.user_id()}}-u" role="menu">
                      <li id="{{game.game_id()}}-{{current_user.user_id()}}-u">
                        <a style="cursor:pointer;">Не пойду</a>
                      </li>
                    </ul>
                  % end
                % end

                % if len(game.subscribed()) < game.capacity() or game.capacity()<0:
                  % if game.is_subscribed():
                    <button type="button" class="btn btn-success btn-xs dropdown-toggle button-{{game.game_id()}}-{{current_user.user_id()}}-u" data-toggle="dropdown">Я записан{{'а' if current_user.sex()=='female' else ''}}</button>
                    <ul class="dropdown-menu ul-{{game.game_id()}}-{{current_user.user_id()}}-u" role="menu">
                      <li id="{{game.game_id()}}-{{current_user.user_id()}}-u">
                        <a style="cursor:pointer;">Не пойду</a>
                      </li>
                    </ul>
                  % end

                  % if current_user_user.user_id() in set((game.reserved_people()):
                    <button type="button" class="btn btn-success btn-xs dropdown-toggle button-{{game.game_id()}}-{{current_user.user_id()}}-u" data-toggle="dropdown">Я в резерве</button>
                    <ul class="dropdown-menu ul-{{game.game_id()}}-{{current_user.user_id()}}-u" role="menu">
                      <li id="{{game.game_id()}}-{{current_user.user_id()}}-u">
                        <a style="cursor:pointer;">Не пойду</a>
                      </li>
                    </ul>
                  % end

                  % if not game.is_subscribed():
                    <button type="button" class="btn btn-primary btn-xs dropdown-toggle button-{{game.game_id()}}-{{current_user.user_id()}}" data-toggle="dropdown">Идет набор</button>
                    <ul class="dropdown-menu ul-{{game.game_id()}}-{{current_user.user_id()}}" role="menu">
                      <li id="{{game.game_id()}}-{{current_user.user_id()}}">
                        <a style="cursor:pointer;">Пойду</a>
                      </li>
                    </ul>
                  % end
                % end
              % end
              % if not loggedin and game.can_subscribe():
                % if len(game.subscribed()) == game.capacity():
                  <a href="#" data-toggle="modal" data-target="#loginModal">
                    <button type="button" class="btn btn-default btn-xs" disabled="disabled" data-toggle="dropdown">Места заполнены</button>
                  </a>
                % end
                % if len(game.subscribed()) < game.capacity():
                  <a href="#" data-toggle="modal" data-target="#loginModal">
                    <button type="button" class="btn btn-primary btn-xs">Идет набор</button>
                  </a>
                % end
              % end
              
              % if not game.can_subscribe():
                % if game.datetime.soon:
                    <button id="blocked" type="button" class="btn btn-warning btn-xs" data-toggle="tooltip" data-placement="bottom" title="До игры осталось менее 1 часа">Скоро начнется</button>
                    <script type="text/javascript">
                      $('#blocked').tooltip();
                    </script>
                % end
                % if game.datetime.now:
                    <button id="blocked" type="button" class="btn btn-warning btn-xs">Игра идет</button>
                % end
                % if game.datetime.passed:
                    <button id="blocked" type="button" class="btn btn-success btn-xs" disabled>Игра прошла</button>
                % end
              % end
              </div>
              <br>
              <br>
            </div>
          </div>
        </div>
      </div>
    % if standalone:
    </div>
    <div class="row">
      <div class="col-md-12">
        <div class="page-header" style="margin-top:0">
          <h3>Комментарии</h3>
        </div>

        <!-- Put this div tag to the place, where the Comments block will be -->
        <div id="vk_comments"></div>
        <script type="text/javascript">
        VK.Widgets.Comments("vk_comments", {limit: 5, attach: "*", autoPublish: "0", pageUrl: window.location.toString()});
        </script>

      </div>
    </div>
  </div>
  % end

  % if loggedin and standalone:
  <script type="text/javascript">
    $(document).on('click', 'li', function() {
      arr = $(this).attr("id").split('-');
      var user_id = arr[1],
        game_id = arr[0],
        unsubscribe = arr[2];
      if (unsubscribe=='u') {
        $.ajax({
          url: '/subscribe',
          data: {
            game_id: game_id,
            unsubscribe: 0
          },
          async: true,
          success: function (responseData, textStatus) {
            // alert(responseData + ' Status: ' + textStatus);
            alert('Теперь вас нет в списках на игру');
            // document.location.href = '/games#game' + game_id;
            window.location.reload();
          },
          error: function (response, status, errorThrown) {
            alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
          },
          type: "POST",
          dataType: "text"
        });
      } else {
        $.ajax({
          url: '/subscribe',
          data: {
            game_id: game_id
          },
          async: true,
          success: function (responseData, textStatus) {
            // alert(responseData + ' Status: ' + textStatus);
            alert('Вы успешно записаны на игру');
            // document.location.href = '/games#game' + game_id;
            window.location.reload();
          },
          error: function (response, status, errorThrown) {
            alert('Все плохо' + response + status + errorThrown);
          },
          type: "POST",
          dataType: "text"
        });
      }
    });
  </script>
  % end
</div>
