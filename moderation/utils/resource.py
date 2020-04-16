import logging

from moderation.models import ModerationConfig, DataStore
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


def get_all_active_entity(user, tab=''):
    resp = {
        "entity_data": [],
        "active_tab": {}
    }
    try:
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
                    "filter_attribute": entity.get("filter_attributes", ''),
                    "attribute_config": make_attribute_config(entity.get("attribute_config", []))
                }
                if tab == str(entity.get("entity_id", '')):
                    tab_data["active"] = True
                    resp["active_tab"] = tab_data
                resp["entity_data"].append(tab_data)
        if not tab:
            resp["entity_data"][0]["active"] = True
            resp["active_tab"] = resp["entity_data"][0]

    except Exception as e:
        msg = "Error While Fetching entity."
        logger.critical(msg + " " + repr(e))
    return resp


def get_entity_table_data(active_tab_id, ):
    resp = []
    try:
        data_packets = DataStore.objects.filter(moderation_status=False, entity=active_tab_id)
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
            resp.append(packet_dict)
    except Exception as e:
        msg = "Error While Fetching entity data."
        logger.critical(msg + " " + repr(e))
    return resp


def get_detail_entity_view_data(unique_id):
    resp = {}
    try:
        data_packet = DataStore.objects.get(unique_id=unique_id)
        entity_config = data_packet.entity.fetch()
        entity_config_data = ModerationConfigSerializer(entity_config).data
        resp['field_description'] = make_attribute_config(entity_config_data.get("attribute_config", []))
        resp['detail_view'] = entity_config_data.get("view", {}).get('detail_view', [])
        data_packet_data = DataStoreSerializer(data_packet).data
        packet_dict = {
            "id": data_packet_data.get('id', ''),
            "unique_id": data_packet_data.get('unique_id', ''),
            "user_assigned": data_packet_data.get('user_assigned', ''),
            "entity_object_id": data_packet_data.get('entity_object_id', ''),
            "current_status": {
                "new_value": data_packet_data.get('current_status', '')
            }
        }
        packet_dict.update(data_packet_data.get('entity_data', {}).get('input_data', {}))
        resp['field_value'] = packet_dict
    except Exception as e:
        msg = "Error While Fetching entity data."
        logger.critical(msg + " " + repr(e))
    return resp
