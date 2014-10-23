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