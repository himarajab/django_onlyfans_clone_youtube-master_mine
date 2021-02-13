from django import forms
from django.db.models import fields
from tier.models import Tier

class NewTierForm(forms.ModelForm):
  description = forms.CharField(widget=forms.TextInput(attrs={'class':'materialize-textarea'}),required=True)
  price = forms.CharField(required=True)
  can_message = forms.BooleanField(widget=forms.TextInput(attrs={'class':'materialize-textarea'}),required=False)

  class Meta:
    model= Tier
    fields = ('description','price','can_message')
