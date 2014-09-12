from modules import dbutils
import models


class UserGameInfo(models.JsonDBData):
    def full_playtime(self):
        pass

    def by_sport_type(self, sport_type:int) -> int:
        if sport_type in self.sport_types():
            return self._get('sport_types')[sport_type]
        else:
            raise KeyError(sport_type)

    def sport_types(self):
        if isinstance(self._get('sport_types'), dict):
            return set(self._get('sport_types').keys())
        return set()

    def add(self, sport_type:int, value:int):
        if sport_type in self.sport_types():
            self._get('sport_types')[sport_type] += value
        else:
            self._get('sport_types')[sport_type] = value


@models.autodb
def get(user_id:int, dbconnection:dbutils.DBConnection=None) -> UserGameInfo:
    pass