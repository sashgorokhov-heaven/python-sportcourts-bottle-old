import pages


class Game_team1(pages.Page):
    def get(self, **kwargs):
        return pages.PageBuilder('game_team1')

    get.route = '/game_team1'