from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
import settings

def enviar_email(sender, **kwargs):
    instance = kwargs.get("instance")
    s ="http://" + Site.objects.get_current().domain + reverse("admin:index")
    subject = "Se ha agregado un candidato nuevo"
    messages = "el candidato %s\n %s" % ( instance.name,s )
    send_mail(subject, messages, settings.FROM_EMAIL, settings.TO_EMAIL)

