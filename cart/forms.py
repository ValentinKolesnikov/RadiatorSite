from django import forms
from django.forms import TextInput


class OrderForm(forms.Form):
    name = forms.CharField(label="ФИО", max_length=300, required=True)
    phone_number = forms.CharField(label="Телефон", max_length=30, required=True)
    more_info = forms.CharField(label="Удобное время для звонка", max_length=300, required=True)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget = TextInput(attrs={
            'id': 'phone'})