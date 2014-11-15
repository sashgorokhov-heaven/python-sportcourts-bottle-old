% rebase("_fatpage", title="Главная")
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
            <p class="h3">Ваш проводник в мире любительского спорта.</p>
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
              <img src="https://pp.vk.me/c620918/v620918493/11636/b5Nb4HPu7g0.jpg">
              <div class="carousel-caption">
              </div>
            </div>
            <!-- <div class="item">
              <img src="https://pp.vk.me/c620918/v620918493/117a7/jSIAcO1gn3A.jpg" alt="...">
              <div class="carousel-caption">
              </div>
            </div>
            <div class="item">
              <img src="https://pp.vk.me/c625829/v625829744/17f8/yxWs5iYf8UY.jpg" alt="...">
              <div class="carousel-caption">
              </div>
            </div>
            <div class="item">
              <img src="https://pp.vk.me/c620918/v620918493/11775/SvCsj0Bu6qY.jpg">
              <div class="carousel-caption">
              </div>
            </div>
            <div class="item">
              <img src="https://pp.vk.me/c620918/v620918493/116f4/hA1KaeFeLXU.jpg">
              <div class="carousel-caption">
              </div>
            </div> -->
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
      <script>
        $('.carousel').carousel();
      </script>

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
                    <h2>Просто</h2>
                    <ul class="promo-ul" style="margin-left: -24px;">
                      <li class="promo-li">регистрируйся в системе</li>
                      <li class="promo-li">выбирай подходящую игру</li>
                      <li class="promo-li">получай удовольствие!</li>
                    </ul>
                  </div>
                </div>
                <div class="col-md-4 hidden-sm">
                  <img src="/images/static/site_preview.png" style="width:100%;"/>
                </div>
                <div class="col-sm-5 col-sm-offset-2 col-md-4 col-md-offset-0 text-left">
                  <h2>Удобно</h2>
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

      <!-- <div class="row hidden-xs bigheadrow">
        <div class="row marketing" style="margin-top: 10vh;">
          <div class="col-md-12 text-center indexpromo">
            <div id="" style="max-width: 60%; margin: 0 auto;">
              <h2>Хочешь поиграть, но не знаешь где и с кем? Ты нашел то, что искал! От желания до игры за 5 минут!</h2>
              <br><br><br>
              <div class="row visible-md visible-lg" style="padding:20px;">
              </div>
              <div class="row">
                <div class="col-sm-4">
                  <h1>1</h1>
                  <p>Регистрируетесь в системе</p>
                </div>
                <div class="col-sm-4">
                  <h1>2</h1>
                  <p>Выбираете подходящую <a href="/games">игру</a> и занимаете место</p>
                </div>
                <div class="col-sm-4">
                  <h1>3</h1>
                  <p>Играете в свое удовольствие!</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div> -->

      <div class="row hidden-xs bigheadrow">
        <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
          <div class="text-center page1head">
            <h2>Вы уже играете и вам не хватает игроков? Подключайтесь к нам! Проблем с составом больше не будет.</h2>
            <br>
            <h2>Мы провели уже более 300 игр!</h2>
          </div>
          <!-- Wrapper for slides -->
          <div class="carousel-inner">
            <div class="item active">
              <img src="https://pp.vk.me/c620918/v620918493/116f4/hA1KaeFeLXU.jpg">
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
              <h2>Найди свое место в мире любительского спорта!</h2>
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
            <h2>Мы мечтаем построить в России динамичное и здоровое спортивное сообщество</h2>
            <!-- <br><br><br>
            <img src="/images/static/stats_index.png" style="width: 70%;"/> -->
          </div>
          <!-- Wrapper for slides -->
          <div class="carousel-inner">
            <div class="item active">
              <img src="https://pp.vk.me/c625829/v625829744/17f8/yxWs5iYf8UY.jpg">
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
              <h2>Не можешь играть каждую неделю? Отвлекает семья и работа? </h2>
              <br>
              <img src="http://s1.iconbird.com/ico/2013/12/505/w450h4001385925290Clock.png" alt="" height="300">
              <br>
              <h2>Со SportCourts это не помеха. Планируй свое время удобным образом!</h2>
            </div>
          </div>
        </div>
      </div>

      <!-- <div class="row hidden-xs bigheadrow">
        <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
          <div class="text-center page2head">
            <h2>Не можешь играть каждую неделю? Отвлекает семья и работа? Со SportCourts это не помеха. Планируй свое время удобным образом!</h2>
          </div>
          Wrapper for slides
          <div class="carousel-inner">
            <div class="item active">
              <img src="http://megamall.oneoweb.com/uploads/site_50/background/min/slika-_original-1319918859-559052.jpg">
              <div class="carousel-caption">
              </div>
            </div>
          </div>
        </div>
      </div> -->

      <div class="row hidden-xs emailrow" style="margin-bottom: -52px;">
        <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
          <div class="text-center emailhead">
            <h2>Будь в игре!</h2>
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
              <img src="https://pp.vk.me/c620918/v620918493/11775/SvCsj0Bu6qY.jpg">
              <div class="carousel-caption">
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Началь мобильного -->

      <div class="jumbotron visible-xs smallhead">
        <h1>SportCourts</h1>
        <p class="lead">Ваш проводник в мире любительского спорта.</p>
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
            <p>Увлекаешься спортом? Ищешь друзей для совместных занятий или соперников для твоей команды? Хочешь быть в курсе спортивных событий твоего города?</p>
          </div>

          <div class="col-md-4 text-center indexpromo">
            <p>Выбери из сотен спортивных событий своего города. Найди подходящую площадку и время. Общайся с участниками и приглашай друзей.</p>
          </div>

          <div class="col-md-4 text-center indexpromo">
            <p>Занимайся спортом. Делись своими достижениями с друзьями. Находи новые площадки и узнавай о том, что происходит вокруг.</p>
          </div>
        </div>

        <div class="row marketing">
          <div class="col-md-12 text-center">
            <h3 class="h1">Чем мы занимаемся?</h3>
            <br>
            <br>
            <br>
          </div>
          <div class="col-md-4 text-center indexpromo">
            <p>Проводим регулярные любительские игры по всему Екатеринбургу</p>
          </div>

          <div class="col-md-4 text-center indexpromo">
            <p>Размещаем на сайте актуальную информацию о площадках города.</p>
          </div>

          <div class="col-md-4 text-center indexpromo">
            <p>Организуем крутые турниры, участие в которых может принять каждый!</p>
          </div>
        </div>
      </div>