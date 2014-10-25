import bottle

import pages

# from modules import dbutils


class Finances(pages.Page):
    def get(self, **kwargs):
        raise bottle.HTTPError(404)

    # if not pages.auth_dispatcher.admin():
    #            raise bottle.HTTPError(404)
    #        with dbutils.dbopen() as db:
    #            games = db.execute("SELECT * FROM games WHERE datetime+INTERVAL duration MINUTE<NOW() AND game_id IN (SELECT game_id FROM usergames)", dbutils.dbfields['games'])
    #            games_dict = {game['game_id']:game for game in games}
    #            courts = db.execute("SELECT * FROM courts", dbutils.dbfields['courts'])
    #            courts = {court['court_id']:court for court in courts}
    #            usergames = db.execute("SELECT * FROM usergames", dbutils.dbfields['usergames'])
    #            #games = list(filter(lambda x: x['game_id'] in set(map(lambda y: y['game_id'], usergames)), games))
    #            ideal = sum([game['capacity']*game['cost'] for game in games if game['capacity']>0])
    #            response = list()
    #            response.append('Идеальный доход {}р ({} игр)'.format(ideal, len(games)))
    #            lost = sum([(game['capacity']-len(list(filter(lambda x: x['game_id']==game['game_id'] and x['status']!=-2, usergames))))*game['cost'] for game in games])
    #            ideal -= lost
    #            response.append('Потеряно изза пустых мест: {}р'.format(lost))
    #            lost = sum([len(list(filter(lambda x: x['game_id']==game['game_id'] and x['status']==0, usergames)))*game['cost'] for game in games])
    #            ideal -= lost
    #            response.append('Потеряно изза непришедших: {}р'.format(lost))
    #            lost = sum([len(list(filter(lambda x: x['game_id']==game['game_id'] and x['status']==1, usergames)))*game['cost'] for game in games])
    #            ideal -= lost
    #            response.append('Потеряно изза неоплативших: {}р'.format(lost))
    #            response.append('Реальный доход: {}р'.format(ideal))
    #            expence = sum([courts[game['court_id']]['cost']*(game['duration']/60) for game in games])
    #            response.append('Расходы на аренду: {}'.format(expence))
    #            response.append('Прибыль: {} ({}%)'.format(ideal-expence, round(((ideal-expence)/ideal)*100, 1)))
    #            ideal -= expence
    #            sport_ids = set(map(lambda x: x['sport_type'], games))
    #            money_by_sport = dict()
    #            for sport_id in sport_ids:
    #                money = sum([len(list(filter(lambda x: x['game_id']==game['game_id'] and x['status']==2, usergames)))*game['cost']-courts[game['court_id']]['cost']*(game['duration']/60) for game in games])
    #                money_by_sport[sport_id] = money
    #                response.append('{}: {}р ({}%)'.format(sport_id, money, round((money/ideal)*100, 1)))
    #
    #            vitaliy = lena = sasha = 0
    #
    #            vitaliy += (money_by_sport[1]//2)//2
    #            sasha += (money_by_sport[1]//2)//2
    #            lena += money_by_sport[1]//2
    #
    #            response.append('Зарплаты: ')
    #            response.append('Виталий: {}р ({}%)'.format(vitaliy, round((vitaliy/ideal)*100), 1))
    #            response.append('Александр: {}р ({}%)'.format(sasha, round((sasha/ideal)*100), 1))
    #            response.append('Елена: {}р ({}%)'.format(lena, round((lena/ideal)*100), 1))
    #
    #            return '<br>'.join(response)

    get.route = '/fin'