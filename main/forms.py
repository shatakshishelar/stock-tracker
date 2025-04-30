from django import forms
from .models import Purchase, CurrentPrice

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['stock', 'quantity', 'buy_price', 'purchase_date']

class CurrentPriceForm(forms.ModelForm):
    class Meta:
        model = CurrentPrice
        fields = ['stock', 'current_price']
