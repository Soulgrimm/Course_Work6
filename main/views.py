from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.http import Http404

from main.forms import MailingForm, MailingUpdate
from main.models import Client, SendingMessage, Message, MailingAttempt
from main.services import get_cache_client


class SendingMessageCreateView(LoginRequiredMixin, CreateView):
    model = SendingMessage
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['client'] = get_cache_client()
        return context_data

    def form_valid(self, form):
        if form.is_valid:
            self.object = form.save()
            self.object.is_author = self.request.user
            self.object.save()

        return super().form_valid(form)


class SendingMessageListView(ListView):
    model = SendingMessage


class SendingMessageDetailView(DetailView):
    model = SendingMessage


class SendingMessageUpdateView(LoginRequiredMixin, UpdateView):
    model = SendingMessage
    form_class = MailingUpdate
    success_url = reverse_lazy('main:mailing')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser:
            return self.object
        elif self.request.user != self.object.is_author:
            return Http404
        return self.object


class SendingMessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = SendingMessage
    permission_required = 'main.delete_mailing'
    success_url = reverse_lazy('main:mailing')


class ClientCreateView(CreateView):
    model = Client
    fields = ('email', 'full_name', 'comment')
    success_url = reverse_lazy('main:clients')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('email', 'full_name', 'comment')
    success_url = reverse_lazy('main:clients')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('main:clients')


class MessageCreateView(CreateView):
    model = Message
    fields = ('theme', 'message')
    success_url = reverse_lazy('main:messages')


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('theme', 'message')
    success_url = reverse_lazy('main:messages')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('main:messages')


class MailingAttemptListView(ListView):
    model = MailingAttempt
