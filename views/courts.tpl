% rebase("_basicpage", title="Спортивные площадки")
      <div class="profile">
        <div class="row">
          <div class="col-md-12">
            <p class="lead">ID {{court['court_id']}} | {{court['title']}}</p>
          </div>
        </div>
        <div class="row">
          <div class="col-md-8">
            <img src="http://sportcourts.ru/images/{{court['court_id']}}_title.jpg" alt="Изображение" style="width:100%">
          </div>
          <div class="col-md-4">
            <p>Город: {{court['city']['title']}}</p>
            <p>Адрес: {{court['address']}}</p>
            <a href="#YMapsID">Показать на карте</a>
            <br><br>
            <p>Время работы:  {{court['worktime']}}</p>
            <p>Аренда от {{court['cost']}} руб./час</p>
            % if defined("game_id"):
                <p><a href="http://sportcourts.ru/games?game_id={{game_id}}">Показать ближайшую игру на этой площадке</a></p>
            % end
          </div>
        </div>
        <div class="row">
          <div class="col-md-8">
            <br>
            <ul class="nav nav-tabs">
              <li class="active"><a href="#about" data-toggle="tab">Характеристики</a></li>
              <li><a href="#text" data-toggle="tab">Описание</a></li>
            </ul>
            <div class="tab-content">
              <!-- About -->
              <div class="tab-pane active" id="about">
                <div class="row">
                  <div class="col-md-12">
                    <br>
                    <p>Виды спорта:  {{', '.join([sport['title'] for sport in court['sport_types']])}}</p>
                    <p>Размер: {{court['size']}}</p>
                    <p>Макс. кол-во игроков: {{court['max_players']}}</p>
                    <p>Тип площадки: {{court['type']}}</p>
                    <p>Покрытие: {{court['cover']}}</p>
                    <p>Инфрастуктура: {{court['infrastructure']}}</p>
                    <p>Телефон: {{court['phone']}}</p>
                    <br>
                  </div>
                </div>
              </div>
              <!-- Text -->
              <div class="tab-pane" id="text">
                <div class="row">
                  <div class="col-md-12">
                    <br>
                    <p>{{court['description']}}</p>
                    <br>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4"></div>
        </div>
        <div class="row">
          <div class="col-md-12">
            <div id="YMapsID" style="height: 500px;"></div>
            <script type="text/javascript">
              YMaps.jQuery(function () {
                  // Создание экземпляра карты и его привязка к созданному контейнеру
                  var map = new YMaps.Map(YMaps.jQuery("#YMapsID")[0]);

                  // Установка для карты ее центра и масштаба
                  map.setCenter(new YMaps.GeoPoint({{court['city']['geopoint']}}), 10);

                  // Создаем метку и добавляем ее на карту
                  var placemark = new YMaps.Placemark(new YMaps.GeoPoint({{court['geopoint']}}));
                  placemark.name = "{{court['title']}}";
                  placemark.description = "Данная площадка";
                  map.addOverlay(placemark);

                  // Открываем балун
                  placemark.openBalloon();
              });
            </script>
            <br><br>
          </div>
        </div>
      </div>