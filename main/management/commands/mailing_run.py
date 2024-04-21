from django.core.management import BaseCommand
from main.cron import send_mailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_mailing()
        print("Запуск рассылки")
