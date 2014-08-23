import bottle

import pages
import modules.logging


class ServerLogs(pages.Page):
    path = ['logs']

    @pages.setlogin
    def get(self):
        if not pages.loggedin() or pages.getadminlevel() != 1:
            raise bottle.HTTPError(404)

        logs = list(filter(lambda x: x != '', map(lambda x: x.strip(), modules.logging.get_log().split('\n'))))
        parsed = list()

        for line in logs:
            if line.startswith('[INFO]') and 'Traceback' not in line:
                parsed.append(list())
                parsed[-1].append('info')
                parsed[-1].append('Info')
                parsed[-1].append(' '.join(line.split(' ')[1:]))
            elif line.startswith('[WARN]'):
                parsed.append(list())
                parsed[-1].append('warning')
                parsed[-1].append('Warning')
                parsed[-1].append(' '.join(line.split(' ')[1:]))
            elif line.startswith('[ERRO]'):
                parsed.append(list())
                parsed[-1].append('danger')
                parsed[-1].append('Error')
                parsed[-1].append(' '.join(line.split(' ')[1:]))
            elif 'Traceback' in line:
                parsed[-1].append(' '.join(line.split(' ')[3:]))
            elif not line.startswith('File'):
                parsed[-1].append(' ' * 4 + line)
            else:
                parsed[1].append(line)

        return pages.Template('logspage', logs=parsed)