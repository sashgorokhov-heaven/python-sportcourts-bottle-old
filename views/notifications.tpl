% rebase("_basicpage", title="Уведомления")
% total = len(notifications['all'])+len(notifications['subscribed'])
% if 'responsible' in notifications:
    % total += len(notifications['responsible'])
% end
<div class="container" style="margin-top:50px;">
<div class="row clearfix">
        <div class="col-md-12 column">
            <h1>{{'Старые' if all else 'Новые'}} уведомления <span class="badge notify">{{total}}</span>
            % if all and total>0:
                <small><a href="/notifications?deleteall">Удалить все</a></small>
            % end
            <div class="tabbable" id="tabs-655216">
                <ul class="nav nav-tabs">
                    <li {{'class=disabled' if len(notifications['all'])==0 else ''}}>
                        <a href="#all" data-toggle="tab">Общие
                        % if len(notifications['all'])>0:
                            <span class="badge">{{len(notifications['all'])}}</span>
                        % end
                        </a>
                    </li>
                    <li {{'class=disabled' if len(notifications['subscribed'])==0 else ''}}>
                        <a href="#subscribed" data-toggle="tab">Мои игры
                        % if len(notifications['subscribed'])>0:
                            <span class="badge">{{len(notifications['subscribed'])}}</span>
                        % end
                        </a>
                    </li>
                    % if 'responsible' in notifications:
                    <li {{'class=disabled' if len(notifications['responsible'])==0 else ''}}>
                        <a href="#responsible" data-toggle="tab">Ответсвенность
                        % if len(notifications['responsible'])>0:
                            <span class="badge">{{len(notifications['responsible'])}}</span>
                        % end
                        </a>
                    </li>
                    % end
                </ul>
                <div class="tab-content">
                    <div class="tab-pane" id="all">
                        % for notification in notifications['all']:
                          <div class="bs-example" style="margin-top:20px;">
                            % if notification['level']==0:
                              <div class="alert alert-info fade in">
                                <button type="button" id="{{notification['notification_id']}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                                <small><p>Информационное уведомление | {{notification['datetime']}}</p></small>
                                <p class="lead">{{!notification['text']}}</p>
                              </div>
                            % end
                            % if notification['level']==1:
                              <div class="alert alert-warning fade in">
                                <button type="button" id="{{notification['notification_id']}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                                <small><p>Предупреждение | {{notification['datetime']}}</p></small>
                                <p class="lead">{{!notification['text']}}</p>
                              </div>
                            % end
                            % if notification['level']==2:
                              <div class="alert alert-danger fade in">
                                <button type="button" id="{{notification['notification_id']}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                                <small><p>Внимание | {{notification['datetime']}}</p></small>
                                <p class="lead">{{!notification['text']}}</p>
                              </div>
                            % end
                          </div>
                        % end
                        % if len(notifications['all'])==0:
                            <p>Уведомлений нет</p>
                        % end
                    </div>
                    <div class="tab-pane active" id="subscribed">
                        % for notification in notifications['subscribed']:
                          <div class="bs-example" style="margin-top:20px;">
                            % if notification['level']==0:
                              <div class="alert alert-info fade in">
                                <button type="button" id="{{notification['notification_id']}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                                <small><p>Информационное уведомление | {{notification['datetime']}}</p></small>
                                <p class="lead">{{!notification['text']}}</p>
                              </div>
                            % end
                            % if notification['level']==1:
                              <div class="alert alert-warning fade in">
                                <button type="button" id="{{notification['notification_id']}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                                <small><p>Предупреждение | {{notification['datetime']}}</p></small>
                                <p class="lead">{{!notification['text']}}</p>
                              </div>
                            % end
                            % if notification['level']==2:
                              <div class="alert alert-danger fade in">
                                <button type="button" id="{{notification['notification_id']}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                                <small><p>Внимание | {{notification['datetime']}}</p></small>
                                <p class="lead">{{!notification['text']}}</p>
                              </div>
                            % end
                          </div>
                        % end
                        % if len(notifications['subscribed'])==0:
                            <p>Уведомлений нет</p>
                        % end
                    </div>
                    % if 'responsible' in notifications:
                    <div class="tab-pane active" id="responsible">
                        % for notification in notifications['responsible']:
                          <div class="bs-example" style="margin-top:20px;">
                            % if notification['level']==0:
                              <div class="alert alert-info fade in">
                                <button type="button" id="{{notification['notification_id']}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                                <small><p>Информационное уведомление | {{notification['datetime']}}</p></small>
                                <p class="lead">{{!notification['text']}}</p>
                              </div>
                            % end
                            % if notification['level']==1:
                              <div class="alert alert-warning fade in">
                                <button type="button" id="{{notification['notification_id']}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                                <small><p>Предупреждение | {{notification['datetime']}}</p></small>
                                <p class="lead">{{!notification['text']}}</p>
                              </div>
                            % end
                            % if notification['level']==2:
                              <div class="alert alert-danger fade in">
                                <button type="button" id="{{notification['notification_id']}}" class="close" data-dismiss="alert" aria-hidden="true">x</button>
                                <small><p>Внимание | {{notification['datetime']}}</p></small>
                                <p class="lead">{{!notification['text']}}</p>
                              </div>
                            % end
                          </div>
                        % end
                        % if len(notifications['responsible'])==0:
                            <p>Уведомлений нет</p>
                        % end
                    </div>
                    % end
                </div>
            </div>
        </div>
    </div>
</div>