# Create your views here.
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class MiscView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "app/list_view.html"

    def get(self, request):
        context = {"nav_list": [{"name": "event_cal", "active": False}, {"name": "notices", "active": True}]}
        return Response({'nav_list': context['nav_list']})

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["nav_list"] = [{"name": "event_cal", "active": False}, {"name": "notices", "active": True}]
    #     return context
