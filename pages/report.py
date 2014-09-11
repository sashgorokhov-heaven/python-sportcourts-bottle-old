import pages


class Report(pages.Page):
    def get(self, **kwargs):
        return pages.PageBuilder('report')

    get.route = '/report'