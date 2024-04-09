from django.db import models
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Почта')
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.TextField(max_length=200, verbose_name='Комментарий', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    is_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь',
                                  **NULLABLE)

    def __str__(self):
        return f'{self.full_name}, {self.email}'

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        permissions = [(
            'set_active',
            'Can active client',
        )]


class Message(models.Model):
    theme = models.CharField(max_length=100, verbose_name='Тема письма')
    message = models.TextField(max_length=500, verbose_name='Тело письма')

    is_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class SendingMessage(models.Model):
    DAYLY = "Раз в день"
    WEEKLY = "Раз в неделю"
    MONTHLY = "Раз в месяц"

    PERIODICITY_MAILING = [
        (DAYLY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]

    CREATED = 'Создана'
    STARTED = 'Запущена'
    FINISHED = 'Завершена'

    STATUS_CHOICES = [
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
        (FINISHED, "Завершена"),
    ]

    time_first_sending = models.DateTimeField(verbose_name='Время первой отправки')
    periodicity = models.CharField(max_length=100, choices=PERIODICITY_MAILING, verbose_name='Периодичность отправки')
    status = models.CharField(default=CREATED, choices=STATUS_CHOICES, max_length=50, verbose_name='Статус рассылки')
    is_active = models.BooleanField(default=True)
    clients = models.ManyToManyField(Client, verbose_name='Клиенты для рассылки')
    message_to = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, verbose_name='Сообщение')

    is_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return f'{self.time_first_sending}, {self.periodicity}, {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [(
            'set_active',
            'Can active'),
        ]


class MailingAttempt(models.Model):
    last_attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    attempt_status = models.BooleanField(verbose_name='Cтатус попытки')
    server_response = models.CharField(verbose_name='Ответ почтового сервера', **NULLABLE)
    sending_list = models.ForeignKey(SendingMessage, on_delete=models.CASCADE, verbose_name='Отправка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент рассылки', **NULLABLE)

    def __str__(self):
        return f'{self.last_attempt_time}, {self.attempt_status}'

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
