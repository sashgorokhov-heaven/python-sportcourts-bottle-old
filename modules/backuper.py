import os
import config

from modules.myuwsgi import uwsgidecorators


# TODO: rework!
if not config.standalone and not os.path.exists(config.paths.dumps.root):
    raise FileNotFoundError('{} not found'.format(config.paths.dumps.root))


started = True


@uwsgidecorators.cron(0, 0, -1, -1, -1)
def backup(*args, **kwargs):
    global started
    if not started:
        if os.path.exists('/bsp/dumps/sportcourts_dump.sql'):
            os.remove('/bsp/dumps/sportcourts_dump.sql')
        if os.path.exists('/bsp/dumps/logsdb_dump.sql'):
            os.remove('/bsp/dumps/logsdb_dump.sql')
        if os.path.exists('/bsp/dumps/data_dump.tar'):
            os.remove('/bsp/dumps/data_dump.tar')
        os.system("mysqldump sportcourts > /bsp/dumps/sportcourts_dump.sql")
        os.system("mysqldump logsdb > /bsp/dumps/logsdb_dump.sql")
        os.system("tar -cvf /bsp/dumps/data_dump.tar /bsp/data > /dev/null")
    else:
        started = False