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
        <div class="yashare-auto-init" data-yashareL10n="ru" data-yashareQuickServices="vkontakte,facebook,twitter,odnoklassniki,gplus" data-yashareTheme="counter"></div>
      </div>
    </div>
  </div>
  <div class="col-md-9">
% end
    <div id="gamepane-{{game.game_id()}}-{{'None' if standalone else tab_name}}">
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
                <img src="/images/avatars/{{game.created_by()}}?sq_sm" class="round" width="30" height="30" >
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
                % include("game_conflict_handler", game=game, conflict=conflict, conflict_data=conflict_data)
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
                % if not game.reported():
                    <div class="progress-bar{{' progress-bar-success progress-bar-striped active' if len(game.subscribed()) == game.capacity() else ''}}" role="progressbar" style="width:{{round((len(game.subscribed())/game.capacity())*100)}}%">
                        <span class="">{{str(len(game.subscribed()))+'/'+str(game.capacity())}}</span>
                    </div>
                % else:
                  <div class="progress">
                    <div class="progress-bar{{' progress-bar-success progress-bar-striped active' if game.report(True)[1] >= game.capacity() else ' progress-bar-info'}}" role="progressbar" style="width:{{round(((game.capacity() if game.report(True)[1] >= game.capacity() else game.report(True)[1]) /game.capacity())*100)}}%">
                          <span class="">{{str(game.report(True)[1])+'/'+str(game.capacity())}}</span>
                    </div>
                  </div>
                % end
              </div>
              % end
              % if game.capacity() < 0:
              <p><span class="glyphicon glyphicon-user"></span> Заявок: {{len(game.subscribed())}}</p>
              % end
              % if loggedin:
                % if not game.reported() and len(game.subscribed()) > 0 or game.reported() and game.report(True)[1]>0:
                <div class="panel-group" id="accordion" style="margin-bottom:15px;">
                  <div class="panel panel-default">
                    <div class="panel-heading" style="text-align: center">
                      <h5 class="panel-title" style="font-size:1em;">
                        <a data-toggle="collapse" data-parent="#accordion" href="#collapse-{{game.game_id()}}-{{tab_name}}">Список участников <span class="caret"></span></a>
                      </h5>
                    </div>
                    <div id="collapse-{{game.game_id()}}-{{tab_name}}" class="panel-collapse collapse">
                      <div class="panel-body" style="padding-bottom:5px;">
                        % if not game.reported():
                            % for n, user in enumerate(game.subscribed(True), 1):
                                <p><a target="_blank" href="/profile?user_id={{user.user_id()}}">{{'{}. {}'.format(n, user.name)}}</a></p>
                            % end
                        % else:
                            % last = 0
                            % for n, user_id in enumerate(game.report(True)[0]['registered'], 1):
                                % user = game.report(True)[0]['registered'][user_id]
                                    <p><a target="_blank" href="/profile?user_id={{user.user_id()}}">{{'{}. {}'.format(n, user.name)}}</a></p>
                                % last = n
                            % end
                            % for n, name in enumerate(game.report(True)[0]['unregistered'], last+1):
                                <p>{{'{}. {}'.format(n, name)}}</p>
                            % end
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
              % if loggedin:
                % if game.datetime.passed:
                    <button id="blocked" type="button" class="btn btn-success btn-xs" disabled>Игра прошла</button>
                % elif game.datetime.soon:
                    <button id="blocked" type="button" class="btn btn-warning btn-xs" data-toggle="tooltip" data-placement="bottom" title="До игры осталось менее 1 часа">Скоро начнется</button>
                    <script type="text/javascript">
                      $('#blocked').tooltip();
                    </script>
                % elif game.datetime.now:
                    <button id="blocked" type="button" class="btn btn-warning btn-xs">Игра идет</button>
                % elif game.is_subscribed():
                    <button type="button" class="btn btn-success btn-xs dropdown-toggle button-{{game.game_id()}}" data-toggle="dropdown">Вы записаны</button>
                    <ul class="dropdown-menu ul-{{game.game_id()}}" role="menu">
                      <li id="{{game.game_id()}}-unsubscribe">
                        <a style="cursor:pointer;">Отписаться</a>
                      </li>
                    </ul>
                % elif game.capacity()>0 and len(game.subscribed())<game.capacity() or game.capacity()<0:
                    % if game.reserved() and current_user.user_id() in set(game.reserved_people()):
                        <button type="button" class="btn btn-warning btn-xs dropdown-toggle button-{{game.game_id()}}" data-toggle="dropdown">В резерве</button>
                        <ul class="dropdown-menu ul-{{game.game_id()}}" role="menu">
                          <li id="{{game.game_id()}}-fromreserve">
                            <a style="cursor:pointer;">В основу</a>
                          </li>
                          <li id="{{game.game_id()}}-unreserve">
                            <a style="cursor:pointer;">Выйти из резерва</a>
                          </li>
                        </ul>
                    % else:
                        <button type="button" class="btn btn-primary btn-xs dropdown-toggle button-{{game.game_id()}}" data-toggle="dropdown">Идет набор</button>
                        <ul class="dropdown-menu ul-{{game.game_id()}}" role="menu">
                          <li id="{{game.game_id()}}-subscribe">
                            <a style="cursor:pointer;">Записаться</a>
                          </li>
                        </ul>
                    % end
                % elif game.reserved():
                    % if current_user.user_id() in set(game.reserved_people()):
                        <button type="button" class="btn btn-warning btn-xs dropdown-toggle button-{{game.game_id()}}" data-toggle="dropdown">В резерве</button>
                        <ul class="dropdown-menu ul-{{game.game_id()}}" role="menu">
                          <li id="{{game.game_id()}}-unreserve">
                            <a style="cursor:pointer;">Выйти из резерва</a>
                          </li>
                        </ul>
                    % elif len(game.reserved_people())<game.reserved():
                        <button type="button" class="btn btn-default btn-xs dropdown-toggle button-{{game.game_id()}}" data-toggle="dropdown">Мест нет</button>
                        <ul class="dropdown-menu ul-{{game.game_id()}}" role="menu">
                          <li id="{{game.game_id()}}-reserve">
                            <a style="cursor:pointer;">Записаться в резерв</a>
                          </li>
                        </ul>
                    % else:
                        <button type="button" class="btn btn-default btn-xs" disabled="disabled" data-toggle="dropdown">Мест нет</button>
                    % end
                % else:
                    <button type="button" class="btn btn-default btn-xs" disabled="disabled" data-toggle="dropdown">Мест нет</button>
                % end
              % else:
                % if game.datetime.passed:
                    <button id="blocked" type="button" class="btn btn-success btn-xs" disabled>Игра прошла</button>
                % elif game.datetime.soon:
                    <button id="blocked" type="button" class="btn btn-warning btn-xs" data-toggle="tooltip" data-placement="bottom" title="До игры осталось менее 1 часа">Скоро начнется</button>
                    <script type="text/javascript">
                      $('#blocked').tooltip();
                    </script>
                % elif game.datetime.now:
                    <a href="#" data-toggle="modal" data-target="#loginModal">
                        <button id="blocked" type="button" class="btn btn-warning btn-xs">Игра идет</button>
                    </a>
                % elif game.capacity()>0 and len(game.subscribed())<game.capacity() or game.capacity()<0:
                    <a href="#" data-toggle="modal" data-target="#loginModal">
                        <button type="button" class="btn btn-primary btn-xs">Идет набор</button>
                    </a>
                % else:
                    <a href="#" data-toggle="modal" data-target="#loginModal">
                        <button type="button" class="btn btn-default btn-xs" data-toggle="dropdown">Мест нет</button>
                    </a>
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
      var game_id = arr[0], action = arr[1];
      var pane = 'None';
      $.ajax({
        url: '/subscribe',
        data: {
          game_id: game_id, action: action, tab_name:pane
        },
        async: true,
        success: function (responseData, textStatus) {
          $('#gamepane-'+game_id+'-'+pane).fadeOut('slow', function() {
              $('#gamepane-'+game_id+'-'+pane).replaceWith(responseData);
          });
        },
        error: function (response, status, errorThrown) {
          alert('Все плохо, расскажите нам про эту ошибку \n\r\n\r' + response + status + errorThrown);
        },
        type: "POST",
        dataType: "text"
      });

    });
    </script>
  % end
</div>
