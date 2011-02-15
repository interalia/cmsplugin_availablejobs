from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class AvailableJobApp(CMSApp):
    name = u"AvailableJob"
    urls = ["availablejob.urls"]

apphook_pool.register(AvailableJobApp)
