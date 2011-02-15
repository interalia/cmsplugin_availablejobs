from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_detail
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404 
from django.contrib import messages
from models import EnableOpening, Opening, Candidate
from forms import ApplyForm
import datetime
import hashlib

def index(request):
    eopen = EnableOpening.objects.all()
    d = {"opens": eopen}
    return direct_to_template(request,
            template="vacancy/index.html",
            extra_context = d,
            )

def detail(request, id):
    qs = EnableOpening.objects.all()
    d = {"queryset": qs, 'object_id': int(id), 'template_name': "vacancy/opening_detail.html" }
    return object_detail(request,**d)

def _process_cv(request, opening):
    applyform = ApplyForm()
    if request.method == "POST":
        applyform = ApplyForm(data = request.POST, files = request.FILES)
        if applyform.is_valid():
            can = applyform.get_candidate(opening)
            if can:
                d = {'candidate': can, 'open': opening}
                return direct_to_template(request, template="vacancy/job_submit_success.html")
            else:
                messages.error(request, "Tu email/Nombre ya han sido ingreados")
    d = {"open": opening , "form": applyform}
    return direct_to_template(request, template = "vacancy/job_form.html", extra_context = d)


def show_form(request, id):
    opening = get_object_or_404(EnableOpening, id = id)
    return _process_cv(request, opening)

def send_cv(request):
    opening = None
    return _process_cv(request,opening)

def facebook(request):
    ops = EnableOpening.objects.all()
    today = hashlib.md5(str(datetime.datetime.now()))
    SITE = Site.objects.get_current()
    d = {"enable_openings": ops, "today": today.hexdigest(), 'SITE': SITE}
    return direct_to_template(request, "vacancy/facebook.html", extra_context = d)
