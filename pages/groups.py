import pages


@pages.get('/groups')
def groups():
    return pages.PageBuilder('groups')


@pages.post('/groups')
@pages.only_organizers
def add_group():
    raise NotImplementedError


@pages.get('/groups/<group_id:int>')
def group(group_id:int):
    raise NotImplementedError