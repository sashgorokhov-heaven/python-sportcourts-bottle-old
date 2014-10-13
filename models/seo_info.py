import dbutils
from models import Cache, autodb
from objects import SeoInfo


class SeoCache(Cache):
    def cache(self, *args, **kwargs):
        tplname = args[0]
        if self.check(tplname):
            return self.get(tplname)
        else:
            retval = get(tplname, dbconnection=kwargs.get('dbconnection'))
            self.set(tplname, retval)
            return retval


_cache = SeoCache(3600)


@_cache
@autodb
def get(tplname:str, dbconnection:dbutils.DBConnection=None) -> SeoInfo:
    dbconnection.execute("SELECT * FROM seo_info WHERE tplname='{}'".format(tplname))
    if len(dbconnection.last()) == 0: return None
    return SeoInfo(dbconnection.last()[0])