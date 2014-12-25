% rebase("_fatpage", title="Будь в игре!")
% import random
<div class="row hidden-xs bigheadrow">
  <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
    <!-- Indicators -->
    <!-- <ol class="carousel-indicators">
      <li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>
      <li data-target="#carousel-example-generic" data-slide-to="1"></li>
      <li data-target="#carousel-example-generic" data-slide-to="2"></li>
      <li data-target="#carousel-example-generic" data-slide-to="3"></li>
      <li data-target="#carousel-example-generic" data-slide-to="4"></li>
    </ol> -->
    <div class="text-center bighead">
      <h1>SportCourts</h1>
      <h2 class="h3">Ваш проводник в мире любительского спорта.</h2>
      <p class="h3">Играй в <span class="gamestyped"></span> вместе с {{random.choice(["нами", "друзьями"])}}!</p>
      <br><br>
      % if not loggedin:
        <div id="reg1">
          <p>
            <a id="regbutton" class="btn btn-main btn-lg btn-success" role="button">Зарегистрироваться</a>
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
        <p class="text-center">или</p>
        <p><a class="btn btn-main btn-lg btn-primary" href="#" data-toggle="modal" data-target="#loginModal" role="button">Войти</a></p>
      % end
    </div>
    <!-- Wrapper for slides -->
    <div class="carousel-inner" style="overflow:hidden;">
      <div class="item active">
        <img src="/images/static/main_1.jpg" alt="Играем в баскетбол в Екатеринбурге">
        <div class="carousel-caption">
        </div>
      </div>
    </div>

    <!-- Controls -->
    <!-- <a class="left carousel-control" href="#carousel-example-generic" data-slide="prev">
      <span class="glyphicon glyphicon-chevron-left"></span>
    </a>
    <a class="right carousel-control" href="#carousel-example-generic" data-slide="next">
      <span class="glyphicon glyphicon-chevron-right"></span>
    </a> -->
  </div>
</div>

<div class="row hidden-xs bigheadrow">
  <div class="row marketing" style="margin-top: 15vh;">
    <div class="col-md-12 text-center indexpromo">
      <div id="" style="max-width: 80%; margin: 0 auto;">
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
    <div class="text-center page1head">
      <h3 class="h2">Вы уже играете и вам не хватает игроков? Подключайтесь к нам! Проблем с составом больше не будет.</h3>
      <br>
      <h3 class="h2">Мы провели уже более 300 игр!</h3>
    </div>
    <!-- Wrapper for slides -->
    <div class="carousel-inner">
      <div class="item active">
        <img src="/images/static/main_2.jpg" alt="SportCourts решает все острые проблемы в организации любительских игр">
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
  <div class="row marketing" style="margin-top: 10vh;">
    <div class="col-md-12 text-center indexpromo">
      <div id="" style="max-width: 60%; margin: 0 auto;">
        <p class="h2">Не можешь играть каждую неделю? Отвлекает семья и работа? </p>
        <br>
        <img src="/images/static/main_4.png" alt="" height="300">
        <br>
        <p class="h2">Со SportCourts это не помеха. Планируй свое время удобным образом!</p>
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
  <h1>SportCourts</h1>
  <h2 class="lead">Ваш проводник в мире любительского спорта.</h2>
  <p class="lead">Играй в <span class="gamestyped"></span> вместе с {{random.choice(["нами", "друзьями"])}}!</p>
  % if not loggedin:
      <div id="reg3">
        <p>
          <a id="regbutton" class="btn btn-lg btn-success" role="button">Зарегистрироваться</a>
        </p>
      </div>
      <div id="reg4" hidden class="input-group" style="min-width:440px; margin: 0 auto; margin-bottom:10px; display: none;">
        <form action="/registration/email" method="POST" style="text-align: center">
          <input type="text" id="email3" name="email" class="form-control input-lg" placeholder="Введи свой email" style="max-width:260px;">
          <span class="input-group-btn">
            <a id="email3button" class="btn btn-success btn-lg" disabled>Присоединиться</a>
          </span>
        </form>
      </div>
      <p class="text-center">или</p>
      <p><a class="btn btn-lg btn-primary" href="#" data-toggle="modal" data-target="#loginModal" role="button">Войти</a></p>
      <p>&nbsp;</p>
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