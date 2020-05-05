import json

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from mongoengine import NotUniqueError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from . import logger
from .models import ModerationConfig, DataStore
from .serializers.data_store import DataStoreSerializer
from .serializers.moderation_config import ModerationConfigSerializer
from .utils.resource import get_all_active_entity, get_entity_table_data, get_detail_entity_view_data, \
    assign_revoke_user_to_packet, save_moderated_data, get_list_view_context


class ListView(View):

    def get(self, request):
        entity_id = request.GET.get('entity_id', '')
        pending_page = request.GET.get('pending_page', '')
        moderated_page = request.GET.get('moderated_page', '')
        user = request.user
        context = get_list_view_context(entity_id, pending_page, moderated_page, user)
        return render(request, "app/list_view.html", context)

    def post(self, request):
        request_data = {}
        for k in request.POST:
            request_data[k] = request.POST.get(k)
        request_data.pop('csrfmiddlewaretoken', None)
        entity_id = request_data.pop('entity_id', '')
        pending_page = request_data.pop('pending_page', '')
        moderated_page = request_data.pop('moderated_page', '')
        user = request.user
        context = get_list_view_context(entity_id, pending_page, moderated_page, user, request_data)
        return render(request, "app/list_view.html", context)


class DetailView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "app/detail_view.html"

    def get(self, request):
        unique_id = request.GET.get('unique_id', '')
        stat, detail_view_data = get_detail_entity_view_data(unique_id)
        return Response(detail_view_data)


class FormSubmit(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, JSONParser]

    def get(self, request):
        return Response("get success")

    def post(self, request):
        response = {
            "data": {},
            "message": "",
            "success": False
        }
        data = request.data
        stat, resp = save_moderated_data(data, request.user)
        response["message"] = resp
        response["success"] = True
        rep_status = status.HTTP_200_OK if stat else status.HTTP_400_BAD_REQUEST
        return Response(data=response, status=rep_status)


class UserAssign(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = {
            "data": {},
            "message": "",
            "success": False
        }
        rep_status = status.HTTP_400_BAD_REQUEST
        try:
            unique_id = request.data.get("unique_id", "")
            user_assignment = request.data.get("user_assignment", "")
            stat, msg = assign_revoke_user_to_packet(unique_id, user_assignment, request.user.username)
            if stat:
                rep_status = status.HTTP_200_OK
                response["success"] = True
            response["message"] = msg
        except Exception as e:
            msg = "Error While assigning user to entity."
            response["message"] = msg
            rep_status = status.HTTP_400_BAD_REQUEST
            logger.critical(msg + " " + repr(e))

        return Response(data=response, status=rep_status)


class Config(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        response = {
            "data": {},
            "message": "",
            "success": False
        }
        rep_status = status.HTTP_400_BAD_REQUEST
        try:
            entity_id = request.data.get('entity_id', '')
            config_packet = ModerationConfig.objects.get(entity_id=entity_id)
            response["data"] = ModerationConfigSerializer(config_packet).data
            response["success"] = True
            rep_status = status.HTTP_200_OK
        except NotUniqueError as e:
            response["message"] = "Moderation Config is already exist."
            logger.error(response["msg"])
        except Exception as e:
            response["message"] = repr(e)
            logger.error(response["message"])
        return Response(data=response, status=rep_status)

    def post(self, request):
        """

        :param request:
        :return:

        """
        response = {
            "data": {},
            "message": "",
            "success": False
        }
        rep_status = status.HTTP_400_BAD_REQUEST
        try:
            data = request.data
            config_obj = ModerationConfig.from_json(json.dumps(data))
            config_obj.save()
            response["data"] = json.loads(config_obj.to_json())
            response["success"] = True
            rep_status = status.HTTP_200_OK
        except NotUniqueError as e:
            response["message"] = "Moderation Config is already exist."
            logger.error(response["msg"])
        except Exception as e:
            response["message"] = repr(e)
            logger.error(response["message"])
        return Response(data=response, status=rep_status)

    def put(self, request):
        response = {
            "data": {},
            "message": "",
            "success": False
        }
        rep_status = status.HTTP_400_BAD_REQUEST
        try:
            data = request.data
            entity_id = data.pop('entity_id')
            config_obj = ModerationConfig.objects.get(entity_id=entity_id)
            config_obj.update(**data)
            response["data"] = json.loads(config_obj.to_json())
            response["success"] = True
            rep_status = status.HTTP_200_OK
        except NotUniqueError as e:
            response["message"] = "Moderation Config is already exist."
            logger.error(response["msg"])
        except Exception as e:
            response["message"] = repr(e)
            logger.error(response["message"])
        return Response(data=response, status=rep_status)


class DataPacket(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        response = {
            "data": {},
            "message": "",
            "success": False
        }
        rep_status = status.HTTP_400_BAD_REQUEST
        try:
            unique_id = request.data.get('unique_id', '')
            entity_id = request.data.get('entity_id', '')
            data_packet = DataStore.objects.get(unique_id=unique_id, entity=entity_id)
            response["data"] = DataStoreSerializer(data_packet).data
            response["success"] = True
            rep_status = status.HTTP_200_OK
        except NotUniqueError as e:
            response["message"] = "Moderation Config is already exist."
            logger.error(response["msg"])
        except Exception as e:
            response["message"] = repr(e)
            logger.error(response["message"])
        return Response(data=response, status=rep_status)

    def post(self, request):
        response = {
            "data": {},
            "message": "",
            "success": False
        }
        rep_status = status.HTTP_400_BAD_REQUEST
        try:
            data = request.data
            data_packet = DataStore.from_json(json.dumps(data))
            data_packet.save()
            response["data"] = json.loads(data_packet.to_json())
            response["success"] = True
            rep_status = status.HTTP_200_OK
        except NotUniqueError as e:
            response["message"] = "Moderation Config is already exist."
            logger.error(response["msg"])
        except Exception as e:
            response["message"] = repr(e)
            logger.error(response["message"])
        return Response(data=response, status=rep_status)
