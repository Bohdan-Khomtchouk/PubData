from django import forms
from .models import Search, ServerNames


class SearchForm(forms.ModelForm):

    class Meta:
        model = Search
        fields = ('word',)
        widgets = {'word': forms.Textarea(attrs={'rows': 1, 'cols': 2, 'size':4,
        		  								 'placeholder':"search for data",
        		  								 'class':'form-control'},),}


class SelectServer(forms.Form):
    servers = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(SelectServer, self).__init__(*args, **kwargs)
        self.fields['servers'].choices = [(x.name, x.path) for x in ServerNames.objects.all()]
        self.fields['servers'].widget.attrs['class'] = "dropdown show"