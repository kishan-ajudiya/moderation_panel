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
                                                 "filter_attributes", "view__list_view", "attribute_config").filter(
            is_active=True)
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


def get_detail_view_context(data_packet_id):
    resp = {}
    try:
        data_packet = DataStore.objects.get(_id=data_packet_id)
        entity_config = data_packet.entity.fetch()
        data_packet_data = DataStoreSerializer(data_packet).data
        entity_config_data = ModerationConfigSerializer(entity_config).data
        field_description = make_attribute_config(entity_config_data.get("attribute_config", []))
        detail_view = entity_config_data.get("view", {}).get('detail_view', [])
    except Exception as e:
        msg = "Error While Fetching entity data."
        logger.critical(msg + " " + repr(e))
    return resp


def get_entity_table_data(active_tab_id):
    resp = []
    try:
        data_packets = DataStore.objects.filter(moderation_status=False, entity=active_tab_id)

    except Exception as e:
        msg = "Error While Fetching entity data."
        logger.critical(msg + " " + repr(e))
    return resp
