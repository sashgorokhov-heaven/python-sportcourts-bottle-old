import pages


@pages.only_admins
def show_template(name:str):
    return pages.PageBuilder(name)