from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer, drf_fields

from moderation.models import DataPacket, DataStore


class DataPacketSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = DataPacket


class DataStoreSerializer(DocumentSerializer):
    entity_data = DataPacketSerializer()
    created = drf_fields.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = DataStore
