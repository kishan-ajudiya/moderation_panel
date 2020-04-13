import json

from mongoengine import NotUniqueError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from . import logger
from .models import ModerationConfig, DataStore
from .utils.resource import get_all_active_entity, get_entity_table_data


class ListView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "app/list_view.html"

    def get(self, request):
        tab = request.GET.get('tab_id', '')
        entity_data = get_all_active_entity(request.user, tab)
        active_tab_id = entity_data.get('active_tab', {}).get("entity_id", '')
        table_data = get_entity_table_data(active_tab_id)
        context = {
            "nav_bar": entity_data.get('entity_data', []),
            "active_tab": entity_data.get('active_tab', {}),
        }
        return Response(context)


class DetailView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "app/detail_view.html"

    def get(self, request):
        context = '{"detail_view":[["User Details",{"help_text":"","fields":["user","modifiedon","createdon"]}],' \
                  '["Event Details",{"help_text":"","fields":["event_name","event_address"]}],["Event Duration",' \
                  '{"help_text":"","fields":["start_date","end_date"]}],["Event Images",{"help_text":"",' \
                  '"fields":["images"]}],["Event Location",{"help_text":"","fields":["latitude","longitude"]}]],' \
                  '"field_description":{"user":{"label":"Created by","type":"text","is_editable":false,' \
                  '"is_moderable":true,"child_attr":["abc","def"]},"abc":{"label":"ABC","type":"text",' \
                  '"is_editable":false,"is_moderable":true,"child_attr":["ghi"]},"ghi":{"label":"GHI","type":"text",' \
                  '"is_editable":false,"is_moderable":true},"def":{"label":"DEF","type":"text","is_editable":false,' \
                  '"is_moderable":true},"modifiedon":{"label":"Modified On","type":"text","is_editable":false,' \
                  '"is_moderable":true},"createdon":{"label":"Created On","type":"text","is_editable":false,' \
                  '"is_moderable":true},"event_name":{"label":"Event Name","type":"text","is_editable":true,' \
                  '"is_moderable":true},"event_address":{"label":"Event Address","type":"text","is_editable":true,' \
                  '"is_moderable":true},"start_date":{"label":"Stare Date","type":"date","is_editable":false,' \
                  '"is_moderable":true},"end_date":{"label":"End Date","type":"date","is_editable":false,' \
                  '"is_moderable":true},"images":{"label":"Images","type":"image","is_editable":false,' \
                  '"is_multiplae":true,"is_moderable":true,"child_attr":["caption","tags"]},"caption":{' \
                  '"label":"Caption","type":"text","is_editable":false,"is_moderable":true},"tags":{"label":"Tags",' \
                  '"type":"multiselect","is_editable":false,"is_moderable":true},"latitude":{"label":"Latitude",' \
                  '"type":"multiselect","is_editable":true,"is_moderable":true},"longitude":{"label":"Longitude",' \
                  '"type":"text","is_editable":true,"is_moderable":true}}} '
        context = json.loads(context)
        return Response(context)

    def post(self, request):
        context = json.loads(context)
        return Response(context)


class FormSubmit(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, JSONParser]

    def get(self, request):
        return Response("get success")

    def post(self, request):
        data = json.loads(json.dumps(request.data))
        return Response(data)


class UserAssign(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
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
