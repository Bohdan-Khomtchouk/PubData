from django import forms
from .models import SearchQuery, ServerName


class SearchForm(forms.ModelForm):

    class Meta:
        model = SearchQuery
        fields = ('word',)
        widgets = {'word': forms.TextInput(attrs={'placeholder': "search for data",
        		  								  'class': 'form-control',},),}
        labels = {
        "word": ""
        }


class SelectServer(forms.Form):
    servers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                        choices=[],
                                        required=False)

    def __init__(self, *args, **kwargs):
        super(SelectServer, self).__init__(*args, **kwargs)
        self.fields['servers'].choices = [(x.path, x.name) for x in ServerName.objects.all()]
        self.fields['servers'].widget.attrs['class'] = "dropdown show"
