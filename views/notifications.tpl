% rebase("_basicpage", title="Уведомления")
<div class="row">
    <div class="col-md-12">
        <h1>Уведомления <span class="badge">{{len(notifications)}}</span></h1>
        % for notification in notifications:
            <div class="bs-example">
                % if notification['level']==0:
                    <div class="alert alert-info fade in">
                        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">{{notification['text']}}</button>
                        <strong>{{notification['datetime']}}</strong> Информационное уведомление
                    </div>
                % end
                % if notification['level']==1:
                    <div class="alert alert-warning fade in">
                        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">{{notification['text']}}</button>
                        <strong>{{notification['datetime']}}</strong> Предупреждение
                    </div>
                % end
                % if notification['level']==2:
                    <div class="alert alert-danger fade in">
                        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">{{notification['text']}}</button>
                        <strong>{{notification['datetime']}}</strong> Внимание
                    </div>
                % end
            </div>
        % end
    </div>
</div>