import re

lineregexp = re.compile(r"\[(?P<date>.+?)\s(?P<time>.+?)\]\s(?P<ip>.+?)\s\"(?P<path>.+?)\"(\suid=\[(?P<uid>\d+?)\])?")

data = dict()

with open("logs/access.txt") as f:
    for line in f:
        match = re.match(lineregexp, line)
        if not match:
            print("-", line)
        ip = match.group('ip')
        path = match.group('path')
        uid = None if 'uid' not in match.groupdict() else match.groupdict()['uid']
        if ip in data:
            data[ip]['visits'] += 1
            if path in data[ip]['paths']:
                data[ip]['paths'][path] += 1
            else:
                data[ip]['paths'][path] = 1
            if uid:
                data[ip]['uid'].add(uid)
        else:
            data[ip] = dict()
            data[ip]['paths'] = dict()
            data[ip]['paths'][path] = 1
            data[ip]['visits'] = 1
            data[ip]['uid'] = set()
            if uid:
                data[ip]['uid'].add(uid)

for n, ip in enumerate(sorted(data, key=lambda x: data[x]['visits'], reverse=True), 1):
    print(n,
          "\t",
          ip + " " * (15 - len(ip)),
          "\t",
          data[ip]['visits'],
          "\t",
          ','.join(data[ip]['uid']) if len(data[ip]['uid']) > 0 else '')  # ,
    # sorted(data[ip]['paths'], key= lambda x:data[ip]['paths'][x], reverse=True)[0])