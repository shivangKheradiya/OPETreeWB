from opetreewb.domain.schema.schema_loader import get_schema
from opetreewb.SKET.schema.attribute_ids import get_attr_name
from opetreewb.ui.model.tree_model import AttributeValue, TreeNodeModel


def node_dict_to_model(node_dict):

    node_id = node_dict["node_id"]
    attr_map = node_dict["attributes"]

    attributes = {}

    for attr_id, data in attr_map.items():
        attr_name = get_attr_name(attr_id)
        attributes[attr_name] = AttributeValue(
            data_id=data["data_id"], value=data["value"]
        )

    # build label
    name_attr = attributes.get("Name")
    type_attr = attributes.get("Type")

    if type_attr:
        schema = get_schema(type_attr.value)
        schema_attrs = schema.attributes()
        if schema:
            for attr_name, meta in schema_attrs.items():
                # ✅ If not present in DB → add empty placeholder
                if attr_name not in attributes:
                    attributes[attr_name] = AttributeValue(
                        data_id=None, value=meta.get("default")
                    )

    if type_attr and name_attr:
        label = f"{type_attr.value} {name_attr.value}"
    elif type_attr:
        label = type_attr.value
    else:
        label = str(node_id)

    return TreeNodeModel(
        node_id=node_id, label=label, attributes=attributes, children=[]
    )
