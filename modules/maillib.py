import smtplib
import email.mime.text

import modules
import modules.logging


def send(message:str, to:str):
    try:
        me = modules.config['email']['login']
        you = to
        text = str(message)
        subj = 'Уведомление | Sportcourts | Спортивные площадки'
        server = "smtp.gmail.com"
        port = 25
        user_name = modules.config['email']['login']
        user_passwd = modules.config['email']['password']
        msg = email.mime.text.MIMEText(text, _charset="utf-8")
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
        modules.logging.error(e.__class__.__name__ + ': {}', e.args[0] if len(e.args) > 0 else '')
        modules.logging.info(modules.extract_traceback(e))
        return False
    return True
