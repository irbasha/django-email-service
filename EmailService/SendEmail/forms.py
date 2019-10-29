from .models import Mails
from django import forms


class EmailForm(forms.ModelForm):
	emailto = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
	csv_file = forms.FileField(required=False)
	cc = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
	bcc = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
	subject = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
	message = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}))


	class Meta:
		model = Mails
		fields = ('emailto', 'cc', 'bcc', 'subject','message','csv_file',)
		# fields = ('emailto','subject','message',)

