import bottle

import dbutils
import pages

import base64

class Blog(pages.Page):
    def get(self, **kwargs):
        if not pages.auth.current().userlevel.admin():
            raise bottle.HTTPError(404)
        return pages.PageBuilder('blog')

    def post(self):
        if not pages.auth.current().userlevel.admin():
            raise bottle.HTTPError(404)
        with dbutils.dbopen() as db:
            text = base64.b64encode(bottle.request.forms.get('text').encode()).decode()
            sql = 'INSERT INTO blog_posts (content) VALUES ({})'.format(text)
            db.execute(sql)
            raise bottle.redirect("/blog")

    get.route = '/blog'
    post.route = '/blog'