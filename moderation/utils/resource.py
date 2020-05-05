import logging
from datetime import datetime

from django.core.paginator import Paginator

from moderation.models import ModerationConfig, DataStore
from moderation.produce_data import product_data_to_kafka
from moderation.serializers.data_store import DataStoreSerializer
from moderation.serializers.moderation_config import ModerationConfigSerializer

logger = logging.getLogger('moderationLogger')


def is_in_multiple_groups(user, group_list):
    return user.groups.filter(name__in=group_list).exists()


def make_attribute_config(config):
    config_dict = {}
    try:

        for conf in config:
            config_dict[conf["attribute_name"]] = conf
    except Exception as e:
        msg = "Error While Fetching entity."
        logger.critical(msg + " " + repr(e))
    return config_dict


def get_all_active_entity(user, entity_id=''):
    resp = {
        "entity_data": [],
        "active_entity": {}
    }
    status = False
    try:
        logger.info("fetching active entity. for user id " + str(user.id))
        entities = ModerationConfig.objects.only("entity_name", "entity_id", "user_permission", "group",
                                                 "filter_attributes", "view__list_view", "attribute_config") \
            .filter(is_active=True)
        entities = ModerationConfigSerializer(entities, many=True).data
        for entity in entities:
            user_permissions = entity.get("user_permission", [])
            group = entity.get("group", [])
            if (user_permissions and user.has_perms(user_permissions)) or is_in_multiple_groups(user, group):
                tab_data = {
                    "entity_id": entity.get("entity_id", ''),
                    "entity_name": entity.get("entity_name", ''),
                    "active": False,
                    "list_view": entity.get("view", {}).get('list_view', []),
                    "filter_attributes": entity.get("filter_attributes", []),
                    "attribute_config": make_attribute_config(entity.get("attribute_config", []))
                }
                if entity_id == str(entity.get("entity_id", '')):
                    tab_data["active"] = True
                    resp["active_entity"] = tab_data
                resp["entity_data"].append(tab_data)
        if not entity_id:
            resp["entity_data"][0]["active"] = True
            resp["active_entity"] = resp["entity_data"][0]
        status = True
        logger.info("fetched active entity. for user id " + str(user.id))
    except Exception as e:
        msg = "Error While Fetching entity."
        logger.critical(msg + " " + repr(e))
    return status, resp


def get_entity_table_data(active_entity_id, row_query):
    resp = {
        "pending_packets": [],
        "moderated_packets": []
    }
    status = False
    try:
        logger.info("get_entity_table_data for tab id " + str(active_entity_id))
        if row_query:
            row_query['entity'] = active_entity_id
            data_packets = DataStore.objects.filter(__raw__=row_query).order_by('-created')
        else:
            data_packets = DataStore.objects.filter(entity=active_entity_id).order_by('-created')
        data_packets_data = DataStoreSerializer(data_packets, many=True).data
        for packet in data_packets_data:
            packet_dict = {
                "id": packet.get('id', ''),
                "unique_id": packet.get('unique_id', ''),
                "entity_object_id": packet.get('entity_object_id', ''),
                "user_assigned": packet.get('user_assigned', ''),
                "current_status": {
                    "new_value": packet.get('current_status', '')
                }
            }
            packet_dict.update(packet.get('entity_data', {}).get('input_data', {}))
            if packet.get("is_moderation_done", False):
                resp["moderated_packets"].append(packet_dict)
            else:
                resp["pending_packets"].append(packet_dict)

        status = True
        logger.info("Entity table data fetched " + str(active_entity_id))
    except Exception as e:
        msg = "Error While Fetching entity data."
        logger.critical(msg + " " + repr(e))
    return status, resp


def get_list_view_context(entity_id, pending_page, moderated_page, user, filter_params={}):
    row_query = {}
    for ele in filter_params:
        if filter_params.get(ele):
            query_key = "entity_data.input_data." + ele + ".new_value"
            row_query[query_key] = {"$regex": ".*" + filter_params.get(ele, '') + ".*"}

    stat, entity_data = get_all_active_entity(user, entity_id)
    active_entity_id = entity_data.get('active_entity', {}).get("entity_id", '')
    stat, table_data = get_entity_table_data(active_entity_id, row_query)
    context = {
        "nav_bar": entity_data.get('entity_data', []),
        "active_entity": entity_data.get('active_entity', {})
    }

    active_tab = 'moderated' if moderated_page else 'pending'
    context['active_tab'] = active_tab
    pending_paginator = Paginator(table_data.get('pending_packets', []), 20)
    pending_page_number = pending_page if pending_page else 1
    pending_page_obj = pending_paginator.get_page(pending_page_number)
    context["pending_page_obj"] = pending_page_obj

    moderated_paginator = Paginator(table_data.get('moderated_packets', []), 20)
    moderated_page_number = moderated_page if moderated_page else 1
    moderated_page_obj = moderated_paginator.get_page(moderated_page_number)
    context["moderated_page_obj"] = moderated_page_obj
    return context


