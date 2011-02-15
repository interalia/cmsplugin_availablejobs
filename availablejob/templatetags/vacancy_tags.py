from django import template
from availablejob.models import EnableOpening

register = template.Library()

@register.inclusion_tag("vacancy/list_openings.html")
def list_openings():
    opens = EnableOpening.objects.all()
    return dict(opens = opens)


