from django.db import models
from django.shortcuts import redirect
from django.db.models.signals import post_save
import settings
from signals import *
import hashlib
import time

def file_dir(instance, filename):
    """ Cambia el nombre del archivo para que no sea descargable """
    #name =  DIR_FILES_GUIAS +date.strftime("%Y_%m_%d_%s_") + filename.encode("utf-8")
    def timestamp():
        lt = time.localtime(time.time())
        return "%02d%02d%04d%02d%02d%02d" % (lt[2], lt[1], lt[0], lt[3], lt[4], lt[5])

    return "%s%s.%s" % ('cv_list/', hashlib.sha1("%s-%s" % ( timestamp(), instance.pk)).hexdigest(), filename.split('.')[-1])


class Candidate(models.Model):
    name = models.CharField(max_length=200, unique = True)
    email = models.EmailField(unique  = True )
    phone = models.CharField(max_length=15)
    cv = models.FileField(upload_to = file_dir)
    opening = models.ForeignKey("EnableOpening", related_name="candidates", null = True, blank = True )
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.name

class Require(models.Model):
    description = models.TextField()
    def __unicode__(self):
        return self.description

class Opening(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    require = models.ForeignKey(Require, related_name="openings")
    slug = models.SlugField()
    def __unicode__(self):
        return self.title

class EnableOpening(models.Model):
    opening = models.ForeignKey(Opening, related_name="enable_openings")
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    @models.permalink
    def get_absolute_url(self):
        return ("job-detail", [self.id])
    def __unicode__(self):
        return self.opening.title



post_save.connect(enviar_email, sender = Candidate)
