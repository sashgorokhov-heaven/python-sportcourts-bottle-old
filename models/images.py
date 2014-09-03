import os

from PIL import Image


AVATARSIZE = (200, 200)


def _save_image(fullname:str, bottlefile):
    if os.path.exists(fullname):
        os.remove(fullname)
    bottlefile.save(fullname)
    im = Image.open(fullname)
    im.save(fullname)
    im.close()


def save_avatar(user_id:int, bottlefile):
    filename = str(user_id) + '.jpg'
    dirname = '/bsp/data/avatars'
    fullname = os.path.join(dirname, filename)
    _save_image(fullname, bottlefile)


def save_court_photo(court_id:int, bottlefile):
    filename = str(court_id) + '.jpg'
    dirname = '/bsp/data/images/courts/'
    fullname = os.path.join(dirname, filename)
    _save_image(fullname, bottlefile)
