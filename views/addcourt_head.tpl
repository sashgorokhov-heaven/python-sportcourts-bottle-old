<link rel="stylesheet" href="/view/jasny/css/jasny-bootstrap.css">
<script src="/view/jasny/js/jasny-bootstrap.js"></script>
<script src="http://api-maps.yandex.ru/1.1/index.xml?key=ADtA-FMBAAAAO_95dwIAb8cxoJ0XVsmlrrEljkqDE8QIFgsAAAAAAAAAAADwojBjdahSnZySk0zChxiVovWqNw==" type="text/javascript"></script>

<script>
	$(function () {
	    $("#court_add_slider").slider({
	        value: 1000,
	        min: 0,
	        max: 10000,
	        step: 50,
	        slide: function (event, ui) {
	            $("#court_add_amount").val(ui.value);
	        }
	    });
      $("#court_add_amount").val($("#court_add_slider").slider("value"));
	});

	$(function () {
	    $("#court_add_slider1").slider({
	        value: 20,
	        min: 8,
	        max: 60,
	        step: 1,
	        slide: function (event, ui) {
	            $("#court_add_count").val(ui.value);
	        }
	    });
	    $("#court_add_count").val($("#court_add_slider1").slider("value"));
	});
</script>

<script type="text/javascript">
      var map, geoResult;

      // Создание обработчика для события window.onLoad
      YMaps.jQuery(function () {
          // Создание экземпляра карты и его привязка к созданному контейнеру
          map = new YMaps.Map(YMaps.jQuery("#YMapsID")[0]);

          // Установка для карты ее центра и масштаба
          map.setCenter(new YMaps.GeoPoint({{cities[0].geopoint()}}), 10);

          // Добавление элементов управления
          map.addControl(new YMaps.Zoom());
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
                  document.getElementById('address').value = geoResult.text;
                  document.getElementById('geopoint').value = this.get(0).getGeoPoint();
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