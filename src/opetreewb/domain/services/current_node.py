from PySide.QtCore import QObject, Signal
from opetreewb.messaging.reporter import Reporter
from opetreewb.domain.services.tree_service import TreeService
from opetreewb.domain.services.attribute_service import AttributeService


class CurrentNode(QObject):
    """
    CN – Current Node (like !!CE in AVEVA PML)
    """

    changed = Signal(object)               # node
    deleted = Signal(object)               # node
    attribute_changed = Signal(str, object)  # name, value
    structure_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self._node = None

        # Domain services (dummy adapters for now)
        self._tree_service = TreeService()
        self._attr_service = AttributeService()

    # -------------------------
    # Core access
    # -------------------------

    def get(self):
        return self._node

    @property
    def node(self):
        return self._node

    def set(self, node):
        self._node = node
        Reporter.info(
            f"[CN] Current node set to: "
            f"{getattr(node, 'label', None)}"
        )
        self.changed.emit(node)

    def clear(self):
        self._node = None
        Reporter.info("[CN] Current node cleared")
        self.changed.emit(None)

    # -------------------------
    # Convenience properties
    # -------------------------

    @property
    def id(self):
        return getattr(self._node, "node_id", None)

    @property
    def type(self):
        if not self._node:
            return None
        return self._node.attributes.get("Type").value

    @property
    def name(self):
        if not self._node:
            return None
        attr = self._node.attributes.get("Name")
        return attr.value if attr else None

    @property
    def attributes(self):
        if not self._node:
            return {}
        return self._node.attributes

    # -------------------------
    # Tree operations
    # -------------------------

    def create_child(self, element_type, name=""):
        if not self._node:
            Reporter.error("[CN] No current node to create child under")
            return

        Reporter.info(
            f"[CN] create_child(type={element_type}, name={name})"
        )

        ok = self._tree_service.create_node(
            self._node,
            element_type,
            name,
        )

        if not ok:
            return False

        # ✅ Structural change
        self.structure_changed.emit()

        return True

    def delete(self):
        if not self._node:
            Reporter.error("[CN] No current node to delete")
            return

        node = self._node
        Reporter.info("[CN] delete current node")

        ok = self._tree_service.delete_node(node)

        if not ok:
            return False
        
        self.structure_changed.emit()
        self.deleted.emit(node)
        self.clear()

        return True

    # -------------------------
    # Attribute operations
    # -------------------------

    def set_attr(self, name, value):
        if not self._node:
            Reporter.error("[CN] No current node")
            return

        attr = self._node.attributes.get(name)
        if not attr:
            Reporter.error(f"[CN] Attribute '{name}' does not exist")
            return
        
        ok = self._attr_service.update_attribute(
            name,
            attr.data_id,
            value,
        )

        if not ok:
            return False
        
        Reporter.info(
            f"[CN] set_attr({name}={value})"
        )
        
        self.attribute_changed.emit(name, value)

        return True

    def get_attr(self, name):
        if not self._node:
            return None
        attr = self._node.attributes.get(name)
        return attr.value if attr else None

    def allowed_child_types(self):
        if not self._node:
            return []
    
        from opetreewb.domain.schema.schema_loader import get_schema
    
        schema = get_schema(self.type)
    
        if not schema:
            return []
    
        return schema.allowed_children()