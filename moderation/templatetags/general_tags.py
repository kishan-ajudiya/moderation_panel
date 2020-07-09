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
def get_field_id(attribute, parent_id=None, obj_id=None):
    field_name = str(attribute) + "_"
    field_name += (str(parent_id) + "_") if parent_id else ''
    field_name += (str(obj_id) + "_") if obj_id else ''
    field_name += "id"
    return field_name


@register.simple_tag
def get_field_name(attribute, parent_id=None, obj_id=None):
    field_name = "data." + str(attribute) + "."
    # field_name += (str(parent_id) + ".") if parent_id else ''
    field_name += (str(obj_id) + ".") if obj_id else ''
    field_name += "value"
    return field_name


@register.simple_tag
def get_moderable_field_name(attribute, parent_id=None, obj_id=None):
    field_name = "data." + str(attribute) + "."
    # field_name += (str(parent_id) + ".") if parent_id else ''
    field_name += (str(obj_id) + ".") if obj_id else ''
    field_name += "moderable"
    return field_name


@register.simple_tag
def get_reject_reason_field_name(attribute, parent_id=None, obj_id=None):
    field_name = "data." + str(attribute) + "."
    # field_name += (str(parent_id) + ".") if parent_id else ''
    field_name += (str(obj_id) + ".") if obj_id else ''
    field_name += "reject_reason"
    return field_name


@register.simple_tag
def get_parent_field_name(attribute, parent_id=None, obj_id=None):
    field_name = "data." + str(attribute) + "."
    # field_name += (str(parent_id) + ".") if parent_id else ''
    field_name += (str(obj_id) + ".") if obj_id else ''
    field_name += "parent_id"
    return field_name


@register.simple_tag
def get_field_context(field_value_dict, attribute, parent_id=None, is_multiple=False):
    context_dict = field_value_dict.get(attribute, {})
    if parent_id:
        context_dict = context_dict.get(parent_id, {})
    if not is_multiple:
        context_dict = {None: context_dict}
    return context_dict


@register.simple_tag
def get_field_label(field_description, attribute, label, parent_label=None, obj_id=None):
    field_label = field_description.get(attribute, {}).get(label, '')
    if obj_id:
        field_label = field_label + " id: " + str(obj_id)
    if parent_label:
        field_label = field_label + " for " + str(parent_label)
    return field_label


@register.simple_tag
def get_field_choices(field_description, attribute):
    field_attr = field_description.get(attribute, {})
    return field_attr.get('choices', {})


@register.simple_tag
def get_field_selected_value(field_value, selected_field_value, attribute):
    field_attr_value = field_value.get(attribute, {}).get('new_value', [])
    selected_field_attr_value = selected_field_value.get(attribute, {}).get('edited_data', [])
    field_attr_value_list = convert_str_to_list(field_attr_value)
    selected_field_attr_value_list = convert_str_to_list(selected_field_attr_value)
    return list(set(field_attr_value_list + selected_field_attr_value_list))


def convert_str_to_list(data):
    if isinstance(data, str):
        try:
            data = data.split(',')
        except:
            data = []
    elif isinstance(data, list):
        data = data
    return data
