import smtplib
import bottle
from models import autodb, settings, users
from modules import config, dbutils, extract_traceback
from email.mime import text
import modules.logging

def sendmail(message:str, to:str, subject:str='Уведомление'):
    try:
        me = config['email']['login']
        you = to
        message = str(message)
        subj = '{} | Sportcourts | Спортивные площадки'.format(subject)
        server = "smtp.gmail.com"
        port = 25
        user_name = config['email']['login']
        user_passwd = config['email']['password']
        msg = text.MIMEText(message, _charset="utf-8")
        msg['Subject'] = subj
        msg['From'] = me
        msg['To'] = you
        s = smtplib.SMTP(server, port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(user_name, user_passwd)
        s.sendmail(me, you, msg.as_string())
        s.quit()
    except Exception as e:
        try:
            print(e.__class__.__name__, e.args)
        except:
            pass
        return False
    return True


@autodb
def send_to_user(user_id:int, message:str, subject:str='Уведомление', override:bool=False,
                 dbconnection:dbutils.DBConnection=None) -> bool:
    sett = settings.get(user_id, dbconnection=dbconnection)
    if not override and not sett.send_email():
        return True
    email = users.get(user_id, fields=['email'], dbconnection=dbconnection)['email']
    return sendmail(message, email, subject)


def send_report(e:Exception):
    lines = ["На сайте возникла ошибка"]
    lines.append('')
    lines.append("Подробности запроса:")
    lines.append(modules.logging.access_log(False))
    lines.append("Referer: " + bottle.request.get_header("Referer", "None"))
    lines.append('')
    lines.append("Подробности об ошибке:")
    lines.append(e.__class__.__name__ + (': ' + ','.join(map(str, e.args)) if len(e.args) > 0 else ''))
    lines.append(extract_traceback(e))
    lines = '\n'.join(lines)
    sendmail(lines, config['admin_email'], "Ошибка")