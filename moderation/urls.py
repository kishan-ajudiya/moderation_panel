from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from moderation.views import ListView, DetailView, FormSubmit, UserAssign, Config, DataPacket, Reports

urlpatterns = [
    url(r"^report", login_required(Reports.as_view()), name="reports"),
    url(r"^list", login_required(ListView.as_view()), name="list-view"),
    url(r"^detail", login_required(DetailView.as_view()), name="detail-view"),
    url(r"^collect-detail", FormSubmit.as_view(), name="collect-detail"),
    url(r"^user-assign", UserAssign.as_view(), name="user-assign"),
    url(r"^config", Config.as_view(), name="config"),
    url(r"^data-packet", DataPacket.as_view(), name="data-packet")
]
