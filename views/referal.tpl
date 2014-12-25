% rebase("_fatpage", title=str(user.name)+" приглашает вас")
% import random
<div class="row hidden-xs referalheadrow">
  <div class="text-center referalhead">
    <div class="referalheaddark">
      <br><br><br>
      <img src="/images/avatars/{{user.user_id()}}" class="img-circle referal-avatar" width="150" height="150">
      <h1 class="h2">{{user.name}}</h1>
      <p class="lead">Приглашает вас присоединиться к SportCourts.ru</p>
      <p class="h4">Зарегистрируйтесь прямо сейчас и получите пробную тренировку в подарок</p>
      <br><br>
      % if not loggedin:
      <div id="reg1">
        <p>
          <a id="regbutton" class="btn btn-main btn-lg btn-success" role="button">Присоединиться к SportCourts.ru</a>
        </p>
      </div>
      <div id="reg2" hidden class="input-group" style="min-width:498px; margin: 0 auto; margin-bottom:10px; display: none;">
        <form action="/registration/email" method="POST" style="text-align: center">
          <input type="text" id="email" name="email" class="form-control input-lg" placeholder="Введи свой email" style="max-width:320px;">
          <span class="input-group-btn">
            <a id="emailbutton" class="btn btn-main btn-lg btn-success" disabled>Присоединиться</a>
          </span>
        </form>
      </div>
      <br>
      % end
      % if loggedin:
      <p class="text-center">Чтобы пригласить своих друзей на эту страницу</p>
      <p class="text-center">расскажите про нее в соцсетях:</p>
      <script type="text/javascript" src="//yandex.st/share/share.js" charset="utf-8"></script>
      <div class="yashare-auto-init" data-yashareL10n="ru"data-yashareQuickServices="vkontakte,facebook,twitter,odnoklassniki" data-yashareTheme="counter" style="margin-left: -5px; display: inline;"></div>
      % end
    </div>
  </div>
  <div class="item-ref" style="text-align:center;">
    <img src="/images/static/main_1.jpg" alt="Играем в баскетбол в Екатеринбурге">
  </div>
</div>

<div class="row hidden-xs bigheadrow">
  <div class="row marketing" style="margin-top: 10vh;">
    <div class="col-md-12 text-center indexpromo">
      <div id="" style="max-width: 80%; margin: 0 auto; padding:10px;">
        <h2>SportCourts.ru - это сообщество для тех, кто любит спорт и активный образ жизни.</h2>
        <br>
        <h2>Хочешь поиграть, но не знаешь где и с кем? Ты нашел то, что искал! От желания до игры за 5 минут!</h2>
        <br><br><br>
        <div class="row visible-md visible-lg" style="padding:20px;">
        </div>
        <div class="row">
          <div class="col-sm-5 col-md-4">
            <div class="text-left" style="float:right;">
              <h3 class="h2">Просто</h3>
              <ul class="promo-ul" style="margin-left: -24px;">
                <li class="promo-li">регистрируйся в системе</li>
                <li class="promo-li">выбирай подходящую игру</li>
                <li class="promo-li">получай удовольствие!</li>
              </ul>
            </div>
          </div>
          <div class="col-md-4 hidden-sm">
            <img src="/images/static/site_preview.png" style="width:100%;" alt="SportCourts - это удобное приложение для любителей спорта."/>
          </div>
          <div class="col-sm-5 col-sm-offset-2 col-md-4 col-md-offset-0 text-left">
            <h3 class="h2">Удобно</h3>
            <ul class="promo-ul" style="margin-left: -24px;">
              <li class="promo-li">пользуйся с любого устройства</li>
              <li class="promo-li">задавай вопросы организаторам</li>
              <li class="promo-li">меняй свои планы одним кликом!</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="row hidden-xs bigheadrow">
  <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
    <div class="text-center page2head">
      <p class="h2">Мы мечтаем построить в России динамичное и здоровое спортивное сообщество</p>
    </div>
    <!-- Wrapper for slides -->
    <div class="carousel-inner">
      <div class="item active">
        <img src="/images/static/main_3.jpg" alt="SportCourts - это развивающееся спортивное сообщество">
        <div class="carousel-caption">
        </div>
      </div>
    </div>
  </div>
</div>

