import logging
from django.conf import settings

from moderation.kafka_helper import Producer
from moderation.proto_helper import dict_to_proto_message
from proto_files.compiled.moderation_output_packet_pb2 import DataNode as OutputDataNode

logger = logging.getLogger('moderationLogger')


def product_data_to_kafka(key, data):
    try:
        d = OutputDataNode()
        proto_data = dict_to_proto_message(data, d)
        config = settings.MODERATION_PANEL_KAFKA_SERVER_CONF['servers']['moderation_panel_output']
        topic = config['TOPIC']
        p = Producer.get_instance(config['HOST'][0])
        p.send_msg(topic=topic, key=key.encode('utf-8'), value=proto_data)
    except Exception as e:
        message = "Error while pushing data to kafka " + repr(e)
        logger.critical(message)
