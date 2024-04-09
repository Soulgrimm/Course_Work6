from main.models import Client
from django.core.cache import cache
from django.conf import settings


def get_cache_client():
    if settings.CACHE_ENABLE:
        key = f'client_list'
        client_list = cache.get(key)
        print('Список клиентов')
        if client_list is None:
            client_list = Client.objects.all()
            cache.set(key, client_list)
            print('Загружены данные в кеш')
    else:
        client_list = Client.objects.all()

    return client_list
