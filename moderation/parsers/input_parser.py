def parse_dict(data):
    response_dict = {}
    for field in data:
        field_name = field.get("field_name", '')
        id = field.get('id', '')
        parent_id = field.get('parent_id', '')

        if field_name and field_name not in response_dict:
            response_dict[field_name] = {}

        if parent_id and id:
            response_dict[field_name][parent_id][id] = field
        elif parent_id:
            response_dict[field_name][parent_id] = field
        elif id:
            response_dict[field_name][id] = field
        else:
            response_dict[field_name] = field
    return response_dict
