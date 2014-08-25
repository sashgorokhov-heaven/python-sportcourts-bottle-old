import bottle

import pages


class Authorize(pages.Page):
    def get(self):
        if pages.auth_dispatcher.loggedin():
            raise bottle.redirect('/profile')
        return pages.PageBuilder('auth')

    def post(self):
        email = bottle.request.forms.email
        password = bottle.request.forms.password
        try:
            pages.auth_dispatcher.login(email, password)
        except ValueError:
            return pages.PageBuilder('auth', email=email, error='Ошибка авторизации',
                                     error_description='Неправильный email или пароль')
        return bottle.redirect('/profile')

    get.route = '/auth'
    post.route = get.route