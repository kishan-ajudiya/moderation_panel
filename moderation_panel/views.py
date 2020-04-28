from django.shortcuts import redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView


class HomeView(View):

    def get(self, request):
        return redirect('/moderation/list')


class HealthCheck(APIView):

    def get(self, request):
        return Response('All Set. Working fine.', status=HTTP_200_OK)
