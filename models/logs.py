import dbutils
import datetime


class Logs:
    def __init__(self, db:dbutils.DBConnection):
        self._db = db

        self.logs = db.execute("SELECT * FROM logsdb.access WHERE MONTH(datetime)=MONTH(NOW()) AND YEAR(datetime)=YEAR(NOW()) ORDER BY datetime DESC", dbutils.setdbfields(dbutils.logsdb_connection)['access'])
        self.logs_dict = dict()
        self.dates = set()
        self.logs_by_date = dict()
        self.ips = set()
        self.logs_by_ip = dict()
        self.paths = set()
        self.logs_by_paths = dict()
        self.users = set()
        self.logs_by_users = dict()
        self.users_by_ips = dict()
        self.ips_by_users = dict()
        for log in self.logs:
            self.logs_dict[log['id']] = log

            if log['datetime']:
                date = str(log['datetime'].date())
            else:
                date = '00.00.00'
            if date not in self.dates:
                self.dates.add(date)

            if date not in self.logs_by_date:
                self.logs_by_date[date] = [log['id']]
            else:
                self.logs_by_date[date].append(log['id'])

            if log['ip'] not in self.ips:
                self.ips.add(log['ip'])

            if log['ip'] not in self.logs_by_ip:
                self.logs_by_ip[log['ip']] = [log['id']]
            else:
                self.logs_by_ip[log['ip']].append(log['id'])

            path = log['path'].split('?')[0]
            if path not in self.paths:
                self.paths.add(path)
            if path not in self.logs_by_ip:
                self.logs_by_paths[path] = [log['id']]
            else:
                self.logs_by_paths[path].append(log['id'])
            if log['user_id']!=0:
                if log['user_id'] not in self.users:
                    self.users.add(log['user_id'])
                if log['user_id'] not in self.logs_by_ip:
                    self.logs_by_users[log['user_id']] = [log['id']]
                else:
                    self.logs_by_users[log['user_id']].append(log['id'])

                if log['user_id'] not in self.ips_by_users:
                   self.ips_by_users[log['user_id']] = {log['ip']}
                else:
                   self.ips_by_users[log['user_id']].add(log['ip'])

                if log['ip'] not in self.users_by_ips:
                   self.users_by_ips[log['ip']] = {log['user_id']}
                else:
                   self.users_by_ips[log['ip']].add(log['user_id'])

            today = datetime.date.today()
            dates = [str(today + datetime.timedelta(days=i)) for i in range(0 - today.weekday(), 7 - today.weekday())]
            self.this_week = [self.logs_by_date[date] for date in dates if date in self.logs_by_date]
            self.today = self.logs_by_date[str(today)]

    def dict(self) -> dict:
        return {i:self.__dict__[i] for i in self.__dict__ if not i.startswith('_')}