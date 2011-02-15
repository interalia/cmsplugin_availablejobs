from django.conf.urls.defaults import *

urlpatterns = patterns("availablejob.views",
     url(r"^detail/(?P<id>\d+)/$", 'detail',name="job-detail"),
     url(r"^apply/(?P<id>\d+)/$", 'show_form',name="show-form"),
     url(r"^sendcv/$", 'send_cv',name="send-cv"),
     url(r"^$", 'index', name="vacancy-index"),
)
