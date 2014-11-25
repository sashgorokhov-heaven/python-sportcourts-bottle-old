import pages


@pages.get(['/', '/main', '/index'])
def index():
    return pages.PageBuilder('index')


@pages.get('/about')
def about():
    return pages.PageBuilder('about')


@pages.get('/contacts')
def get():
    return pages.PageBuilder('contacts')