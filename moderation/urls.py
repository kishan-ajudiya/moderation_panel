from django.conf.urls import url

from moderation.views import MiscView

urlpatterns = [
    url(r"^misc$", MiscView.as_view(), name="misc"),
]
