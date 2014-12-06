import dbutils
from models import autodb
from objects import SeoInfo
import cacher


@cacher.create('seo_info', 600, cacher.KeyCache)
def get(tplname:str, *args) -> SeoInfo:
    with dbutils.dbopen() as db:
        db.execute("SELECT * FROM seo_info WHERE tplname='{}'".format(tplname), dbutils.dbfields['seo_info'])
        if len(db.last()) == 0: return None
        return SeoInfo(db.last()[0])