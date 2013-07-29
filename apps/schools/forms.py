from django import forms
from .models import YearlyData


class SearchForm(forms.ModelForm):
    class Meta:
        model = YearlyData
        fields =("management", )