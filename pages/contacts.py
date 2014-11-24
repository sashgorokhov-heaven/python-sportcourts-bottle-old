import pages


@pages.get('/contacts')
def get():
    return pages.PageBuilder('contacts')