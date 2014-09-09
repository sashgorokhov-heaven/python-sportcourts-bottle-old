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