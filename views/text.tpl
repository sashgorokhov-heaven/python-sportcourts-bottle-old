% rebase("_basicpage", title="Уведомление")
<div class="row">
  <div class="col-md-12" style="margin-top:50px;">
    <h1>{{!message}}</h1>
    % if defined("description"):
        <p class="lead">{{!description}}</p>
    % end
  </div>
</div>