import bottle

import config
import pages
from models import mailing


class SendMail(pages.Page):
    def get(self, name):
        mailing.sendhtml(bottle.template(name), config.email.admin, subject='Мыльце')
        raise bottle.redirect(bottle.request.get_header('Referer', '/'))

    get.route = '/sendmail/<name>'
