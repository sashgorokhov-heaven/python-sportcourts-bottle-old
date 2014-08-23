% rebase("_basicpage", title="Спортивные площадки")
      <div class="profile">
        <div class="row">
          <div class="col-md-12">
            <p class="lead">ID 222 | Футбольный манеж "Пионер" (Футбол S)</p>
          </div>
        </div>
        <div class="row">
          <div class="col-md-8">
            <img src="http://artinvestgrup.ru/userfiles/photos/service/959c6888f2321ceddcb639ca78ddae60.jpg" alt="" style="width:100%">
          </div>
          <div class="col-md-4">
            <p>Адрес: Партийный переулок, д.1, стр.7</p>
            <a href="#YMapsID">Показать на карте</a>
            <br><br>
            <p>Время работы:  07:00- 24:00</p>
            <p>Аренда от 2000 руб./час</p>
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
                    <p>Виды спорта:  Футбол S</p>
                    <p>Размер: 32х16</p>
                    <p>Макс. кол-во игроков: 14</p>
                    <p>Тип площадки: Крытая</p>
                    <p>Покрытие: Искусственная трава</p>
                    <p>Инфрастуктура:   трибуны на 10 мест, раздевалка, душевая, освещение</p>
                    <br>
                  </div>
                </div>
              </div>
              <!-- Text -->
              <div class="tab-pane" id="text">
                <div class="row">
                  <div class="col-md-12">
                    <br>
                    <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Natus, porro, fugit repudiandae reprehenderit fugiat nobis nesciunt dolores harum tenetur fuga voluptatem nemo ullam totam non est ipsam sequi minima sapiente labore nam necessitatibus voluptate expedita doloremque incidunt eaque quo officia eum. Dolorem laborum possimus animi beatae! Pariatur repellendus qui reprehenderit?</p>
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
                  map.setCenter(new YMaps.GeoPoint(37.64, 55.76), 10);

                  // Создаем метку и добавляем ее на карту
                  var placemark = new YMaps.Placemark(new YMaps.GeoPoint(37.6, 55.7));
                  placemark.name = "Имя метки";
                  placemark.description = "Описание метки";
                  map.addOverlay(placemark);

                  // Открываем балун
                  placemark.openBalloon();
              });
            </script>
            <br><br>
          </div>
        </div>
      </div>