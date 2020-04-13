from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer

from moderation.models import DataPacket, DataStore


class DataPacketSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = DataPacket


class DataStoreSerializer(DocumentSerializer):
    entity_data = DataPacketSerializer(many=True)

    class Meta:
        model = DataStore
