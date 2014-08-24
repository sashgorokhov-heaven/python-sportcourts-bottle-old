% rebase("_basicpage", title="Спортивные площадки")
      <div class="profile">
        <div class="row">
          <div class="col-md-12">
            <p class="lead">ID {{court['court_id']}} | {{court['title']}}</p>
          </div>
        </div>
        <div class="row">
          <div class="col-md-8">
            <img src="http://sportcourts.ru/images/courts/{{court['court_id']}}" alt="Изображение" class="img-thumbnail" style="width:100%;">
          </div>
          <div class="col-md-4">
            <div class="table-responsive">
              <table class="table">
                <tr>
                  <td><strong>Адрес:</strong></td>
                  <td>
                    {{court['address']}}
                    <br>
                    <a href="#YMapsID">Показать на карте</a>
                  </td>
                </tr>
                <tr>
                  <td><strong>Время работы:</strong></td>
                  <td>{{court['worktime']}}</td>
                </tr>
                <tr>
                  <td><strong>Аренда:</strong></td>
                  <td>от {{court['cost']}} руб./час</td>
                </tr>
                % if defined("game_id"):
                <tr>
                  <td colspan="2"><a href="http://sportcourts.ru/games?game_id={{game_id}}">Ближайшая игра</a></td>
                </tr>
                % end
              </table>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-8">
            <br>
            <ul class="nav nav-tabs">
              <li class="active"><a href="#about" data-toggle="tab">Характеристики</a></li>
              <!-- <li><a href="#text" data-toggle="tab">Описание</a></li> -->
            </ul>
            <div class="tab-content">
              <!-- About -->
              <div class="tab-pane active" id="about">
                <div class="row">
                  <div class="col-md-12">
                    <br>
                    <div class="table-responsive">
                      <table class="table table-hover">
                        <tr>
                          <td><strong>Виды спорта:</strong></td>
                          <td>{{', '.join([sport['title'] for sport in court['sport_types']])}}</td>
                        </tr>
                        <tr>
                          <td><strong>Вместимость:</strong></td>
                          <td>{{court['max_players']}}</td>
                        </tr>
                        <tr>
                          <td><strong>Тип площадки:</strong></td>
                          <td>{{court['type']}}</td>
                        </tr>
                        <tr>
                          <td><strong>Покрытие:</strong></td>
                          <td>{{court['cover']}}</td>
                        </tr>
                        <tr>
                          <td><strong>Инфрастуктура:</strong></td>
                          <td>{{court['infrastructure']}}</td>
                        </tr>
                        <tr>
                          <td><strong>Комментарии:</strong></td>
                          <td>{{court['description']}}</td>
                        </tr>
                        <tr>
                          <td><strong>Телефон:</strong></td>
                          <td>{{court['phone']}}</td>
                        </tr>
                      </table>
                    </div>
                    <br>
                  </div>
                </div>
              </div>
              <!-- <div class="tab-pane" id="text">
                <div class="row">
                  <div class="col-md-12">
                    <br>
                    <p>{{court['description']}}</p>
                    <br>
                  </div>
                </div>
              </div> -->
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
                  map.setCenter(new YMaps.GeoPoint({{court['geopoint']}}), 15);

                  map.addControl(new YMaps.Zoom());
                  map.addControl(new YMaps.MiniMap());
                  map.addControl(new YMaps.ScaleLine());

                  // Создаем метку и добавляем ее на карту
                  var placemark = new YMaps.Placemark(new YMaps.GeoPoint({{court['geopoint']}}), 5);
                  placemark.name = "{{court['title']}}";
                  placemark.description = "{{court['address']}}";
                  map.addOverlay(placemark);

                  // Открываем балун
                  placemark.openBalloon();
              });
            </script>
            <br><br>
          </div>
        </div>
      </div>