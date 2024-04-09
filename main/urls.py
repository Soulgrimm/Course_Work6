from django.urls import path
from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import SendingMessageListView, SendingMessageCreateView, SendingMessageUpdateView, \
    SendingMessageDeleteView, SendingMessageDetailView, ClientListView, ClientCreateView, ClientDetailView, \
    ClientUpdateView, ClientDeleteView, MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, \
    MessageDeleteView, MailingAttemptListView

app_name = MainConfig.name

urlpatterns = [
    path('', cache_page(60)(SendingMessageListView.as_view()), name='mailing'),
    path('create/', SendingMessageCreateView.as_view(), name='create'),
    path('view/<int:pk>/', SendingMessageDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', SendingMessageUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', SendingMessageDeleteView.as_view(), name='delete'),

    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/add', ClientCreateView.as_view(), name='add_client'),
    path('client/view/<int:pk>/', ClientDetailView.as_view(), name='view_client'),
    path('clients/edit/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/add', MessageCreateView.as_view(), name='add_message'),
    path('messages/view/<int:pk>/', MessageDetailView.as_view(), name='view_message'),
    path('messages/edit/<int:pk>/', MessageUpdateView.as_view(), name='update_message'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),

    path('attempts/', MailingAttemptListView.as_view(), name='attempts'),
]
