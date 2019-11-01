from django.db import models


class Mails(models.Model):
    emailto = models.CharField(max_length=1000)
    csv_file = models.FileField(blank=True, null=True, max_length=1000)
    cc = models.CharField(max_length=1000)
    bcc = models.CharField(max_length=1000)
    subject = models.CharField(max_length=1000)
    message = models.CharField(max_length=20000)


    def __str__(self):
        return self.emailto
