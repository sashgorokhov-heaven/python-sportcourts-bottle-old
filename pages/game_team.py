import pages


class Game_team(pages.Page):
    def get(self, **kwargs):
        return pages.PageBuilder('game_team')

    get.route = '/game_team'