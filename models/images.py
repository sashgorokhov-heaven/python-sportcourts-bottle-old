import os
import urllib.request
import config
from modules import logging
from PIL import Image


AVATARSIZE = (300, 300)


def _save_image(fullname:str, bottlefile):
    if os.path.exists(fullname):
        os.remove(fullname)
    bottlefile.save(fullname)


def _save_avatar(user_id:int):
    filename = str(user_id) + '.jpg'
    fullname = os.path.join(config.paths.images.avatars, filename)

    original = Image.open(fullname)
    width, height = original.size
    if width > height:
        ratio = AVATARSIZE[0] / width
    else:
        ratio = AVATARSIZE[1] / height
    new_width = round(ratio * width)
    new_height = round(ratio * height)
    resized = original.resize((new_width, new_height))
    resized.save(fullname)

    if new_height > new_width:
        new_height = new_width
    if new_width > new_height:
        new_width = new_height
    cropped = resized.crop((0, 0, new_width, new_height))
    cropped.save(os.path.join(config.paths.images.avatars, str(user_id) + '_sq.jpg'))

    small = cropped.resize((50, 50))
    small.save(os.path.join(config.paths.images.avatars, str(user_id) + '_sq_sm.jpg'))

    original.close()
    resized.close()
    cropped.close()
    small.close()


def save_avatar(user_id:int, bottlefile):
    filename = str(user_id) + '.jpg'
    fullname = os.path.join(config.paths.images.avatars, filename)
    delete_avatar(user_id)
    bottlefile.save(fullname)
    try:
        _save_avatar(user_id)
    except Exception as e:
        logging.message('Error saving avatar <{}>'.format(user_id), e)



def save_avatar_from_url(user_id:int, url:str):
    fullname = os.path.join(config.paths.images.avatars, str(user_id) + '.jpg')
    delete_avatar(user_id)
    urllib.request.urlretrieve(url, fullname)
    try:
        _save_avatar(user_id)
    except Exception as e:
        logging.message('Error saving avatar <{}>'.format(user_id), e)


def have_avatar(user_id:int):
    filename = str(user_id) + '.jpg'
    fullname = os.path.join(config.paths.images.avatars, filename)
    return os.path.exists(fullname)


def delete_avatar(user_id:int):
    filename = str(user_id) + '.jpg'
    fullname = os.path.join(config.paths.images.avatars, filename)
    if os.path.exists(fullname):
        os.remove(fullname)
    fullname = os.path.join(config.paths.images.avatars, str(user_id) + '_sq.jpg')
    if os.path.exists(fullname):
        os.remove(fullname)
    fullname = os.path.join(config.paths.images.avatars, str(user_id) + '_sq_sm.jpg')
    if os.path.exists(fullname):
        os.remove(fullname)


def save_court_photo(court_id:int, bottlefile):
    filename = str(court_id) + '.jpg'
    fullname = os.path.join(config.paths.images.courts, filename)
    _save_image(fullname, bottlefile)


def save_report(game_id:int, bottlefile):
    filename = str(game_id) + '.jpg'
    fullname = os.path.join(config.paths.images.reports, filename)
    _save_image(fullname, bottlefile)