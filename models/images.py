import os

from PIL import Image


AVATARSIZE = (200, 200)


def _save_image(fullname:str, bottlefile, avatar:bool=False):
    if os.path.exists(fullname):
        os.remove(fullname)
    bottlefile.save(fullname)
    im = Image.open(fullname)
    width, heigth = im.size
    if heigth < width and avatar:
        left = (width - heigth) // 2
        top = 0
        right = left + heigth
        bottom = heigth
        im = im.crop((left, top, right, bottom))
    elif heigth > width and avatar:
        left = 0
        top = (heigth - width) // 2
        right = width
        bottom = top + width
        im = im.crop((left, top, right, bottom))
    if avatar:
        im = im.resize(AVATARSIZE)
    im.save(fullname)
    im.close()


def save_avatar(user_id:int, bottlefile):
    filename = str(user_id) + '.jpg'
    dirname = '/bsp/data/images/avatars'
    fullname = os.path.join(dirname, filename)
    _save_image(fullname, bottlefile, True)


def have_avatar(user_id:int):
    filename = str(user_id) + '.jpg'
    dirname = '/bsp/data/images/avatars'
    fullname = os.path.join(dirname, filename)
    return os.path.exists(fullname)


def delete_avatar(user_id:int):
    filename = str(user_id) + '.jpg'
    dirname = '/bsp/data/images/avatars'
    fullname = os.path.join(dirname, filename)
    if os.path.exists(fullname):
        os.remove(fullname)

def save_court_photo(court_id:int, bottlefile):
    filename = str(court_id) + '.jpg'
    dirname = '/bsp/data/images/courts/'
    fullname = os.path.join(dirname, filename)
    _save_image(fullname, bottlefile)
