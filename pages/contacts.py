import pages


@pages.get('/contacts')
def cjntacts():
    return pages.PageBuilder('contacts')