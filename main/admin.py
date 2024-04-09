from django.contrib import admin
from main.models import Client, SendingMessage, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email',)
    search_fields = ('is_active',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme', 'message',)
    search_fields = ('theme',)


@admin.register(SendingMessage)
class SendindMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_first_sending', 'periodicity', 'status',)
    list_filter = ('clients', 'status',)
    search_fields = ('status',)
