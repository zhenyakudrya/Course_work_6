<h2 align="center">Курсовая работа Django</h2>

Веб-приложение сервиса управления рассылками, администрирования и получения статистики.


<!-- USAGE EXAMPLES -->
## Usage

Перед запуском web-приложения создайте базу данных, создайте и примените миграции, установите необходимые пакеты из файла requirements.txt и заполните файл .env по образцу env.sample. Используйте команду "python manage.py csu" для создания суперпользователя и "python manage.py manager" для создания группы с функционалом менеджера. Для запуска используйте команду "python manage.py runserver" либо через конфигурационные настройки PyCharm.

## Структура проекта

config/

    settings.py - настройки приложений
    urls.py - файл маршрутизации

blog/

    templates/blog - html шаблоны для приложения blog
    admin.py - настройки админки
    models.py - модели приложения
    urls.py - файл маршрутизации приложения
    views.py - контроллеры

mailing/

    management/commands
        runapscheduler - кастомная команда начала рассылки
    static - директория с файлами для стилистического оформления сайта
    templates/sheduler - html шаблоны для приложения newsletter
    admin.py - настройки админки
    forms.py - настройки форм
    models.py - модели приложения
    services.py - сервисные функции
    urls.py - файл маршрутизации приложения
    views.py - контроллеры

users/

    management/commands
        csu - кастомная команда создания суперпользователя
    template/users - html шаблоны для приложения users
    admin.py - настройки админки
    forms.py - настройки форм
    models.py - модели приложения
    urls.py - файл маршрутизации приложения
    views.py - контроллеры

manage.py - точка входа веб-приложения

requirements.txt - список зависимостей для проекта.





<p align="right">(<a href="#readme-top">back to top</a>)</p>