from django import forms
from .models import Poll, Choice


class PollForm(forms.ModelForm):
  class Meta:
    model = Poll
    fields = ('question', 'creator', 'description')

class ChoiceForm(forms.ModelForm):
  class Meta:
    model = Choice
    fields = ('poll', 'option')
  poll = forms.ModelChoiceField(Poll.objects.all())

class ManyOptionsForm(forms.Form):
  number = forms.IntegerField(min_value=2, max_value=10)