from .models import Mails
from django import forms


class EmailForm(forms.ModelForm):
	emailto = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
	csv_file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': "form-control-file"}))
	cc = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
	bcc = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
	subject = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
	message = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': "form-control"}))

	class Meta:
		model = Mails
		fields = ('emailto', 'csv_file', 'cc', 'bcc', 'subject','message',)
