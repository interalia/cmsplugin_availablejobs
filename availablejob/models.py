from django.db import models
from django.shortcuts import redirect
from django.db.models.signals import post_save
import settings
from signals import *


class Candidate(models.Model):
    name = models.CharField(max_length=200, unique = True)
    email = models.EmailField(unique  = True )
    phone = models.CharField(max_length=15)
    cv = models.FileField(upload_to = "photos/%Y/%m/%d/")
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
