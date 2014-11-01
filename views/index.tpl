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
                <form action="" style="text-align: center">
                  <input type="text" id="email" class="form-control input-lg" placeholder="Введи свой email" style="max-width:320px;">
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
        <div class="row marketing" style="margin-top: 30vh;">
          <div class="col-md-12 text-center indexpromo">
            <div id="" style="max-width: 60%; margin: 0 auto;">
              <h2>Хочешь поиграть, но не знаешь где и с кем? Ты нашел то, что искал! От желания до игры за 5 минут! (далее последовательность действий)</h2>
            </div>
          </div>
        </div>
      </div>

      <div class="row hidden-xs bigheadrow">
        <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
          <div class="text-center page1head">
            <h2>Вы уже играете и вам не хватает игроков? Подключайтесь к нам! Мы соберем участников, обзвоним всех, возьмем на себя переговоры с площадками. (Мы провели уже более 300 игр)</h2>
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
        <div class="row marketing" style="margin-top: 30vh;">
          <div class="col-md-12 text-center indexpromo">
            <div id="" style="max-width: 60%; margin: 0 auto;">
              <h2>Найдите свое место в мире любительского спорта!</h2>
              <p>Пройдите весь путь от интереса к игре, через тренировки, поиск команды, участие в турнирах к получению необходимой игровой практики, достижению собственных целей. (схема)</p>
            </div>
          </div>
        </div>
      </div>

      <div class="row hidden-xs bigheadrow">
        <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
          <div class="text-center page1head">
            <h2>Ради чего? Мы мечтаем построить динамичное и здоровое спортивное сообщество. (В России доля людей, активно занимающихся спортом - 16%. Средний показатель в Европе - 50%)</h2>
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
        <div class="row marketing" style="margin-top: 30vh;">
          <div class="col-md-12 text-center indexpromo">
            <div id="" style="max-width: 60%; margin: 0 auto;">
              <h2>Не можете играть каждую неделю? Отвлекает семья и работа? Со SportCourts это не помеха. Планируйте ваше время удобным образом!</h2>
            </div>
          </div>
        </div>
      </div>

      <div class="row hidden-xs emailrow" style="margin-bottom: -52px;">
        <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
          <div class="text-center emailhead">
            <h2>Присоединяйся к сообществу спортсменов!</h2>
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

      <div class="modal fade" id="activateModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                <h4 class="modal-title">Активируйте свой профиль</h4>
            </div>
      
            <div class="modal-body text-center">
              <br>
              <p>Сейчас на указанный Вами адрес электронной почты <span class="text-primary" id="useremail"></span> придет сообщение, содержащее ссылку для активации профиля. Если сообщения не видно в папке "Входящие", проверьте папку "Спам"</p>
              <br><br>
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
            <p><a class="btn btn-main btn-lg btn-success" href="/registration" role="button">Зарегистрироваться</a></p>
            <p class="text-center">или</p>
            <p><a class="btn btn-main btn-lg btn-primary" href="#" data-toggle="modal" data-target="#loginModal" role="button">Войти</a></p>
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