import datetime

from django import forms
from django.forms import ModelForm
from django.utils import timezone

from django.contrib.auth.models import User

from .models import Diary, Entry

class AddEntryForm(forms.Form):
    user = forms.CharField(widget=forms.HiddenInput())
    diary = forms.ModelChoiceField(queryset=None)
    date = forms.DateTimeField(initial=timezone.now)
    title = forms.CharField(max_length=200)
    text = forms.CharField(widget=forms.Textarea)
    feelings = forms.CharField(max_length=200, label="Feelings, separate with commas)")
    energy = forms.IntegerField(label="Energy (0 to 100%)")
    mood = forms.IntegerField(label="Mood (-100 to 100%")
    
    def __init__(self, user, *args, **kwargs):
        super(AddEntryForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['user'].initial = user.id
        self.fields['diary'].queryset = Diary.objects.filter(user=user)
		
