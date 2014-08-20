            % setdefault("standalone", False)
            % if standalone:
            %   rebase("_basicpage", title=game['description'])
            % end
            <div class="panel panel-default"><a name="{{game['game_id']}}"></a>
              <div class="panel-heading">
                <a href="/games?game_id={{game['game_id']}}">#{{game['game_id']}}</a>
                % if 0<adminlevel<10:
                <div style="float:right;"><a href="/games?edit={{game['game_id']}}"><span class="glyphicon glyphicon-pencil"></span></a></div>
                <div style="float:right;"><a href="/games?delete={{game['game_id']}}"><span class="glyphicon glyphicon-remove"></span></a></div>
                % end
              </div>
              <div class="panel-body">
                <div class="col-md-2">
                  <p>{{game['datetime'][0]}}</p>
                  <p>{{game['datetime'][1]}}</p>
                  <p>{{game['datetime'][2]}}</p>
                </div>
                <div class="col-md-6">
                  <p>{{game['description']}}</p>
                  <p><a href="/courts?court_id={{game['court']['court_id']}}" target="_blank">{{game['court']['title']}}</a></p>
                  <div class="progress">
                    <div class="progress-bar{{' progress-bar-success' if game['subscribed']['count'] == game['capacity'] else ''}}" role="progressbar" style="width:{{round((game['subscribed']['count']/game['capacity'])*100)}}%">
                        <span class="">{{game['subscribed']['count']}}/{{game['capacity']}}</span>
                    </div>
                  </div>
                  % if game['subscribed']['count'] > 0:
                  <div class="panel-group" id="accordion" style="margin-bottom:0px;">
                    <div class="panel panel-default">
                      <div class="panel-heading" style="text-align: center">
                        <h5 class="panel-title" style="font-size:1em;">
                          <a data-toggle="collapse" data-parent="#accordion" href="#collapse-{{game['game_id']}}">Список участников <span class="caret"></span> 
                        </h5>
                      </div>
                      <div id="collapse-{{game['game_id']}}" class="panel-collapse collapse">
                        <div class="panel-body">
                          % for n, user in enumerate(game['subscribed']['users'], 1):
                          <p><a href="/profile?user_id={{user['user_id']}}">{{'{}. {} {}'.format(n, user['first_name'], user['last_name'])}}</a></p>
                          % end
                        </div>
                      </div>
                    </div>
                  </div>
                  % end
                </div>
                <div class="col-md-2">
                  <p>{{game['cost']}} RUB за {{game['duration']}} минут</p>
                </div>
                <div class="col-md-2">
                  <div class="btn-group" style="float:right;">
                  % if loggedin:
                    % if game['subscribed']['count'] == game['capacity']:
                        <button type="button" class="btn btn-default btn-xs dropdown-toggle" {{'disabled="disabled"' if game['is_subscribed'] else ''}} data-toggle="dropdown">Места заполнены</button>
                      % if game['is_subscribed']:
                        <ul class="dropdown-menu" role="menu"><li id="{{game['game_id']}}-{{user_id}}-u"><a style="cursor:pointer;">Не пойду</a></li></ul>
                      % end
                    % end
                    % if game['subscribed']['count'] < game['capacity']:
                      % if game['is_subscribed']:
                        <button type="button" class="btn btn-success btn-xs dropdown-toggle" data-toggle="dropdown">Я записан</button>
                        <ul class="dropdown-menu" role="menu"><li id="{{game['game_id']}}-{{user_id}}-u"><a style="cursor:pointer;">Не пойду</a></li></ul>
                      % end
                      % if not game['is_subscribed']:
                        <button type="button" class="btn btn-primary btn-xs dropdown-toggle" data-toggle="dropdown">Идет набор</button>
                        <ul class="dropdown-menu" role="menu"><li id="{{game['game_id']}}-{{user_id}}"><a style="cursor:pointer;">Пойду</a></li></ul>               
                      % end
                    % end
                  % end
                  % if not loggedin:
                    % if game['subscribed']['count'] == game['capacity']:
                      <button type="button" class="btn btn-default btn-xs" disabled="disabled" data-toggle="dropdown">Места заполнены</button>
                    % end
                    % if game['subscribed']['count'] < game['capacity']:
                      <button type="button" class="btn btn-primary btn-xs" disabled="disabled" data-toggle="dropdown">Идет набор</button>
                    % end
                  % end
                </div>
                </div>
              </div>
            </div>