def get_detail_entity_view_data(unique_id):
    resp = {}
    status = False
    try:
        logger.info("Fetching entity detail view data for unique id" + str(unique_id))
        data_packet = DataStore.objects.get(unique_id=unique_id)
        entity_config = data_packet.entity.fetch()
        entity_config_data = ModerationConfigSerializer(entity_config).data
        resp['field_description'] = make_attribute_config(entity_config_data.get("attribute_config", []))
        resp['detail_view'] = entity_config_data.get("view", {}).get('detail_view', [])
        resp['entity_id'] = entity_config_data.get("entity_id", "")
        resp['entity_name'] = entity_config_data.get("entity_name", "")
        resp['reject_reason'] = entity_config_data.get("reject_reason", {})
        data_packet_data = DataStoreSerializer(data_packet).data
        packet_dict = {
            "id": data_packet_data.get('id', ''),
            "is_moderation_done": data_packet_data.get('is_moderation_done', False),
            "unique_id": data_packet_data.get('unique_id', ''),
            "user_assigned": data_packet_data.get('user_assigned', ''),
            "entity_object_id": data_packet_data.get('entity_object_id', ''),
            "current_status": {
                "new_value": data_packet_data.get('current_status', '')
            },
            "selected_reject_reason": data_packet_data.get('reject_reason', []),
            "moderation_status": data_packet_data.get('moderation_status', [])
        }
        packet_dict.update(data_packet_data.get('entity_data', {}).get('input_data', {}))
        resp['field_value'] = packet_dict
        status = True
    except Exception as e:
        msg = "Error While Fetching entity data."
        logger.critical(msg + " " + repr(e))
    return status, resp


def assign_revoke_user_to_packet(unique_id, user_assignment, username):
    msg = ""
    status = False
    try:
        logger.info("assign_revoke_user_to_packet for unique id and user id " + str(unique_id)
                    + " and " + str(username))
        data_packet = DataStore.objects.get(unique_id=unique_id)
        if data_packet.user_assigned and data_packet.user_assigned != username:
            return False, "You can not assign already assigned packet"

        if user_assignment:
            data_packet.user_assigned = username
            msg = "User Assigned Successfully."
        else:
            data_packet.user_assigned = ''
            msg = "User Revoked Successfully."

        data_packet.save()
        status = True
        logger.info("user assigned for unique id and user id " + str(unique_id)
                    + " and " + str(username))
    except Exception as e:
        msg = "Error While assign/revoke user from data packet."
        logger.critical(msg + " " + repr(e))
    return status, msg


def save_moderated_data(data, user):
    msg = ""
    status = False
    try:
        unique_id = data.get('unique_id', '')
        if not unique_id:
            return False, "Packet id is not present."
        data_packet = DataStore.objects.get(unique_id=unique_id)
        data_packet_data = DataStoreSerializer(data_packet).data
        if data_packet_data.get('user_assigned', '') and data_packet_data.get('user_assigned', '') != user.username:
            return False, "Data Packet is not assigned to you."
        output_data_packet = {
            "entity_id": data_packet.entity.id,
            "unique_id": data_packet_data.get("unique_id", None),
            "object_id": data_packet_data.get("entity_object_id", None),
            "current_status": data_packet_data.get("current_status", None),
            "moderation_status": data.get("action", None),
            "moderated_by": user.username,
            "moderated_by_id": user.id,
            "reject_reason": data.get("reject_reason", []),
        }
        data_packet.is_moderation_done = True
        data_packet.user_assigned = output_data_packet.get("moderated_by", None)
        data_packet.moderation_status = output_data_packet.get("moderation_status", None)
        data_packet.reject_reason = output_data_packet.get("reject_reason", [])
        data_packet.moderated_time = datetime.now()
        data_packet.save()
        product_data_to_kafka(str(data_packet_data.get("unique_id")), output_data_packet)
        status = True
        msg = "Data saved Successfully."
    except Exception as e:
        msg = "Error While saving response to data packet."
        logger.critical(msg + " " + repr(e))
    return status, msg
