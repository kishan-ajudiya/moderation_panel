from django.conf.urls import *

urlpatterns = [
	url(r"^api/", include("api.v1.urls"), name="api"),
]