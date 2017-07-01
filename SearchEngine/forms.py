from django import forms
from .models import Search, ServerNames


class SearchForm(forms.ModelForm):

    class Meta:
        model = Search
        fields = ('word',)


class SelectServer(forms.Form):
    servers = forms.ChoiceField(choices = [])

    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['servers'].choices = [(x.name, x.path) for x in ServerNames.objects.all()]