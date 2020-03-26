# Create your views here.
from django.views.generic import TemplateView


class MiscView(TemplateView):
    template_name = "app/misc.html"
