from django.core.management import BaseCommand

from main.models import Message


class Command(BaseCommand):

    def handle(self, *args, **options):
        Message.objects.all().delete()

        message_list = [
            {'theme': 'Привет', 'message': 'Подписывайся'},
            {'theme': 'Заглядывай', 'message': 'У нас новые товары!'},
            {'theme': 'ОПОВЕЩЕНИЕ', 'message': 'Срочно скупаем все бананы!'}
        ]

        messages_for_create = []

        for message_item in message_list:
            messages_for_create.append(Message(**message_item))

        Message.objects.bulk_create(messages_for_create)
