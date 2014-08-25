% rebase("_basicpage", title="Спортивные площадки")
      <div class="profile">
        <!-- <div class="row">
          <div class="col-md-12">
            <p class="lead">{{court['title']}}</p>
          </div>
        </div> -->
        <div class="row">
          <div class="col-md-8">
            <img src="http://sportcourts.ru/images/courts/{{court['court_id']}}" alt="Изображение" class="img-thumbnail" style="width:100%;">
            <br><br><br>
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
                          <td><small><strong>Виды спорта:</strong></small></td>
                          <td><small>{{', '.join([sport['title'] for sport in court['sport_types']])}}</small></td>
                        </tr>
                        <tr>
                          <td><small><strong>Вместимость:</strong></small></td>
                          <td><small>{{court['max_players']}}</small></td>
                        </tr>
                        <tr>
                          <td><small><strong>Тип площадки:</strong></small></td>
                          <td><small>{{court['type']}}</small></td>
                        </tr>
                        <tr>
                          <td><small><strong>Покрытие:</strong></small></td>
                          <td><small>{{court['cover']}}</small></td>
                        </tr>
                        <tr>
                          <td><small><strong>Инфрастуктура:</strong></small></td>
                          <td><small>{{court['infrastructure']}}</small></td>
                        </tr>
                        <tr>
                          <td><small><strong>Комментарии:</strong></small></td>
                          <td><small>{{court['description']}}</small></td>
                        </tr>
                        <tr>
                          <td><small><strong>Телефон:</strong></small></td>
                          <td><small>{{court['phone']}}</small></td>
                        </tr>
                      </table>
                    </div>
                    <br>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <p class="lead">{{court['title']}}
              % if userinfo['organizer']:
              <small><span class="glyphicon glyphicon-pencil"></span>&nbsp;<a href="/courts?edit={{court['court_id']}}">Ред.</a></small>
              % end
            </p>
            <div class="table-responsive">
              <table class="table">
                <tr>
                  <td><small><strong>Адрес:</strong></small></td>
                  <td>
                    <small>{{court['address']}}</small>
                    <br>
                    <small><a href="#YMapsID">Показать на карте</a></small>
                  </td>
                </tr>
                <tr>
                  <td><small><strong>Время работы:</strong></small></td>
                  <td><small>{{court['worktime']}}</small></td>
                </tr>
                <tr>
                  <td><small><strong>Аренда:</strong></small></td>
                  <td><small>от {{court['cost']}} руб./час</small></td>
                </tr>
                % if defined("game"):
                <tr>
                  <td colspan="2">
                    <p><a href="http://sportcourts.ru/games?game_id={{game['game_id']}}">Ближайшая игра:</a></p>
                    <small><p>{{game['datetime'][0]}}, {{game['datetime'][2]}}, {{game['datetime'][1]}}</p></small>
                    <small><p>{{game['sport_type']['title']}} - {{game['game_type']['title']}}</p></small>
                    <div class="progress">
                      <div class="progress-bar{{' progress-bar-success' if game['subscribed']['count'] == game['capacity'] else ''}}" role="progressbar" style="width:{{round((game['subscribed']['count']/game['capacity'])*100)}}%">
                          <span class="">{{game['subscribed']['count']}}/{{game['capacity']}}</span>
                      </div>
                    </div>
                  </td>
                </tr>
                %end
              </table>
            </div>
          </div>
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