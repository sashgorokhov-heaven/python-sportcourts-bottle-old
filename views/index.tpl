% rebase("_fatpage", title="Главная")
      <div class="row hidden-xs bigheadrow">
        <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
          <!-- Indicators -->
          <ol class="carousel-indicators">
            <li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>
            <li data-target="#carousel-example-generic" data-slide-to="1"></li>
            <li data-target="#carousel-example-generic" data-slide-to="2"></li>
            <li data-target="#carousel-example-generic" data-slide-to="3"></li>
            <li data-target="#carousel-example-generic" data-slide-to="4"></li>
          </ol>
          <div class="text-center bighead">
            <h1>SportCourts</h1>
            <p class="lead">Ваш проводник в мире любительского спорта.</p>
            <p class="lead">Играй в <span class="gamestyped"></span> вместе с нами!</p>
            % if not loggedin:
                <p><a class="btn btn-main btn-lg btn-success" href="/registration" role="button">Зарегистрироваться</a></p>
                <p class="text-center">или</p>
                <p><a class="btn btn-main btn-lg btn-primary" href="https://oauth.vk.com/authorize?client_id=4436558&scope=email&redirect_uri=http://{{serverinfo['ip']}}:{{serverinfo['port']}}/auth&response_type=code&v=5.21" role="button">Войти через ВКонтакте</a></p>
                <p>&nbsp;</p>
            % end
          </div>
          <!-- Wrapper for slides -->
          <div class="carousel-inner" style="overflow:hidden;">
            <div class="item active">
              <img src="https://pp.vk.me/c620918/v620918493/11636/b5Nb4HPu7g0.jpg">
              <div class="carousel-caption">
              </div>
            </div>
            <div class="item">
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
            </div>
          </div>

          <!-- Controls -->
          <a class="left carousel-control" href="#carousel-example-generic" data-slide="prev">
            <span class="glyphicon glyphicon-chevron-left"></span>
          </a>
          <a class="right carousel-control" href="#carousel-example-generic" data-slide="next">
            <span class="glyphicon glyphicon-chevron-right"></span>
          </a>
        </div>
      </div>
      <script>
        $('.carousel').carousel();
      </script>
      <div class="jumbotron visible-xs smallhead">
        <h1>SportCourts</h1>
        <p class="lead">Ваш проводник в мире любительского спорта.</p>
        <p class="lead">Наша бета-версия стартовала!</p>
        % if not loggedin:
            <p><a class="btn btn-main btn-lg btn-success" href="/registration" role="button">Зарегистрироваться</a></p>
            <p class="text-center">или</p>
            <p><a class="btn btn-main btn-lg btn-primary" href="https://oauth.vk.com/authorize?client_id=4436558&scope=email&redirect_uri=http://{{serverinfo['ip']}}:{{serverinfo['port']}}/auth&response_type=code&v=5.21" role="button">Войти через ВКонтакте</a></p>
        % end
      </div>

      <div class="container">
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