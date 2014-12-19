import bottle
import dbutils
import pages
import base64

from models import users


@pages.get(['/blog'])
def get_blog(): # для всего блога
    return pages.PageBuilder('blog_main')


@pages.post('/blog/add')
@pages.only_organizers
def post_blog(): # добавление новости
    with dbutils.dbopen() as db:
        text = base64.b64encode(bottle.request.forms.get('text').encode()).decode()
        sql = 'INSERT INTO blog_posts (content) VALUES ({})'.format(text)
        db.execute(sql)
        article_id = db.execute('SELECT last_insert_id() FROM games')[0][0]
        raise bottle.redirect("/blog")
        # raise bottle.redirect("/blog/{}".format(article_id))


@pages.get('/blog/<article_id:int>')
def get_article(article_id:int): # просмотр отдельной новости
    return pages.PageBuilder('blog_article')


@pages.get('/blog/add')
@pages.only_organizers
def get_blog(): # для добавления статьи
    return pages.PageBuilder('addarticle')


@pages.get('/blog/moderate')
@pages.only_admins
def get_moderate(): # для модерации статей
    return pages.PageBuilder('blogmoderate')


@pages.get('/calc')
def get_calc(): # для калькулятора
    with dbutils.dbopen() as db:
        user_id = pages.auth.current().user_id()
        user = users.get(user_id, dbconnection=db)
        return pages.PageBuilder('calc', user=user)