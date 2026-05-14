from enum import Enum, auto


class SessionState(Enum):
    """
    Canonical session lifecycle states.
    """

    NO_SESSION = auto()
    ACTIVE = auto()
    DIRTY = auto()
    COMMITTED = auto()
    ABORTED = auto()
