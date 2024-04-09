from django import forms

from main.models import SendingMessage


class StyleForMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleForMixin, forms.ModelForm):
    class Meta:
        model = SendingMessage
        exclude = ('status', 'is_active',)


class MailingUpdate(forms.ModelForm):
    class Meta:
        model = SendingMessage
        exclude = ('status', 'is_active',)

