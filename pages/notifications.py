import bottle

import pages
import modules.dbutils


months = ['Января', 'Февраля',
          'Марта', 'Апреля',
          'Мая', 'Июня', 'Июля',
          'Августа', 'Сентября',
          'Октября', 'Ноября', 'Декабря']
days = ['Понедельник', 'Вторник', 'Среда',
        'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def beautifuldate(datetime:str):
    date, day = datetime.split(' ')[0].split('-')[1:]
    return '{} {}'.format(day, months[int(date) - 1])


def beautifultime(datetime:str):
    return ':'.join(datetime.split(' ')[-1].split(':')[:-1])


class Notifications(pages.Page):
    path = ['notifications']

    def execute(self, method:str):
        if method == 'GET':
            data = self.get()
            if isinstance(data, pages.Template):
                return data.template()
            return data

    @pages.setlogin
    def get(self):
        if not pages.loggedin():
            return bottle.HTTPError(404)
        notifications = pages.get_notifications(pages.getuserid())
        for i in notifications:
            modules.dbutils.strdates(i)
            i['datetime'] = '{} {}'.format(beautifuldate(i['datetime']), beautifultime(i['datetime']))
        return pages.Template("notifications", notifications=notifications)

