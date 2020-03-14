from django import forms
from .StraightAndrewAssignment10models import Stock


class StockForm(forms.ModelForm):
    """Class to initialize form model to hold stock data."""
    class Meta:
        model = Stock
        fields = ["ticker"]