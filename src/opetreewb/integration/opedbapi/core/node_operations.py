from opetreewb.integration.opedbapi.utils.schema_helper import load_element_schema


def build_node_create_operations(
    *,
    parent_node_id,
    type_value,
    name,
    id_gen
):
    node_id = id_gen.next_id()

    schema = load_element_schema(type_value)

    operations = []

    for attr_name, meta in schema.items():

        attr_id = meta["id"]

        if attr_name == "Name":
            value = name if name is not None else ""
            data_id = node_id  # ✅ identity rule

        elif attr_name == "Type":
            value = type_value
            data_id = id_gen.next_id()

        elif attr_name == "Owner":
            value = parent_node_id
            data_id = id_gen.next_id()

        else:
            continue

        operations.append({
            "data_id": data_id,
            "node_id": node_id,
            "attribute_id": attr_id,
            "value": value,
        })

    return node_id, operations