% rebase("_basicpage", title="Уведомления")
% total = len(notifications['all'])+len(notifications['subscribed'])
% if 'responsible' in notifications:
    % total += len(notifications['responsible'])
% end
  <div class="row" style="margin-top:30px;">
    &nbsp;
  </div>

  <div class="row">
    <div class="col-md-12">
      <h1>
        {{'Старые' if all else 'Новые'}} уведомления 
        <span class="badge notify">{{total}}</span>
        % if all and total>0:
          <small><a href="/notifications?deleteall">Удалить все</a></small>
        % end
      </h1>
      </br>
      <ul class="nav nav-tabs">
        <li  class="active">
          <a href="#all" data-toggle="tab">{{!'<b>Общие</b>' if len(notifications['all'])>len(notifications['subscribed']) and ('responsible' in notifications and len(notifications['all'])>len(notifications['responsible'])) else 'Общие'}}
          % if len(notifications['all'])>0:
              <span class="badge notify_all">{{len(notifications['all'])}}</span>
          % end
          </a>
        </li>
        <li>
            <a href="#subscribed" data-toggle="tab">{{!'<b>Мои игры</b>' if len(notifications['subscribed'])>len(notifications['all']) and ('responsible' in notifications and len(notifications['subscribed'])>len(notifications['responsible'])) else 'Мои игры'}}
            % if len(notifications['subscribed'])>0:
                <span class="badge notify_subscribed">{{len(notifications['subscribed'])}}</span>
            % end
            </a>
        </li>
        % if 'responsible' in notifications:
        <li>
            <a href="#responsible" data-toggle="tab">{{!'<b>Ответственность</b>' if len(notifications['responsible'])>len(notifications['all']) and len(notifications['responsible'])>len(notifications['subscribed']) else 'Ответственность'}}
            % if len(notifications['responsible'])>0:
                <span class="badge notify_responsible">{{len(notifications['responsible'])}}</span>
            % end
            </a>
        </li>
        % end
      </ul>
      <div class="tab-content">
        <div class="tab-pane active" id="all">
            % for notification in notifications['all']:
              <div class="bs-example" style="margin-top:20px;">
                % if notification.level()==0:
                  <div class="alert alert-info fade in">
                    <button type="button" id="{{notification.notification_id()}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                    <small><p>Информационное уведомление | {{notification.datetime.beautiful}}</p></small>
                    <p class="lead">{{!notification.text()}}</p>
                  </div>
                % end
                % if notification.level()==1:
                  <div class="alert alert-warning fade in">
                    <button type="button" id="{{notification.notification_id()}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                    <small><p>Предупреждение | {{notification.datetime.beautiful}}</p></small>
                    <p class="lead">{{!notification.text()}}</p>
                  </div>
                % end
                % if notification.level()==2:
                  <div class="alert alert-danger fade in">
                    <button type="button" id="{{notification.notification_id()}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                    <small><p>Внимание | {{notification.datetime.beautiful}}</p></small>
                    <p class="lead">{{!notification.text()}}</p>
                  </div>
                % end
              </div>
            % end
            % if len(notifications['all'])==0:
              <div class="bs-example" style="margin-top:20px;">
                <div class="alert alert-info fade in">
                  <p class="lead">Уведомлений нет</p>
                </div>
              </div>
            % end
        </div>
        <div class="tab-pane" id="subscribed">
            % for notification in notifications['subscribed']:
              <div class="bs-example" style="margin-top:20px;">
                % if notification.level()==0:
                  <div class="alert alert-info fade in">
                    <button type="button" id="{{notification.notification_id()}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                    <small><p>Информационное уведомление | {{notification.datetime.beautiful}}</p></small>
                    <p class="lead">{{!notification.text()}}</p>
                  </div>
                % end
                % if notification.level()==1:
                  <div class="alert alert-warning fade in">
                    <button type="button" id="{{notification.notification_id()}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                    <small><p>Предупреждение | {{notification.datetime.beautiful}}</p></small>
                    <p class="lead">{{!notification.text()}}</p>
                  </div>
                % end
                % if notification.level()==2:
                  <div class="alert alert-danger fade in">
                    <button type="button" id="{{notification.notification_id()}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                    <small><p>Внимание | {{notification.datetime.beautiful}}</p></small>
                    <p class="lead">{{!notification.text()}}</p>
                  </div>
                % end
              </div>
            % end
            % if len(notifications['subscribed'])==0:
              <div class="bs-example" style="margin-top:20px;">
                <div class="alert alert-info fade in">
                  <p class="lead">Уведомлений нет</p>
                </div>
              </div>
            % end
        </div>
        % if 'responsible' in notifications:
        <div class="tab-pane" id="responsible">
            % for notification in notifications['responsible']:
              <div class="bs-example" style="margin-top:20px;">
                % if notification.level()==0:
                  <div class="alert alert-info fade in">
                    <button type="button" id="{{notification.notification_id()}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                    <small><p>Информационное уведомление | {{notification.datetime.beautiful}}</p></small>
                    <p class="lead">{{!notification.text()}}</p>
                  </div>
                % end
                % if notification.level()==1:
                  <div class="alert alert-warning fade in">
                    <button type="button" id="{{notification.notification_id()}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                    <small><p>Предупреждение | {{notification.datetime.beautiful}}</p></small>
                    <p class="lead">{{!notification.text()}}</p>
                  </div>
                % end
                % if notification.level()==2:
                  <div class="alert alert-danger fade in">
                    <button type="button" id="{{notification.notification_id()}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                    <small><p>Внимание | {{notification.datetime.beautiful}}</p></small>
                    <p class="lead">{{!notification.text()}}</p>
                  </div>
                % end
              </div>
            % end
            % if len(notifications['responsible'])==0:
              <div class="bs-example" style="margin-top:20px;">
                <div class="alert alert-info fade in">
                  <p class="lead">Уведомлений нет</p>
                </div>
              </div>
            % end
        </div>
        % end
      </div>
    </div>
  </div>