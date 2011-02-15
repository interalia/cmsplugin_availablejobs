from django.contrib import admin
from django.contrib.sites.models import Site
from django.shortcuts import redirect
from  django.core.urlresolvers import reverse
from models import Opening, Candidate, EnableOpening, Require
import settings
class OpeAdmin(admin.ModelAdmin):
    raw_id_fields = ("require",)
    prepopulated_fields = {"slug": ("title",)}

class CandidatesInline(admin.TabularInline):
    model = Candidate
    extra = 1

class CandidateAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "opening", "created_on")
    list_display_links = ("name","email")
    search_fields = ("name","email",)
    list_select_related = True
class EnOpAdmin(admin.ModelAdmin):
    list_display = ("opening","get_candidates", "created_on", "get_twitter")
    raw_id_fields = ("opening",)
    inlines = [CandidatesInline]

    def get_twitter(self,obj):
        i =  Site.objects.get_current()
        d = {"twitter_account": settings.TWITTER_ACCOUNT, 
             "url": "http://" + i.domain + reverse("job-detail", args=[obj.id]),
                "msg": settings.TWITTER_MESSAGE}
        st = '<a href="http://twitter.com/share" class="twitter-share-button" data-url="%(url)s" data-text="%(msg)s" data-count="none" data-via="%(twitter_account)s" data-lang="es">Tweet</a><script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script>' % d
        return st
    get_twitter.allow_tags = True
    def get_candidates(self,obj):
        return obj.candidates.count()

admin.site.register(Opening, OpeAdmin)
admin.site.register(Require)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(EnableOpening, EnOpAdmin)
