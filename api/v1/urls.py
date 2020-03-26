from django.conf.urls import *

urlpatterns = [
	url(r"^v1/", include("api.v1.user_management.urls"), name="v1")
]