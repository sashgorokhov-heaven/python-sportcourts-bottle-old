% rebase("_basicpage", title="Уведомление")
<div class="jumbotron" style="margin-top:85px;">
    <h2>{{!message}}</h2>
    % if defined("description"):
        <p class="lead">{{!description}}</p>
    % end
</div>