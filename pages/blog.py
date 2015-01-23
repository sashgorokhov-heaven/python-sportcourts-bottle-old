import bottle
import dbutils
import pages
import base64

from models import users, blog
from objects import SeoInfo

@pages.get('/blog')
def get_blog():
    with dbutils.dbopen() as db:
        posts = blog.get_posts()
        tags = blog.get_all_tags()
        tags_posts = list()
        for tag in tags:
            tags_posts.append((tag, len(blog.get_posts_by_tag(tag.tag_id(), dbconnection=db))))
        tags_posts = sorted(tags_posts, reverse=True, key= lambda x: x[1])[:11] # первые десять
        return pages.PageBuilder('blog_main', posts=posts, alltags=tags_posts)


@pages.get('/blog/tag/<tag_id:int>')
def get_tag(tag_id:int):
    tag = blog.get_tag(tag_id)
    if not tag: raise bottle.HTTPError(404)
    posts = blog.get_posts_by_tag(tag_id=tag_id)
    seo_info = SeoInfo({'tplname':'blog_post', 'keywords':tag.keywords(), 'description':tag.description()})
    return '# TODO страница с отображением списка постов по тэгу'


@pages.get('/blog/<post_id:int>')
def get_article(post_id:int):
    with dbutils.dbopen() as db:
        post = blog.get_post(post_id, dbconnection=db)
        if not post: raise bottle.HTTPError(404)
        tags = blog.get_all_tags(dbconnection=db)
        tags_posts = list()
        for tag in tags:
            tags_posts.append((tag, len(blog.get_posts_by_tag(tag.tag_id(), dbconnection=db))))
        tags_posts = sorted(tags_posts, reverse=True, key= lambda x: x[1])[:11] # первые десять
        seo_info = SeoInfo({'tplname':'blog_post', 'keywords':post.keywords(), 'description':post.description()})
        return pages.PageBuilder('blog_post', post=post, alltags=tags_posts, seo_info=seo_info)


@pages.get('/blog/add')
@pages.only_writers
def get_add_blog():
    tags = blog.get_all_tags()
    return pages.PageBuilder('add_post', tags=tags)


@pages.post('/blog/add')
@pages.only_ajax
@pages.only_writers
def post_add_blog():
    forms = lambda x: bottle.request.forms.get(x)
    tags = list()
    if 'tags' in bottle.request.forms:
        tags = bottle.request.forms.getall('tags')
    post_id = blog.add_post(forms('title'), forms('text'), pages.auth.current().user_id(), tags)
    raise bottle.redirect('/blog/{}'.format(post_id))


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