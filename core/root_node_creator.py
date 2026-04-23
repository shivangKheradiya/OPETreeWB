from OPETreeWB.core.domain_rules import DOMAIN_RULES
from OPETreeWB.core.app_context import APP_CONTEXT


def create_root_node(provider):
    """
    Create a root node according to application domain rules.
    """
    domain = APP_CONTEXT.domain
    rules = DOMAIN_RULES.get(domain)

    if not rules:
        raise RuntimeError(f"No rules for domain {domain}")

    root_type = rules["RootType"]
    max_roots = rules["MaxRoots"]

    # Check existing root nodes (Owner == None)
    owner_attr = provider.registry.get_id("Owner")
    existing_roots = provider.search_by_attribute(
        attribute_id=owner_attr,
        value=None,
    )

    if max_roots is not None and len(existing_roots) >= max_roots:
        raise RuntimeError("Root already exists")

    return provider.create_node(
        parent_node_id=None,
        type_value=root_type,
        name=None,
    )