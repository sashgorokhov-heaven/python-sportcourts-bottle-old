import pages


class Yandex(pages.Page):
    def get(self, **kwargs):
        return pages.PageBuilder('yandex')

    get.route = '/yandex_6e70f79f0ce1999c.html'