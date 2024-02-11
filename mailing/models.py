from django.db import models
from django.conf import settings
from django.utils import timezone

import users.models

NULLABLE = {'null': True, 'blank': True}

CHOICES = (
        ('CREATED', 'Создана'),
        ('LAUNCHED', 'Запущена'),
        ('COMPLETED', 'Завершена'),
    )

PERIOD_CHOICES = (
    ('once_per_day', 'ежедневно'),
    ('once_per_week', 'еженедельно'),
    ('once_per_month', 'ежемесячно'),
)


class Client(models.Model):
    fio = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.EmailField(verbose_name='почта')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    user = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='пользователь')

    def __str__(self):
        return f'{self.email} ({self.fio})'

    def __repr__(self):
        return f'{self.email} ({self.fio})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    title = models.CharField(max_length=250, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    user = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='Владелец сообщения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    name = models.CharField(verbose_name="название рассылки", max_length=50)
    client = models.ManyToManyField(Client, verbose_name="кому")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="сообщение", **NULLABLE)
    start_date = models.DateTimeField(default=timezone.now, verbose_name="начало рассылки")
    next_date = models.DateTimeField(default=timezone.now, verbose_name="следующая рассылка")
    end_date = models.DateTimeField(default=timezone.now, verbose_name="конец рассылки")
    period = models.CharField(default="разовая", max_length=50, verbose_name="период", choices=PERIOD_CHOICES)
    status = models.CharField(max_length=50, choices=CHOICES, verbose_name="статус")
    is_active = models.BooleanField(default=True, verbose_name="действующая")
    user = models.ForeignKey(users.models.User, on_delete=models.CASCADE, verbose_name="владелец рассылки")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('start_date',)
        permissions = [
            ('set_is_activated', 'Может отключать рассылку')
        ]


class Logs(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка', **NULLABLE)
    last_mailing_time = models.DateTimeField(auto_now=True, verbose_name='время последней рассылки')
    status = models.CharField(max_length=50, verbose_name='статус попытки', null=True)
    response = models.CharField(max_length=200, verbose_name="ответ почтового сервера", **NULLABLE)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.last_mail_time = None

    def __str__(self):
        return f'Отправлено: {self.last_mailing_time}, ' \
               f'Статус: {self.status}'

    class Meta:
        verbose_name = 'log'
        verbose_name_plural = 'logs'

