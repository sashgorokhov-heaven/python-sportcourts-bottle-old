<meta property="og:title" content="Игра в {{game.sport_type(True).title()}}" />
<meta property="og:site_name" content="SportCourts.ru" />
<meta property="og:type" content="website" />
<meta property="og:url" content="http://{{serverinfo['ip']}}:{{serverinfo['port']}}/games/{{game.game_id()}}">
<meta property="og:image" content="/images/og/sport_{{game.sport_type(True).sport_id()}}.jpg" />
<meta property="og:description" content="Рекомендую посетить игру 
{{game.datetime.beautiful}}
{{game.game_type(True).title()}}"/>
<!-- перелопатить 
<meta property="og:description" content="{{game.datetime.beautiful}}{{'\n'+game.game_type(True).title()+'\n'+str(game.cost())+' рублей за '+str(game.duration())+' мин'}}"/>-->