import pages


@pages.get('/about')
def about():
    return pages.PageBuilder('about')