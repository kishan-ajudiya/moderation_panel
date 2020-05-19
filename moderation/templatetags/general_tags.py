from django import template

register = template.Library()


@register.filter
def hash(h, key):
    return h.get(key, None)


@register.simple_tag
def get_field_value(data_dict, attribute, key, parent_id=None, obj_id=None):
    field_value = data_dict.get(attribute, {})
    if parent_id:
        field_value = field_value.get(parent_id, {})
    if obj_id:
        field_value = field_value.get(obj_id, {})
    return field_value.get(key, '')


@register.simple_tag
def get_field_name(attribute, parent_id=None, obj_id=None):
    field_name = str(attribute) + "."
    field_name += (str(parent_id) + ".") if parent_id else ''
    field_name += (str(obj_id) + ".") if obj_id else ''
    field_name += "value"
    return field_name


@register.simple_tag
def get_field_id(attribute, parent_id=None, obj_id=None):
    field_name = str(attribute) + "_"
    field_name += (str(parent_id) + "_") if parent_id else ''
    field_name += (str(obj_id) + "_") if obj_id else ''
    field_name += "id"
    return field_name


@register.simple_tag
def get_moderable_field_name(attribute, parent_id=None, obj_id=None):
    field_name = str(attribute) + "."
    field_name += (str(parent_id) + ".") if parent_id else ''
    field_name += (str(obj_id) + ".") if obj_id else ''
    field_name += "moderable"
    return field_name


@register.simple_tag
def get_field_context(field_value_dict, attribute, parent_id, is_multiple):
    context_dict = field_value_dict.get(attribute, {})
    if parent_id:
        context_dict = context_dict.get(parent_id, {})
    if not is_multiple:
        context_dict = {None: context_dict}
    return context_dict