<div class="row hidden-xs bigheadrow">
  <div class="row marketing" style="margin-top: 18vh;">
    <div class="col-md-12 text-center indexpromo">
      <div id="" style="max-width: 80%; margin: 0 auto;">
        <div class="img-row">
          <img src="/images/static/1.png" style="width:100px;"/>
          <img src="/images/static/2.png" style="width:100px;"/>
          <img src="/images/static/3.png" style="width:100px;"/>
          <img src="/images/static/4.png" style="width:100px;"/>
          <img src="/images/static/5.png" style="width:100px;"/>
          <img src="/images/static/6.png" style="width:100px;"/>
          <img src="/images/static/7.png" style="width:100px;"/>
          <img src="/images/static/8.png" style="width:100px;"/>
          <img src="/images/static/9.png" style="width:100px;"/>
        </div>
        <br><br>
        <h3 class="h2">Найди свое место в мире любительского спорта!</h3>
        <p>Пройди весь путь от интереса к игре, через тренировки, поиск команды, участие в турнирах к получению необходимой игровой практики, достижению собственных целей.</p>
        <br><br>
        <div class="img-row">
          <img src="/images/static/10.png" style="width:100px;"/>
          <img src="/images/static/11.png" style="width:100px;"/>
          <img src="/images/static/12.png" style="width:100px;"/>
          <img src="/images/static/13.png" style="width:100px;"/>
          <img src="/images/static/14.png" style="width:100px;"/>
          <img src="/images/static/15.png" style="width:100px;"/>
          <img src="/images/static/16.png" style="width:100px;"/>
          <img src="/images/static/17.png" style="width:100px;"/>
          <img src="/images/static/18.png" style="width:100px;"/>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="row hidden-xs emailrow" style="margin-bottom: -52px;">
  <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
    <div class="text-center emailhead">
      <h3 class="h2">Будь в игре!</h3>
      <br><br>
      <div class="input-group" style="min-width:498px; margin: 0 auto;">
        <form action="" style="text-align: center">
          <input type="text" id="email1" class="form-control input-lg" placeholder="Введи свой email" style="max-width:320px;">
          <span class="input-group-btn">
            <a id="email1button" class="btn btn-main btn-lg btn-success" disabled>Присоединиться</a>
          </span>
        </form>
      </div><!-- /input-group -->
    </div>
    <!-- Wrapper for slides -->
    <div class="carousel-inner">
      <div class="item active">
        <img src="/images/static/main_5.jpg" alt="SportCourts. Будь в игре!">
        <div class="carousel-caption">
        </div>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="activateModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
          <h4 class="modal-title">Активируйте свой профиль</h4>
      </div>
      <div class="modal-body text-center">
        <br><br>
        <span id="userclient"></span>
        <br><br>
      </div>
    </div>
  </div>
</div>

<!-- Началь мобильного -->

<div class="jumbotron visible-xs smallhead smallpage">
  <img src="/images/avatars/{{user.user_id()}}" class="img-circle referal-avatar" width="150" height="150">
  <h1 class="h2">{{user.name}}</h1>
  <p class="lead">Приглашает вас присоединиться к SportCourts.ru</p>
  <p class="h4">Зарегистрируйтесь прямо сейчас и получите пробную тренировку в подарок</p>
  <br><br>
  % if not loggedin:
  <div id="reg1">
    <p>
      <a id="regbutton" class="btn btn-main btn-lg btn-success" role="button">Присоединиться к SportCourts.ru</a>
    </p>
  </div>
  <div id="reg2" hidden class="input-group" style="min-width:498px; margin: 0 auto; margin-bottom:10px; display: none;">
    <form action="/registration/email" method="POST" style="text-align: center">
      <input type="text" id="email" name="email" class="form-control input-lg" placeholder="Введи свой email" style="max-width:320px;">
      <span class="input-group-btn">
        <a id="emailbutton" class="btn btn-main btn-lg btn-success" disabled>Присоединиться</a>
      </span>
    </form>
  </div>
  <br>
  % end
  % if loggedin:
  <p class="text-center">Чтобы пригласить своих друзей на эту страницу</p>
  <p class="text-center">расскажите про нее в соцсетях:</p>
  <script type="text/javascript" src="//yandex.st/share/share.js" charset="utf-8"></script>
  <div class="yashare-auto-init" data-yashareL10n="ru"data-yashareQuickServices="vkontakte,facebook,twitter,odnoklassniki" data-yashareTheme="counter" style="margin-left: -5px; display: inline;"></div>
  <br><br>
  % end
</div>

<div class="container visible-xs">
  <div class="row marketing">
    <div class="col-md-4 text-center indexpromo">
      <p class="smallpagetext">Увлекаешься спортом? Ищешь друзей для совместных занятий или соперников для твоей команды? Хочешь быть в курсе спортивных событий твоего города?</p>
    </div>

    <div class="col-md-4 text-center indexpromo">
      <p class="smallpagetext">Выбери из сотен спортивных событий своего города. Найди подходящую площадку и время. Общайся с участниками и приглашай друзей.</p>
    </div>

    <div class="col-md-4 text-center indexpromo">
      <p class="smallpagetext">Занимайся спортом. Делись своими достижениями с друзьями. Находи новые площадки и узнавай о том, что происходит вокруг.</p>
    </div>
  </div>

  <div class="row marketing">
    <div class="col-md-12 text-center">
      <h2 class="h1">Чем мы занимаемся?</h3>
      <br>
      <br>
      <br>
    </div>
    <div class="col-md-4 text-center indexpromo">
      <p class="smallpagetext">Проводим регулярные любительские игры по всему Екатеринбургу</p>
    </div>

    <div class="col-md-4 text-center indexpromo">
      <p class="smallpagetext">Размещаем на сайте актуальную информацию о площадках города.</p>
    </div>

    <div class="col-md-4 text-center indexpromo">
      <p class="smallpagetext">Организуем крутые турниры, участие в которых может принять каждый!</p>
    </div>
  </div>
</div>