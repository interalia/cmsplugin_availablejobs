from django.conf.urls.defaults import *
from availablejob.views import *

urlpatterns = patterns("availablejob.views",
     url(r"^sendcv/$",send_cv),
     url(r"^detail/(?P<id>\d+)/$", 'detail',name="job-detail"),
     url(r"^apply/(?P<id>\d+)/$", 'show_form',name="show-form"),
     url(r"^$", 'index', name="vacancy-index"),
)
