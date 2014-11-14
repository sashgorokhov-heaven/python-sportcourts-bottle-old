import pages


@pages.get(['/', '/main', '/index'])
def index():
    return pages.PageBuilder('index')