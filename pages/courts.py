import pages


class Courts(pages.Page):
    path = ['courts']

    def execute(self, method:str):
        if method == 'POST':
            data = self.post()
            if isinstance(data, pages.Template):
                return data.template()
            return data
        if method == 'GET':
            data = self.get()
            if isinstance(data, pages.Template):
                return data.template()
            return data

    def get(self):
        pass

    def post(self):
        pass
