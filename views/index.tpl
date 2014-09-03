% rebase("_basicpage", title="Главная")
      <div class="jumbotron">
        <h1>SportCourts</h1>
        <p class="lead">Сервис для спротсменов-любителей.</p>
        <p class="lead">Старт в августе.</p>
        % if not loggedin:
            <p><a class="btn btn-main btn-lg btn-success" href="/registration" role="button">Зарегистрироваться</a></p>
            <p class="text-center">или</p>
            <p><a class="btn btn-main btn-lg btn-primary" href="https://oauth.vk.com/authorize?client_id=4436558&scope=email&redirect_uri=http://sportcourts.ru:80/auth&response_type=code&v=5.21" role="button">Войти через ВКонтакте</a></p>
        % end
      </div>

      <div class="row marketing">
        <div class="col-lg-6">
          <h4>Проблема</h4>
          <p>В России у людей сложился сидячий образ жизни.</p>
          <p>Доля лиц, систематически занимающихся спортом около 16 процентов - ниже, чем в других развивающихся странах.</p>
          <p>К счастью, имеется тенденция к росту численности увлеченных спортом.</p>
          <p>В любительском спорте отсутствует систематизация, поэтому игроки не удовлетворяют свои потребности.</p>
        </div>

        <div class="col-lg-6">
          <h4>Решение</h4>
          <p>Справиться с этими проблемами поможет сервис, где каждый найдет свое место в мире любительского спорта.</p> 
          <p>Мы предоставим вам легкодоступный ассортимент возможностей в любом виде спорта. Подберем площадки, назначим игры и соберем на них людей.</p>
          <p>Далее, вы сможете пройти весь путь от интереса к игре, через тренировки, поиск команды, участие в турнирах к получению необходимой игровой практики, достижению собственных целей.</p>
        </div>
      </div>
