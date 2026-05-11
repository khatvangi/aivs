"""AIVS adapters.

Importing this package causes each adapter module to register itself
via the `@register_adapter` decorator. Downstream code can then call
`discover_adapters(project_path)` to get a list of applicable
adapters.
"""

from aivs.adapters.base import (
    EvidenceAdapter,
    discover_adapters,
    register_adapter,
    registered_adapters,
)

# Trigger adapter registration by importing concrete modules.
from aivs.adapters import claude_code  # noqa: F401
from aivs.adapters import codex  # noqa: F401
from aivs.adapters import aider  # noqa: F401

__all__ = [
    "EvidenceAdapter",
    "discover_adapters",
    "register_adapter",
    "registered_adapters",
]
