from django.conf import settings

from django.core.mail import send_mail
from datetime import timedelta
from config import settings
from django.utils import timezone
from smtplib import SMTPException

from main.models import SendingMessage, MailingAttempt


def send_mailing():
    current_time = timezone.localtime(timezone.now())

    sends = SendingMessage.objects.all()
    for send in sends:
        if send.status == 'Создана':
            send.time_next_sending = send.time_first_sending
            send.save()
        else:
            continue

    mailing_list = SendingMessage.objects.filter(time_next_sending__lte=current_time)
    for mailing in mailing_list:
        for client in mailing.clients.all():
            try:
                result = send_mail(
                    subject=mailing.message_to.theme,
                    message=mailing.message_to.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                attempt = MailingAttempt.objects.create(
                    last_attempt_time=mailing.time_next_sending,
                    attempt_status=result,
                    server_response='Успешно',
                    sending_list=mailing,
                    client=client
                )
                attempt.save()
                if mailing.periodicity == 'Раз в день':
                    mailing.time_next_sending = mailing.time_next_sending + timedelta(days=1)
                    mailing.status = 'Запущена'
                elif mailing.periodicity == 'Раз в неделю':
                    mailing.time_next_sending = mailing.time_next_sending + timedelta(days=7)
                    mailing.status = 'Запущена'
                elif mailing.periodicity == 'Раз в месяц':
                    mailing.time_next_sending = mailing.time_next_sending + timedelta(days=30)
                    mailing.status = 'Запущена'
                mailing.save()
                return attempt

            except SMTPException as error:
                attempt = MailingAttempt.objects.create(
                    last_attempt_time=mailing.time_next_sending,
                    attempt_status=False,
                    server_response=error,
                    sending_list=mailing,
                    client=client,
                )
                attempt.save()
                return attempt
