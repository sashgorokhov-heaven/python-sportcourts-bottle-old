<div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="/admin">Админка</a>
      % import config
      <a class="topmenu" href="#">Время запуска: {{config.starttime}}</a>
    </div>
    <div class="navbar-collapse collapse text-right">
      <ul class="nav navbar-nav navbar-right">
        <li>
          <a class="navbar-brand" href="/" target="_blank">На главную</a>
        </li>
        <li>
          <a class="topmenu" href="/profile">
            <img src="/images/avatars/{{current_user.user_id()}}?sq_sm" class="img-circle" width="30" height="30" style="margin-top: -6px; margin-bottom:-5px;">
          </a>
        </li>
        <li><a class="topmenu" href="/logout">Выход</a></li>
      <!--
        <li><a href="#">Dashboard</a></li>
        <li><a href="#">Settings</a></li>
        <li><a href="#">Profile</a></li>
        <li><a href="#">Help</a></li>
      </ul> -->
      <!-- <form class="navbar-form navbar-right">
        <input type="text" class="form-control" placeholder="Search...">
      </form> -->
      </ul>
    </div>
  </div>
</div>