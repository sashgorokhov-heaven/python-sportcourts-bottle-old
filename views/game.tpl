            % setdefault("standalone", False)
            % if standalone:
            %   rebase("_basicpage", title=game['description'])
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
                <div id="gamepane-{{game['game_id']}}-{{tab_name}}">
                  <div class="panel panel-default {{'panel-success' if userinfo['user_id']==game['created_by']['user_id'] else 'panel-default'}} "><a name="{{game['game_id']}}"></a>
                    <div class="panel-heading">
                      <div class="panel_head">
                        <div style="float:left; max-width:45%;">
                          <a href="/games?game_id={{game['game_id']}}">#{{game['game_id']}} | {{game['description']}}</a>
                        </div>
                        <div class="organizer" style="float:right; max-width:45%;">
                          <p class="text-right">
                            % if userinfo['user_id']==game['created_by']['user_id'] or userinfo['user_id']==game['responsible_user']['user_id'] or userinfo['admin']:
                            <a href="/games?edit={{game['game_id']}}"><span class="glyphicon glyphicon-pencil"></span></a>
                            % end
                            % if userinfo['user_id']!=game['created_by']['user_id']:
                            &nbsp;&nbsp;
                            <a href="/profile?user_id={{game['created_by']['user_id']}}" target="_blank">
                              {{game['created_by']['first_name']+' '+game['created_by']['last_name']}}
                            </a>
                            &nbsp;
                            <img src="/images/avatars/{{str(game['created_by']['user_id'])}}" class="round" width="30">
                            % end
                          </p>
                        </div>
                      </div>
                    </div>
                    <div class="panel-body" style="padding-bottom:0px;">
                      <div class="row">
                        <div class="col-md-2">
                          <div class="panel panel-warning">
                            <div class="panel-heading" style="padding:4px; text-align:center;"><small>{{game['parsed_datetime'][0][1]}}</small></div>
                            <div class="panel-body" style="padding:4px; padding-bottom:0; text-align:center;">
                              <p style="margin-top:-4px; font-size: 180%;">{{game['parsed_datetime'][0][0]}}</p>
                              <small><p style="margin-top:-11px;">{{game['parsed_datetime'][2]}}</p></small>
                              <p style="margin-top:-7px;">{{game['parsed_datetime'][1]}}</p>
                            </div>
                          </div>

                          <!-- <p>{{game['parsed_datetime'][0]}}</p>
                          <p>{{game['parsed_datetime'][1]}}</p>
                          <p>{{game['parsed_datetime'][2]}}</p> -->
                        </div>
                        <div class="col-md-6">
                          <p>{{game['sport_type']['title']}} - {{game['game_type']['title']}}</p>
                          <p><a href="/courts?court_id={{game['court']['court_id']}}" target="_blank">{{game['court']['title']}}</a></p>
                          % if standalone:
                            <p>
                              Ответственный:
                              <a href="/profile?user_id={{game['responsible_user']['user_id']}}" target="_blank">
                                {{game['responsible_user']['first_name']+' '+game['responsible_user']['last_name']}}
                              </a>
                              &nbsp;
                              <img src="/images/avatars/{{str(game['responsible_user']['user_id'])}}" class="round" width="30" >
                            </p>
                            <p style="margin-top:-5px; margin-bottom:15px;">{{game['responsible_user']['phone']}}</p>
                          % end
                          <div class="progress">
                            <div class="progress-bar{{' progress-bar-success' if game['subscribed']['count'] == game['capacity'] else ''}}" role="progressbar" style="width:{{round((game['subscribed']['count']/game['capacity'])*100)}}%">
                                <span class="">{{game['subscribed']['count']}}/{{game['capacity']}}</span>
                            </div>
                          </div>
                          % if game['subscribed']['count'] > 0:
                          % if loggedin:
                          <div class="panel-group" id="accordion" style="margin-bottom:15px;">
                            <div class="panel panel-default">
                              <div class="panel-heading" style="text-align: center">
                                <h5 class="panel-title" style="font-size:1em;">
                                  <a data-toggle="collapse" data-parent="#accordion" href="#collapse-{{game['game_id']}}-{{tab_name}}">Список участников <span class="caret"></span>
                                </h5>
                              </div>
                              <div id="collapse-{{game['game_id']}}-{{tab_name}}" class="panel-collapse collapse">
                                <div class="panel-body" style="padding-bottom:5px;">
                                  % for n, user in enumerate(game['subscribed']['users'], 1):
                                  <p><a target="_blank" href="/profile?user_id={{user['user_id']}}">{{'{}. {} {}'.format(n, user['first_name'], user['last_name'])}}</a></p>
                                  % end
                                </div>
                              </div>
                            </div>
                          </div>
                          % end
                          % end
                        </div>
                        <div class="col-md-2">
                          <p>{{'FREE' if game['cost'] == 0 else str(game['cost'])+' RUB'}}</p>
                          <p>{{game['duration']}} минут</p>
                        </div>
                        <div class="col-md-2">
                          <div class="btn-group" style="float:right;">
                          % if loggedin:
                            % if game['can_subscribe']:
                              % if game['subscribed']['count'] == game['capacity']:
                                  <button type="button" class="btn btn-default btn-xs dropdown-toggle button-{{game['game_id']}}-{{userinfo['user_id']}}-u" {{'disabled="disabled"' if not game['is_subscribed'] else ''}} data-toggle="dropdown">Места заполнены</button>
                                % if game['is_subscribed']:
                                  <ul class="dropdown-menu ul-{{game['game_id']}}-{{userinfo['user_id']}}-u" role="menu">
                                    <li id="{{game['game_id']}}-{{userinfo['user_id']}}-u">
                                      <a style="cursor:pointer;">Не пойду</a>
                                    </li>
                                  </ul>
                                % end
                              % end
                              % if game['subscribed']['count'] < game['capacity']:
                                % if game['is_subscribed']:
                                  <button type="button" class="btn btn-success btn-xs dropdown-toggle button-{{game['game_id']}}-{{userinfo['user_id']}}-u" data-toggle="dropdown">Я записан{{'а' if userinfo['usersex']=='female' else ''}}</button>
                                  <ul class="dropdown-menu ul-{{game['game_id']}}-{{userinfo['user_id']}}-u" role="menu">
                                    <li id="{{game['game_id']}}-{{userinfo['user_id']}}-u">
                                      <a style="cursor:pointer;">Не пойду</a>
                                    </li>
                                  </ul>
                                % end
                                % if not game['is_subscribed']:
                                  <button type="button" class="btn btn-primary btn-xs dropdown-toggle button-{{game['game_id']}}-{{userinfo['user_id']}}" data-toggle="dropdown">Идет набор</button>
                                  <ul class="dropdown-menu ul-{{game['game_id']}}-{{userinfo['user_id']}}" role="menu">
                                    <li id="{{game['game_id']}}-{{userinfo['user_id']}}">
                                      <a style="cursor:pointer;">Пойду</a>
                                    </li>
                                  </ul>
                                % end
                              % end
                            % end
                            % if not game['can_subscribe']:
                              <button id="blocked" type="button" class="btn btn-danger btn-xs" disabled="disabled" data-toggle="tooltip" data-placement="bottom" title="До игры осталось менее 1 часа">Заблокировано</button>
                              <script type="text/javascript">
                                $('#blocked').tooltip();
                              </script>
                            % end
                          % end
                          % if not loggedin:
                            % if game['subscribed']['count'] == game['capacity']:
                              <a href="#" data-toggle="modal" data-target="#loginModal">
                                <button type="button" class="btn btn-default btn-xs" disabled="disabled" data-toggle="dropdown">Места заполнены</button>
                              </a>
                            % end
                            % if game['subscribed']['count'] < game['capacity']:
                              % if game['can_subscribe']:
                              <a href="#" data-toggle="modal" data-target="#loginModal">
                                <button type="button" class="btn btn-primary btn-xs">Идет набор</button>
                              </a>
                              % end
                              % if not game['can_subscribe']:
                                <a href="#" data-toggle="modal" data-target="#loginModal">
                                  <button id="blocked" type="button" class="btn btn-danger btn-xs" disabled="disabled" data-toggle="tooltip" data-placement="bottom" title="До игры осталось менее 1 часа">Заблокировано</button>
                                </a>
                                <script type="text/javascript">
                                  $('#blocked').tooltip();
                                </script>
                              % end
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
