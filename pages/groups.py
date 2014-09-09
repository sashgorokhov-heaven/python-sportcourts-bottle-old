import pages


class Groups(pages.Page):
    def get(self, **kwargs):
        return pages.PageBuilder('groups')

    get.route = '/groups'