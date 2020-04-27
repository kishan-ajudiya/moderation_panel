import logging

from google.protobuf.json_format import ParseDict, MessageToDict

logger = logging.getLogger('moderationLogger')


def convert_proto_message_to_dict(proto_message, obj):
    try:
        obj.ParseFromString(proto_message)
        data_dict = MessageToDict(obj, preserving_proto_field_name=True)
        return data_dict
    except Exception as e:
        message = "%s\t%s" % ("Error in converting proto to dict", repr(e))
        logger.critical(message)


def dict_to_proto_message(data_dict, obj):
    try:
        obj = ParseDict(data_dict, obj,ignore_unknown_fields=True)
        return obj.SerializeToString()
    except Exception as e:
        message = "%s\t%s" % ("Error in converting dict to proto", repr(e))
        logger.critical(message)
