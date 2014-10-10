import datetime

_months_parent = ['Января', 'ФевралЯ',
           'Марта', 'Апреля',
           'Мая', 'Июня', 'Июля',
           'Августа', 'Сентября',
           'Октября', 'Ноября', 'Декабря']

_months = ['Январь', 'Февраль',
           'Март', 'Апрель',
           'Май', 'Июнь', 'Июль',
           'Август', 'Сентябрь',
           'Октябрь', 'Ноябрь', 'Декабрь']

_days = ['Понедельник', 'Вторник', 'Среда',
         'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

class BeautifulDatetime:
    def __init__(self, _datetime:datetime.datetime):
        self._datetime = _datetime

    def day(self) -> str: # '25'
        return str(self._datetime.date().day)

    def day_name(self) -> str: # 'Четверг'
        return _days[self._datetime.date().weekday()]

    def month(self, parent:bool=False) -> str: # 'Сентября' if parent else 'Сентябрь'
        return _months_parent[self._datetime.date().month-1] if parent else _months[self._datetime.date().month-1]

    def time(self) -> str: # '15:32'
        return '{}:{}'.format(self._datetime.time().hour, '0'*(2-len(str(self._datetime.time().minute)))+str(self._datetime.time().minute))

    def day_month(self) -> str: # '25 Сентября'
        return self.day()+' '+self.month(True)

    def __str__(self) -> str:
        return self.day_month()+', '+self.time()


class DateTime:
    def __init__(self, _datetime:datetime.datetime):
        self._datetime = _datetime
        self._beautiful = BeautifulDatetime(self._datetime)

    def __str__(self) -> str:
        return str(self._datetime)

    def __call__(self) -> datetime.datetime:
        return self._datetime

    @property
    def beautiful(self) -> BeautifulDatetime:
        return self._beautiful

    @property
    def today(self) -> bool:
        return self._datetime.date()==datetime.date.today()

    @property
    def tommorow(self) -> bool:
        return self._datetime.date() == datetime.date.today() + datetime.timedelta(days=1)

    @property
    def yesterday(self) -> bool:
        return self._datetime.date() == datetime.date.today() - datetime.timedelta(days=1)

    def date(self) -> datetime.date:
        return self._datetime.date()

    def time(self) -> datetime.time:
        return self._datetime.time()

class GameDateTime(DateTime):
    def __init__(self, _datetime:datetime.datetime, game):
        super().__init__(_datetime)
        self._game = game

    @property
    def can_subscribe(self) -> bool:
        return (self._datetime - datetime.datetime.now() >= datetime.timedelta(hours=1)) and self > datetime.datetime.now()

    @property
    def passed(self) -> bool:
        return (self._datetime + datetime.timedelta(minutes=self._game.duration()) < datetime.datetime.now())

    @property
    def now(self, **kwargs) -> bool:
        return self._datetime <= datetime.datetime.now() <= self._datetime + datetime.timedelta(minutes=self._game.duration())

    @property
    def soon(self) -> bool:
        return self._datetime > datetime.datetime.now() and datetime.timedelta(seconds=1) \
                                                  <= self._datetime - datetime.datetime.now() <= datetime.timedelta(hours=1)

    @property
    def can_subscribe(self) -> bool:
        return (self._datetime - datetime.datetime.now() >= datetime.timedelta(hours=1)) and self._datetime > datetime.datetime.now()

class UserAge(DateTime):
    @property
    def age(self) -> int:
        return abs(round((datetime.date.today() - self._datetime).days // 365))

    def __str__(self) -> str:
        age = str(self.age)
        postfix = ''
        prefix = int(age[-1])
        if prefix == 0 or 5 <= prefix <= 9:
            postfix = 'лет'
        elif prefix == 1:
            postfix = 'год'
        elif 2 <= prefix <= 4:
            postfix = 'года'
        return age + ' ' + postfix


class UserLastTime(DateTime):
    def __str__(self) -> str:
        timedelta = (datetime.date.today() - self._datetime.date()).days
        if timedelta == 0:
            date = 'сегодня'
        elif timedelta == 1:
            date = 'вчера'
        else:
            date = self.beautiful.day_month()
        date += ' в '+self.beautiful.time()
        return date