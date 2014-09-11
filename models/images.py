import os

from PIL import Image


AVATARSIZE = (300, 300)


def _save_image(fullname:str, bottlefile, avatar:bool=False):
    if os.path.exists(fullname):
        os.remove(fullname)
    bottlefile.save(fullname)
    im = Image.open(fullname)
    width, height = im.size
    if avatar:
        if width > height:
            ratio = AVATARSIZE[0] / width
        else:
            ratio = AVATARSIZE[1] / height
        new_width = round(ratio * width)
        new_height = round(ratio * height)
        im = im.resize((new_width, new_height))
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
