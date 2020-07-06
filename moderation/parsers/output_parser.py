def parse_moderated_data(data_dict, field_description):
    fields = []
    for field in data_dict:
        field_name = field
        field_data = data_dict[field]
        is_editable = field_description.get(field_name, {}).get('editable', False)
        is_moderable = field_description.get(field_name, {}).get('moderable', False)
        is_multiple = field_description.get(field_name, {}).get('multiple', False)
        if is_multiple and (is_editable or is_moderable):
            for f_id in field_data:
                id_field_data = field_data[f_id]
                fields.append({
                    "id": f_id,
                    "field_name": field_name,
                    "status": id_field_data.get("moderable", ''),
                    "parent_id": id_field_data.get("parent_id", None),
                    "reject_reason": id_field_data.get("reject_reason", []),
                    "edited_data": id_field_data.get("value", "")
                    if field_description.get(field_name, {}).get('editable', False) else ""
                })
        elif is_editable or is_moderable:
            fields.append({
                "id": None,
                "field_name": field_name,
                "status": field_data.get("moderable", ''),
                "parent_id": field_data.get("parent_id", None),
                "reject_reason": field_data.get("reject_reason", []),
                "edited_data": field_data.get("value", "")
                if field_description.get(field_name, {}).get('editable', False) else ""
            })
    return fields
