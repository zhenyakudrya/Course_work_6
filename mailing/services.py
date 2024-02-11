from datetime import datetime, timedelta
import pytz
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from mailing.models import Mailing, Logs


def my_job():
    day = timedelta(days=1, hours=0, minutes=0)
    weak = timedelta(days=7, hours=0, minutes=0)
    month = timedelta(days=30, hours=0, minutes=0)

    mailings = Mailing.objects.all().filter(status='Создана') \
        .filter(is_active=True) \
        .filter(next_date__lte=datetime.now(pytz.timezone('Europe/Moscow'))) \
        .filter(end_date__gte=datetime.now(pytz.timezone('Europe/Moscow')))

    for mail in mailings:
        mail.status = 'Запущена'
        mail.save()
        emails_list = [client.email for client in mail.mail_to.all()]

        result = send_mail(
            subject=mail.message.title,
            message=mail.message.content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails_list,
            fail_silently=False,
        )

        if result == 1:
            status = 'Отправлено'
        else:
            status = 'Ошибка отправки'

        log = Logs(mail=mail, status=status)
        log.save()

        if mail.interval == 'ежедневно':
            mail.next_date = log.last_mailing_time + day
        elif mail.interval == 'еженедельно':
            mail.next_date = log.last_mailing_time + weak
        elif mail.interval == 'ежемесячно':
            mail.next_date = log.last_mailing_time + month

        if mail.next_date < mail.end_date:
            mail.status = 'Создана'
        else:
            mail.status = 'Завершена'
        mail.save()


def get_cache_for_mailings():
    if settings.CACHE_ENABLED:
        key = 'mailings_count'
        mailings_count = cache.get(key)
        if mailings_count is None:
            mailings_count = Mailing.objects.all().count()
            cache.set(key, mailings_count)
    else:
        mailings_count = Mailing.objects.all().count()
    return mailings_count


def get_cache_for_active_mailings():
    if settings.CACHE_ENABLED:
        key = 'active_mailings_count'
        active_mailings_count = cache.get(key)
        if active_mailings_count is None:
            active_mailings_count = Mailing.objects.filter(is_active=True).count()
            cache.set(key, active_mailings_count)
    else:
        active_mailings_count = Mailing.objects.filter(is_active=True).count()
    return active_mailings_count
