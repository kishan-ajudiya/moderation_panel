import json

import logging
from django.conf import settings
from kafka import KafkaConsumer

from moderation.models import DataStore
from moderation.proto_helper import convert_proto_message_to_dict
from proto_files.compiled.moderation_input_packet_pb2 import DataNode as InputDataNode

logger = logging.getLogger('moderationLogger')


def start_moderation_panel_consumer():
    config = settings.MODERATION_PANEL_KAFKA_SERVER_CONF['servers']['moderation_panel_input']
    topic = config['TOPIC']
    group = config['GROUP']
    consumer = KafkaConsumer(topic, group_id=group, bootstrap_servers=config['HOST'])

    for message in consumer:
        print(message.key)
        print(message.value)
        consume_moderation_input_packet(message.value)
        res_message = "ack consumed.\t%s" % message.key
        logger.info(res_message)


def consume_moderation_input_packet(proto_data):
    try:
        data = InputDataNode()
        data_dict = convert_proto_message_to_dict(proto_data, data)
        save_data_packet(data_dict)
    except Exception as e:
        message = "%s\t%s" % ("Error in consume_moderation_input_packet", repr(e))
        logger.critical(message)


def save_data_packet(data):
    try:
        obj_data = {
            "entity": data.get('entityId', ''),
            "unique_id": data.get('uniqueId', ''),
            "entity_object_id": data.get('objectId'),
            "current_status": data.get('currentStatus', ''),
            "entity_data": {
                "input_data": parse_dict(data.get('fields', []))
            }
        }
        data_obj = DataStore.from_json(json.dumps(obj_data))
        data_obj.save(force_insert=True)
    except Exception as e:
        message = "%s\t%s\t%s\t%s" % ("Error in saving input data packet", repr(e), "data:", data)
        logger.critical(message)
