from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer

from moderation.models import ModerationConfig, ViewConfig, AttributeConfig


class ViewConfigSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = ViewConfig


class AttributeConfigSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = AttributeConfig


class ModerationConfigSerializer(DocumentSerializer):
    attribute_config = AttributeConfigSerializer(many=True)
    view = ViewConfigSerializer()

    class Meta:
        model = ModerationConfig
