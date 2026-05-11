from opetreewb.ui.model.tree_model import TreeNodeModel, AttributeValue
from opetreewb.SKET.schema.attribute_ids import ATTR_ID


def node_dict_to_model(node_dict):

    node_id = node_dict["node_id"]
    attr_map = node_dict["attributes"]

    attributes = {}

    for name, attr_id in ATTR_ID.items():

        if attr_id in attr_map:
            data = attr_map[attr_id]

            attributes[name] = AttributeValue(
                data_id=data["data_id"],
                value=data["value"]
            )

    # build label
    name_attr = attributes.get("Name")
    type_attr = attributes.get("Type")

    if type_attr and name_attr:
        label = f"{type_attr.value} {name_attr.value}"
    elif type_attr:
        label = type_attr.value
    else:
        label = str(node_id)

    return TreeNodeModel(
        node_id=node_id,
        label=label,
        attributes=attributes,
        children=[]
    )