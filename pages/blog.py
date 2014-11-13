import dbutils
import pages


class Blog(pages.Page):
    def get(self, **kwargs):
        return pages.PageBuilder('blog')

    def post(self):
        with dbutils.dbopen() as db:
            text = bottle.request.forms.get('text')
            sql = 'INSERT INTO blog_posts (text) VALUES ({text})'
            db.execute(sql)
            raise bottle.redirect("/blog")

    get.route = '/blog'
    post.route = '/blog'