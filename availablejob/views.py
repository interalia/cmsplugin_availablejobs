from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_detail
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404 
from django.contrib import messages
from models import EnableOpening, Opening, Candidate
from forms import ApplyForm
import datetime
import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings



def __create_candidate(form,op,file):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        phone = form.cleaned_data["phone"]
        cv = form.cleaned_data["cv"]
        uploaded_file(file)
        candidate, created = Candidate.objects.get_or_create(name = name, email = email)
        if op:
            candidate.opening = op
        candidate.phone = phone
        candidate.cv = cv
        candidate.save()
        return candidate


def index(request):
    eopen = EnableOpening.objects.all()
    for i in eopen:
        print i
    form = ApplyForm()
    post=False
    ios=mobile(request)
    d = {"opens": eopen,'form': form,'post':post,'mobile':ios}
    if request.method == "POST":      
        form= ApplyForm(request.POST,request.FILES)
        if form.is_valid():   
            post=True   
            d.update({"form":form,"post":post})   
            name = form.cleaned_data.get("opening")      
            opening = EnableOpening.objects.filter(opening__title = name)
            '''         
            for i in opening:
                __create_candidate(form,i,request.FILES['cv'])
            '''
        else:
	    d.update({"form":form,"post":post})
    return direct_to_template(request, template="vacancy/index.html",extra_context=d)


def detail(request, id):
    qs = EnableOpening.objects.all()
    d = {"queryset": qs, 'object_id': int(id), 'template_name': "vacancy/opening_detail.html" }
    return object_detail(request,**d)

def _process_cv(request,opening):
    applyform = ApplyForm()
    if request.method == "POST":
        form= ApplyForm(request.POST)
        if form.is_valid():
            vacante=form.save(commit=False)  
            vacante.save()
            return direct_to_template(request, template = "vacancy/job_submit_success.html")
    else:
        return direct_to_template(request, template = "vacancy/job_form.html")


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


def mobile(request):
    device = {}
    mobile=False
    ua=request.META.get('HTTP_USER_AGENT','').lower()
    if ua.find("iphone") > 0:
        mobile= True
    if ua.find("ipad") > 0:
        mobile= True
    if mobile:
        return True
    else:
        return False

def uploaded_file(filename):
    fd=open(settings.MEDIA_CV+str(filename),'wb+')
    for chunk in filename.chunks():
        fd.write(chunk)
    fd.close()

       
