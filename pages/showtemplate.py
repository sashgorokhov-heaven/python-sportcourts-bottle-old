import pages


@pages.get('/showtpl/<tplname>')
@pages.only_admins
def show_template(tplname:str):
    return pages.PageBuilder(tplname)