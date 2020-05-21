def parse_moderated_data(data_dict, field_description):
    fields = []
    for field in data_dict:
        field_name = field
        field_data = data_dict[field]
        if field_description.get(field_name, {}).get('multiple', False):
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
        else:
            fields.append({
                "id": None,
                "field_name": field_name,
                "status": field_data.get("moderable", ''),
                "parent_id": field_data.get("parent_id", None),
                "reject_reason": field_data.get("reject_reason", []),
                "edited_data": id_field_data.get("value", "")
                if field_description.get(field_name, {}).get('editable', False) else ""
            })
    return fields
