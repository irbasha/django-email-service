# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.http import Http404
from django.utils import timezone
from django.conf import settings
from .forms import EmailForm
import re


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def isValidAddress(address):
    result = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", address)
    return True if result else False

def send_email(request):
	if request.method == "POST":
		form = EmailForm(request.POST, request.FILES)
		if form.is_valid():
			email = request.POST.get('emailto')
			cc_email = request.POST.get('cc')
			bcc_email = request.POST.get('bcc')
			subject = request.POST.get('subject')
			message = request.POST.get('message')
			email_from = settings.EMAIL_HOST_USER

			csv_file = request.FILES.get('csv_file')
			if not csv_file.name.endswith('.csv'):
				print("Error file is not in csv format")
				recipient_list = [email]
			elif csv_file.multiple_chunks():
				print("Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000)))
				recipient_list = [email]
			else:
				recipient_list = [email]
				file_data = csv_file.read().decode('utf-8')
				lines = file_data.split("\n")
				for line in lines:
				    fields = line.strip().split(',')
				    recipient_list.extend(fields)
				recipient_list = list(set(recipient_list))
				recipient_list = list(filter(isValidAddress, recipient_list))
			print(recipient_list)

			email = EmailMessage(subject,message,email_from,recipient_list, bcc=[bcc_email], cc=[cc_email])
			email.send(fail_silently=False)
			return render(request, 'success.html')
		raise Http404
	else:
		form = EmailForm()
	return render(request, 'home.html', {'form': form})
