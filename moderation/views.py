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
from .utils.resource import get_all_active_entity, get_entity_table_data, get_detail_entity_view_data


class ListView(View):
    #permission_classes = (IsAuthenticated,)
    #renderer_classes = [TemplateHTMLRenderer]
    #template_name = "app/list_view.html"
    #paginate_by = 2

    def get(self, request):
        tab = request.GET.get('tab_id', '')
        entity_data = get_all_active_entity(request.user, tab)
        active_tab_id = entity_data.get('active_tab', {}).get("entity_id", '')
        table_data = get_entity_table_data(active_tab_id)
        context = {
            "nav_bar": entity_data.get('entity_data', []),
            "active_tab": entity_data.get('active_tab', {}),
            "table_data": table_data
        }
        paginator = Paginator(table_data, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        return render(request, "app/list_view.html", context)


class DetailView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "app/detail_view.html"

    def get(self, request):
        unique_id = request.GET.get('unique_id', '')
        detail_view_data = get_detail_entity_view_data(unique_id)
        return Response(detail_view_data)


class FormSubmit(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, JSONParser]

    def get(self, request):
        return Response("get success")

    def post(self, request):
        data = json.loads(json.dumps(request.data))
        return Response(data)


class UserAssign(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication, )
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        import pdb
        pdb.set_trace()
        response = {
            "data": {},
            "message": "",
            "success": False
        }
        rep_status = status.HTTP_400_BAD_REQUEST
        try:
            rep_status = status.HTTP_200_OK
            msg = "User Assigned Successfully."
            response["message"] = msg
            response["success"] = True
        except Exception as e:
            msg = "Error While assigning user to entity."
            response["message"] = msg
            rep_status = status.HTTP_400_BAD_REQUEST
            logger.critical(msg + " " + repr(e))

        return Response(data=response, status=rep_status)


class Config(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

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
            unique_id = request.data.get('uuid', '')
            entity_id = request.data.get('entity_id', '')
            data_packet = DataStore.objects.get(unique_id=unique_id, entity=entity_id)
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
