        <meta property="og:title" content="Игра в {{game['sport_type']['title']}}" />
        <meta property="og:site_name" content="SportCourts.ru" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="http://{{serverinfo['ip']}}:{{serverinfo['port']}}"/games?game_id={{game['game_id']}}>
        <meta property="og:image" content="/images/og/games.jpg" />
        <!-- перелопатить --!>
        <meta property="og:description" content="{{game['parsed_datetime'][0][1]+' '+game['parsed_datetime'][0][0]+', '+game['parsed_datetime'][2]+', '+game['parsed_datetime'][1]}}{{'\n'+game['game_type']['title']+'\n'+str(game['cost'])+' рублей за '+str(game['duration'])+' мин'}}"/>