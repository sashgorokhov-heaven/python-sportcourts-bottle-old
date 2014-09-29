<meta property="og:title" content="Спортивные площадки в Екатеринбурге" />
<meta property="og:site_name" content="SportCourts.ru" />
<meta property="og:type" content="website" />
<meta property="og:url" content="http://{{serverinfo['ip']}}:{{serverinfo['port']}}"/courts?all}}>
<meta property="og:image" content="http://cdn2.img22.ria.ru/images/39169/16/391691688.jpg" />
<meta property="og:description" content="Актуальная база спортивных площадок нашего города. Здесь мы играем."/>

<script src="http://api-maps.yandex.ru/1.1/index.xml?key=ADtA-FMBAAAAO_95dwIAb8cxoJ0XVsmlrrEljkqDE8QIFgsAAAAAAAAAAADwojBjdahSnZySk0zChxiVovWqNw==" type="text/javascript"></script>

<style>
a.title.active{
	text-decoration: underline;
    font-size: 110%;
    font-weight: bold;
}
</style>

<script type="text/javascript">
    // Создание обработчика для события window.onLoad
    YMaps.jQuery(function () {
        // Создание экземпляра карты и его привязка к созданному контейнеру
        var map = new YMaps.Map(YMaps.jQuery("#YMapsID")[0]);

        // Установка для карты ее центра и масштаба
        map.setCenter(new YMaps.GeoPoint({{city['geopoint']}}), 12);

        // Добавление элементов управления
        map.enableScrollZoom();
        map.addControl(new YMaps.ToolBar());
        map.addControl(new YMaps.TypeControl());
        map.addControl(new YMaps.Zoom());

        % colors = ['redPoint', 'greenPoint', 'bluePoint', 'yellowPoint', 'orangePoint', 'darkbluePoint', 'greyPoint', 'nightPoint']
        % sport_types = {sport_type['title']:sport_type for court in courts for sport_type in court['sport_types']}
        % groups = []
        % for n, sport_type_title in enumerate(sport_types):
          % sport_type = sport_types[sport_type_title]
          % group_string = 'createGroup("{title}", [{courts}], "default#{color}")'
          % courts_list = [court for court in courts if sport_type['title'] in {sport_type['title'] for sport_type in court['sport_types']} ]
          % court_string = 'createPlacemark(new YMaps.GeoPoint({geopoint}), "{title} <br> {address}", "<a href=\'http://sportcourts.ru/courts?court_id={court_id}\' target=\'_blank\'>Подробнее</a>")'
          % court_strings = [court_string.format(geopoint=court['geopoint'], title='\\"'.join(court['title'].split('"')), address=','.join(court['address'].split(',')[-3:]), court_id=court['court_id']) for court in courts_list]
          % groups.append(group_string.format(title=sport_type['title'], courts=','.join(court_strings), color=colors[n]))
        % end
        // Группы объектов
        var groups = [
            {{!','.join(groups)}}
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
                    $('.active').removeClass("active");
                    map.removeAllOverlays();
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