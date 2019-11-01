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
from smtplib import SMTPException
import re
import logging
logger = logging.getLogger(__name__)


class SignUp(generic.CreateView):
	"""Class view for signup template"""
	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'

def isValidAddress(address):
	"""function to check if the string is a valid email id format"""
	result = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", address)
	return True if result else False

def send_email(request):
	"""view function which validates form data and sends email to recipients, returns 404 otherwise"""
	if request.method == "POST":
		logger.info("processing email request")
		form = EmailForm(request.POST, request.FILES)
		if form.is_valid():
			from_email = settings.EMAIL_HOST_USER
			recipients = request.POST.get('emailto')
			cc_list = request.POST.get('cc')
			bcc_list = request.POST.get('bcc')
			subject = request.POST.get('subject')
			message = request.POST.get('message')
			csv_file = request.FILES.get('csv_file')

			if csv_file and csv_file.name.endswith('.csv'):
				if csv_file.multiple_chunks():
					logger.warning("uploaded csv file is too big (%.2f MB)." % (csv_file.size/(1000*1000)))
					if not recipients:
						logger.error('recipients list is empty. returning 404')
						raise Http404
					logger.info('email will be sent to ' + str(recipients))
					recipient_list = [recipients]
				else:
					logger.info('CSV file found. reading...')
					recipient_list = [recipients]
					logger.info(recipient_list)
					file_data = csv_file.read().decode('utf-8')
					lines = file_data.split("\n")
					for line in lines:
						fields = line.strip().split(',')
						recipient_list.extend(fields)
					recipient_list = list(set(recipient_list))
					recipient_list = list(filter(isValidAddress, recipient_list))
					logger.info('email will be sent to ' + str(recipients_list))
			else:
				logger.warning('CSV file not found or file is not a csv format.')
				if not recipients:
					logger.error('recipients list is empty. returning 404')
					raise Http404
				logger.info('email will be sent to ' + str(recipients))
				recipient_list = [recipients]

			try:
				email = EmailMessage(subject,message,email_from,recipient_list, bcc=[bcc_email], cc=[cc_email])
				email.send(fail_silently=False)
			except SMTPException as err:
				logger.error('error sending email' + str(err))
				raise Http404

			return render(request, 'success.html')
		logger.error('form validation failed. returning 404')
		raise Http404
	else:
		form = EmailForm()
		logger.info('rendering email form')
	return render(request, 'home.html', {'form': form})
