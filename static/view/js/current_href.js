$(function () {                                      // Когда страница загрузится
    $('li a').each(function () {             // получаем все нужные нам ссылки
        var location = window.location.href; // получаем адрес страницы
        var link = this.href;                // получаем адрес ссылки
        if ($(this).hasClass('topmenu') == true) {
            if (location == link) {               // при совпадении адреса ссылки и адреса окна
                $(this).parent().addClass('active');
                $(this).parent().parent().parent().addClass('active');  //добавляем класс
            }
        }
    });
});