      <div class="jumbotron">
        <div class="row">
          <div class="col-md-12 registration" style="text-align:left;">
            <h2 class="text-center">Новая площадка</h2><br>
            <form id="courtaddForm" method="post" class="form-horizontal"
            data-bv-message="This value is not valid"
            data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
            data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
            data-bv-feedbackicons-validating="glyphicon glyphicon-refresh">
                <div class="form-group">
                  <label for="inlineCheckbox" class="col-sm-2 control-label">Вид спорта</label>
                  <div class="col-sm-10">
                    <label class="checkbox-inline" style="margin-left:-17px;">
                      <input type="radio" name="sport[]" value="basket"
                      data-bv-message="Пожалуйста, выберите вид спорта"
                      data-bv-notempty="true"> Баскетбол
                    </label>
                    <label class="checkbox-inline">
                      <input type="radio" name="sport[]" value="football"> Футбол
                    </label>
                    <label class="checkbox-inline">
                      <input type="radio" name="sport[]" value="volley"> Воллейбол
                    </label>
                  </div>
                </div>
                <div class="form-group">
                  <label for="inputCity" class="col-sm-2 control-label">Адрес</label>
                  <div class="col-sm-10">
                    <input type="text" class="form-control" name="adress"
                      data-bv-message="Пожалуйста, введите адрес"
                      data-bv-notempty="true"
                      onchange="showAddress(this.address.value);return false;">
                  </div>
                  <div class="row">
                    <div id="YMapsID" style="width:600px;height:400px"></div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="court_add_amount" class="col-sm-2 control-label">Аренда</label>
                  <div class="col-sm-10">
                    <input type="text" id="court_add_amount" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0); width:150%;">
                    <div id="court_add_slider"></div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="court_add_count" class="col-sm-2 control-label">Вместимость</label>
                  <div class="col-sm-10">
                    <input type="text" id="court_add_count" readonly style="border:0; color:rgb(60,132,193); font-weight:bold; background-color: rgba(0,0,0,0);">
                    <div id="court_add_slider1"></div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="court_add_count" class="col-sm-2 control-label">Описание</label>
                  <div class="col-sm-10">
                    <textarea class="form-control" name="about" rows="3"></textarea>
                  </div>
                </div>
                <div class="form-group">
                  <div class="col-sm-offset-2 col-sm-8" style="text-align:center;">
                    <button type="submit" class="btn btn-primary">Создать</button>
                  </div>
                </div>
            </form>
            <script type="text/javascript">
                  var map, geoResult;

                  // Создание обработчика для события window.onLoad
                  YMaps.jQuery(function () {
                      // Создание экземпляра карты и его привязка к созданному контейнеру
                      map = new YMaps.Map(YMaps.jQuery("#YMapsID")[0]);

                      // Установка для карты ее центра и масштаба
                      map.setCenter(new YMaps.GeoPoint(37.64, 55.76), 10);

                      // Добавление элементов управления
                      map.addControl(new YMaps.TypeControl());
                  });

                  // Функция для отображения результата геокодирования
                  // Параметр value - адрес объекта для поиска
                  function showAddress (value) {
                      // Удаление предыдущего результата поиска
                      map.removeOverlay(geoResult);

                      // Запуск процесса геокодирования
                      var geocoder = new YMaps.Geocoder(value, {results: 1, boundedBy: map.getBounds()});

                      // Создание обработчика для успешного завершения геокодирования
                      YMaps.Events.observe(geocoder, geocoder.Events.Load, function () {
                          // Если объект был найден, то добавляем его на карту
                          // и центрируем карту по области обзора найденного объекта
                          if (this.length()) {
                              geoResult = this.get(0);
                              map.addOverlay(geoResult);
                              map.setBounds(geoResult.getBounds());
                          }else {
                              alert("Ничего не найдено")
                          }
                      });

                      // Процесс геокодирования завершен неудачно
                      YMaps.Events.observe(geocoder, geocoder.Events.Fault, function (geocoder, error) {
                          alert("Произошла ошибка: " + error);
                      })
                  }
              </script>

          </div>
        </div>
      </div> 
