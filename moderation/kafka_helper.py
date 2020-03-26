import logging

from kafka import KafkaProducer
from kafka.errors import KafkaError

logger = logging.getLogger('moderationLogger')


class Producer:
    kafka_producer = object()
    _instances = {}

    @staticmethod
    def get_instance(server_address):
        """ Static access method. """
        if server_address not in Producer._instances:
            logger.info("Connection not present. Creating Connection.")
            Producer(server_address)
        elif not Producer._instances.get(server_address).kafka_producer.bootstrap_connected():
            logger.info("Connection closed. Creating Connection.")
            Producer._instances.pop(server_address)
            Producer(server_address)
        return Producer._instances.get(server_address)

    def __init__(self, server_address):
        if server_address not in Producer._instances:
            self.kafka_producer = KafkaProducer(bootstrap_servers=server_address, request_timeout_ms=50000)
            self._instances[server_address] = self
        else:
            self.kafka_producer = self._instances[server_address].kafka_producer

    def on_send_success(self, record_metadata):

        message = "Message sent successfully to queue."
        logger.info(message)

    def on_send_error(self, excp):
        message = "Message not sent successfully to queue. Error==>" + repr(excp)
        logger.error(message)

    def send_msg(self, topic, key, value):
        future = self.kafka_producer.send(topic=topic, key=key, value=value).add_callback(self.on_send_success) \
            .add_errback(self.on_send_error)

        data = {}
        try:
            record_metadata = future.get(timeout=10)
            data = {
                "kafka_topic": record_metadata.topic,
                "kafka_partition": record_metadata.partition,
                "kafka_offset": record_metadata.offset
            }
        except KafkaError as e:
            self.on_send_error(e)
            pass
        except Exception as e:
            self.on_send_error(e)
            pass
        return data


