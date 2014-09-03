% rebase("_basicpage", title="Карта площадок")
      <div class="profile">
        <!-- <div class="row">
          <div class="col-md-12">
            <p class="lead">{{court['title']}}</p>
          </div>
        </div> -->
        <div class="row">
          <div class="col-md-8">
            <div id="YMapsID" style="height: 500px;"></div>
          </div>
          <div class="col-md-4">
            <ul id="menu"></ul>
          </div>
        </div>
      </div>

      <script type="text/javascript">
          // Создание обработчика для события window.onLoad
          YMaps.jQuery(function () {
              // Создание экземпляра карты и его привязка к созданному контейнеру
              var map = new YMaps.Map(YMaps.jQuery("#YMapsID")[0]);

              // Установка для карты ее центра и масштаба
              map.setCenter(new YMaps.GeoPoint(60.609926,56.835525), 13);

              // Добавление элементов управления
              map.enableScrollZoom();
              map.addControl(new YMaps.ToolBar());
              map.addControl(new YMaps.TypeControl());
              map.addControl(new YMaps.Zoom());

              // Группы объектов
              var groups = [
                  createGroup("Баскетбол", [
                      createPlacemark(new YMaps.GeoPoint(60.626331,56.83745), "110 гимназия \"Бажова, 124\"", "<a href='http://vk.com/im'>Подробнее</a>"),
                      createPlacemark(new YMaps.GeoPoint(60.582513,56.838528), "2 гимназия", "Пестеревский переулок"),
                  ], "default#redPoint"),
                  createGroup("Футбол", [
                      createPlacemark(new YMaps.GeoPoint(60.573806,56.832385), "Центральный стадион \"ФК Урал\"", "ул.Репина, 5")
                  ], "default#greenPoint")
              ];

              // Создание списка групп
              for (var i = 0; i < groups.length; i++) {
                  addMenuItem(groups[i], map, YMaps.jQuery("#menu"));
              }
          })

          // Добавление одного пункта в список
          function addMenuItem (group, map, menuContainer) {

              // Показать/скрыть группу на карте
              YMaps.jQuery("<a class=\"title\" href=\"#\">" + group.title + "</a>")
                  .bind("click", function () {
                      var link = YMaps.jQuery(this);

                      // Если пункт меню "неактивный", то добавляем группу на карту,
                      // иначе - удаляем с карты
                      if (link.hasClass("active")) {
                          map.removeOverlay(group);
                      } else {
                          map.addOverlay(group);
                      }

                      // Меняем "активность" пункта меню
                      link.toggleClass("active");

                      return false;
                  })

                  // Добавление нового пункта меню в список
                  .appendTo(
                      YMaps.jQuery("<li></li>").appendTo(menuContainer)
                  )
          };

          // Создание группы
          function createGroup (title, objects, style) {
              var group = new YMaps.GeoObjectCollection(style);

              group.title = title;
              group.add(objects);
              
              return group;
          };

          // Создание метки
          function createPlacemark (point, name, description) {
              var placemark = new YMaps.Placemark(point);

              placemark.name = name;
              placemark.description = description;

              return placemark
          }
      </script>