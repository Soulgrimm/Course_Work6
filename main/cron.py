from django.conf import settings

from django.core.mail import send_mail
from config import settings
from django.utils import timezone
from smtplib import SMTPException

from main.models import SendingMessage, MailingAttempt


def send_mailling(mailing):
    print(mailing)
    current_time = timezone.localtime(timezone.now())
    print(mailing.time_first_sending)
    print(current_time)
    print(mailing.time_first_sending <= current_time)
    if mailing.time_first_sending <= current_time:
        mailing.status = SendingMessage.STARTED
        mailing.save()
        for client in mailing.clients.all():
            try:
                result = send_mail(
                    subject=mailing.message_to.theme,
                    message=mailing.message_to.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False
                )
                attempt = MailingAttempt.objects.create(
                    last_attempt_time=mailing.time_first_sending,
                    attempt_status=result,
                    server_response='Успешно',
                    sending_list=mailing,
                    client=client
                )
                attempt.save()
                return attempt

            except SMTPException as error:
                attempt = MailingAttempt.objects.create(
                    last_attempt_time=mailing.time_first_sending,
                    attempt_status=False,
                    server_response=error,
                    sending_list=mailing,
                    client=client
                )
                attempt.save()
            return attempt
    else:
        mailing.status = SendingMessage.FINISHED
        mailing.save()


def daily_mailings():
    mailings = SendingMessage.objects.filter(periodicity="Раз в день")
    if mailings.exists():
        for mailing in mailings:
            send_mailling(mailing)


def weekly_mailings():
    mailings = SendingMessage.objects.filter(periodicity="Раз в неделю")
    if mailings.exists():
        for mailing in mailings:
            send_mailling(mailing)


def monthly_mailings():
    mailings = SendingMessage.objects.filter(periodicity="Раз в месяц")
    if mailings.exists():
        for mailing in mailings:
            send_mailling(mailing)
