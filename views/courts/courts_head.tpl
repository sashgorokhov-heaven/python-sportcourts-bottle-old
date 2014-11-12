<meta property="og:title" content="{{court.title()}}" />
<meta property="og:site_name" content="SportCourts.ru" />
<meta property="og:type" content="website" />
<meta property="og:url" content="http://{{serverinfo['ip']}}:{{serverinfo['port']}}"/courts?court_id={{court.court_id()}}>
<meta property="og:image" content="/images/og/games.jpg" />
<meta property="og:description" content="Рекомендую площадку {{court.title()}}, {{court.address()}}"/>

<script src="http://api-maps.yandex.ru/1.1/index.xml?key=ADtA-FMBAAAAO_95dwIAb8cxoJ0XVsmlrrEljkqDE8QIFgsAAAAAAAAAAADwojBjdahSnZySk0zChxiVovWqNw==" type="text/javascript"></script>

<script type="text/javascript">
  YMaps.jQuery(function () {
      // Создание экземпляра карты и его привязка к созданному контейнеру
      var map = new YMaps.Map(YMaps.jQuery("#YMapsID")[0]);

      // Установка для карты ее центра и масштаба
      map.setCenter(new YMaps.GeoPoint({{court.geopoint()}}), 15);

      map.addControl(new YMaps.Zoom());
      map.addControl(new YMaps.MiniMap());
      map.addControl(new YMaps.ScaleLine());

      // Создаем метку и добавляем ее на карту
      var placemark = new YMaps.Placemark(new YMaps.GeoPoint({{court.geopoint()}}), 5);
      placemark.name = "{{court.title()}}";
      placemark.description = "{{court.address()}}";
      map.addOverlay(placemark);

      // Открываем балун
      placemark.openBalloon();
  });
</script>