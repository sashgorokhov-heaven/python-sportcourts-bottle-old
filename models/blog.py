import base64
import dbutils
from models import autodb
from objects import Tag, BlogPost


_connection = dbutils.default_connection.copy()
_connection['db'] = 'blog'
_fields = dbutils.setdbfields(**_connection)


@autodb
def get_tags(post_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT * FROM blog.tags WHERE tag_id IN (SELECT tag_id FROM blog.post_tags WHERE post_id={})".format(post_id), _fields['tags'])
    if len(dbconnection.last())==0: return list()
    return list(map(lambda x: Tag(x), dbconnection.last()))


@autodb
def get_posts_by_tag(tag_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT * FROM blog.posts WHERE post_id IN (SELECT post_id FROM blog.post_tags WHERE tag_id={}) AND status>=0".format(tag_id), _fields['posts'])
    if len(dbconnection.last())==0: return list()
    return list(map(lambda x: Tag(x), dbconnection.last()))


@autodb
def get_posts_by_tags(tag_ids:list, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT * FROM blog.posts WHERE post_id IN (SELECT post_id FROM blog.post_tags WHERE tag_id IN ({})) AND status>=0".format(', '.join(tag_ids)), _fields['posts'])
    if len(dbconnection.last())==0: return list()
    return list(map(lambda x: Tag(x), dbconnection.last()))


@autodb
def get_posts(dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT * FROM blog.posts WHERE status>=0", _fields['posts'])
    if len(dbconnection.last())==0: return list()
    return list(map(lambda x: BlogPost(x, dbconnection=dbconnection), dbconnection.last()))


@autodb
def get_post(post_id:int, dbconnection:dbutils.DBConnection=None) -> BlogPost:
    dbconnection.execute("SELECT * FROM blog.posts WHERE post_id={}".format(post_id), _fields['posts'])
    if len(dbconnection.last())==0: return None
    return BlogPost(dbconnection.last()[0], dbconnection=dbconnection)


@autodb
def get_tag(tag_id:int, dbconnection:dbutils.DBConnection=None) -> BlogPost:
    dbconnection.execute("SELECT * FROM blog.tags WHERE tag_id={}".format(tag_id), _fields['posts'])
    if len(dbconnection.last())==0: return None
    return Tag(dbconnection.last()[0])


@autodb
def get_all_tags(dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT * FROM blog.tags")
    return list(map(lambda x: Tag(x), dbconnection.last()))


@autodb
def add_post(keywords:str, description:str, title:str, content:str, created_by:int, datetime:str, tags:list, dbconnection:dbutils.DBConnection=None) -> int:
    content = base64.b64encode(content.encode()).decode()
    dbconnection.execute("INSERT INTO blog.posts (keywords, description, title, content, created_by, datetime) VALUES ('{}', '{}', '{}', '{}', {}, '{}')".format(
        keywords, description, title, content, created_by, datetime))
    post_id = dbconnection.execute("SELECT last_insert_id() FROM blog.posts")[0][0]
    for tag_id in tags:
        dbconnection.execute("INSERT INTO blog.post_tags VALUES ({}, {})".format(post_id, tag_id))
    return post_id