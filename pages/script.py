import config
import dbutils
from models import mailing, notifications
from modules import utils
import modules
import pages


@utils.spool('sp')
def sp():
    with dbutils.dbopen() as db:
        users = db.execute("SELECT * FROM users", dbutils.dbfields['users'])
        for user in users:
            try:
                print('[{}] {}'.format(user['user_id'], user['activated']), end=' ', flush=True)
                if user['activated']==1:
                    db.execute("INSERT INTO activation (email, activated, token, datetime) VALUES ('{}', 2, '{}', NOW())".format(user['email'], modules.generate_token()))
                elif user['activated']==0:
                    token = modules.generate_token()
                    email = user['email']
                    print(':', end='', flush=True)
                    mailing.sendhtml(
                        pages.PageBuilder('mail_activation', token=token).template(),
                        email,
                        'Чтобы подтвердить email, перейдите по ссылке http://{}/oldvactivation?token={}'.format(config.server, token),
                        'Подтверждение email')
                    print('+', end=' ', flush=True)
                    notifications.add(user['user_id'], 'Вам было отправлено повторное письмо для подтверждения вашего email', 1)
                    db.execute("INSERT INTO activation (email, activated, token, datetime) VALUES ('{}', 1, '{}', NOW())".format(email, token))
                print()
            except Exception as e:
                print()
                print(e.__class__.__name__, e.args)
                print()
                continue

@pages.get('/t')
def get():
    sp()
