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
import csv


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def validate_recipients_list(email, csv_file):
    rlist = [email]
    print(csv_file)
    file_data = csv_file.read().decode("utf-8")
    print(file_data)
    # filedata = open(csv_file)
    # data = csv.reader(filedata)
    # for row in data:
    #     rlist.extend(row)
    return (list(set(rlist)))


def send_email(request):
	if request.method == "POST":
		form = EmailForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.published_date = timezone.now()
			post.save()
			email = request.POST.get('emailto')
			cc_email = request.POST.get('cc')
			bcc_email = request.POST.get('bcc')
			subject = request.POST.get('subject')
			message = request.POST.get('message')
			csv_file = request.FILES.get('csv_file')
			email_from = settings.EMAIL_HOST_USER
			if not csv_file or not csv_file.name.endswith('.csv'):
				print(email)
				recipient_list = [x.strip() for x in email.split(',')]
			else:
				recipient_list = validate_recipients_list(email,csv_file)
			print(recipient_list)
			email = EmailMessage(subject,message,email_from,recipient_list, bcc=[bcc_email], cc=[cc_email])
			email.send(fail_silently=False)
			return render(request, 'success.html')
		raise Http404
	else:
		form = EmailForm()
	return render(request, 'home.html', {'form': form})
