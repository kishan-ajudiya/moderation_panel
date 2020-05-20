from collections import defaultdict


def parse_dict(data):
    response_dict = defaultdict(dict)
    for field in data:
        field_name = field.get("field_name", "")
        field_id = field.get("id", "")
        parent_id = field.get("parent_id", "")

        if field_name and field_name not in response_dict:
            response_dict[field_name] = {}

        if parent_id and field_id:
            if parent_id not in response_dict[field_name]:
                response_dict[field_name][parent_id] = {}
            response_dict[field_name][parent_id][field_id] = field
        elif parent_id:
            response_dict[field_name][parent_id] = field
        elif field_id:
            response_dict[field_name][field_id] = field
        else:
            response_dict[field_name] = field
    return response_dict
