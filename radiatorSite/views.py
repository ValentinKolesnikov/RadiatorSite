from django.shortcuts import render


def custom404(request, exception):
    return render(request, 'mainApp/404.html', {'ex_title': "Ошибка 404 – указанная страница не найдена",
                                                'ex_text': 'К сожалению, запрашиваемой Вами страницы не существует на сайте.'})

def custom500(request):
    return render(request, 'mainApp/500.html', {'ex_title': "Ошибка 500 - Сервис не доступен",
                                                'ex_text': 'На сервере произошла непредвиденная ошибка. Пожалуйста, подождите, она вскоре будет исправлена. Попробуйте вернуться на главную станицу.'})