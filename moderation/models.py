import datetime

from mongoengine import *
from mongoengine import signals


class MongoDocument(Document):
    created = DateTimeField(default=datetime.datetime.utcnow)
    modified = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'abstract': True
    }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.modified = datetime.datetime.utcnow()


class ViewConfig(EmbeddedDocument):
    list_view = ListField(StringField(max_length=50))
    detail_view = DynamicField()


class AttributeConfig(EmbeddedDocument):
    attribute_name = StringField()
    view_type = StringField()
    label = StringField()
    editable = BooleanField(default=False)
    moderable = BooleanField(default=False)
    meta_fields = ListField(StringField())
    data_type = StringField()
    reject_reason = ListField(StringField())
    object_type = StringField()
    multiple = BooleanField(default=False)
    child_attr = ListField(StringField())


class ModerationConfig(MongoDocument):
    entity_id = IntField(primary_key=True)
    entity_name = StringField()
    help_text = StringField()
    user_permission = ListField(StringField(max_length=50))
    group = ListField(StringField(max_length=50))
    response_config = DictField()
    display_links = ListField(StringField(max_length=50))
    filter_attributes = ListField(StringField(max_length=50))
    reject_reason = ListField()
    required_attributes = ListField(StringField())
    view = EmbeddedDocumentField(ViewConfig)
    attribute_config = EmbeddedDocumentListField(AttributeConfig)
    is_list_moderable = BooleanField(default=False)
    is_active = BooleanField(default=True)

    def save(
        self,
        force_insert=False,
        validate=True,
        clean=True,
        write_concern=None,
        cascade=None,
        cascade_kwargs=None,
        _refs=None,
        save_condition=None,
        signal_kwargs=None,
        **kwargs
    ):
        super(MongoDocument, self).save(force_insert=True)


class DataPacket(EmbeddedDocument):
    input_data = DictField()
    moderated_data = DictField()


class DataStore(MongoDocument):
    entity = LazyReferenceField(ModerationConfig, reverse_delete_rule=1)
    user_assigned = StringField(null=True)
    unique_id = UUIDField(unique=True, binary=False)
    entity_object_id = IntField(null=True)
    current_status = StringField(null=True)
    entity_data = EmbeddedDocumentField(DataPacket)
    moderation_status = StringField(null=True, default="pending")
    moderation_time = DateTimeField(null=True)
    reject_reason = ListField()
    is_moderation_done = BooleanField(default=False)


signals.pre_save.connect(MongoDocument.pre_save, sender=ModerationConfig)
signals.pre_save.connect(MongoDocument.pre_save, sender=DataStore)
