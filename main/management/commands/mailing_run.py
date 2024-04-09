from django.core.management import BaseCommand
from main.cron import daily_mailings


class Command(BaseCommand):
    def handle(self, *args, **options):
        daily_mailings()
        print("Запуск рассылки")
