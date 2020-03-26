from django.urls import path
from django.conf.urls import url, include

from rest_framework import routers

from api.v1.user_management.viewsets import *

router = routers.DefaultRouter()
# router.register("user", UserManagement, "user")

urlpatterns = [
    url(r"", include(router.urls)),
]
