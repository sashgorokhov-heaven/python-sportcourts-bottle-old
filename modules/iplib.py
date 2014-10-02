_ipbase = 'ipbase.json'


def skip(ip:str, fullpath:str):
    if fullpath.startswith('/view') or fullpath.startswith('/images'):
        return True
    return True
