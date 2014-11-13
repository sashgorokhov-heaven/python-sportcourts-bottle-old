import bottle

import dbutils
import pages

import base64

class Blog(pages.Page):
    def get(self, **kwargs):
        return pages.PageBuilder('blog')

    def post(self):
        with dbutils.dbopen() as db:
            text = base64.b64encode(bottle.request.forms.get('text'))
            sql = 'INSERT INTO blog_posts (content) VALUES ({contentval})'
            sql = sql.format(
                contentval=text)
            db.execute(sql)
            raise bottle.redirect("/blog")

    get.route = '/blog'
    post.route = '/blog'