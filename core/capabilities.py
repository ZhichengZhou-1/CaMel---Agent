from __future__ import annotations
from typing import Literal, Optional, Set, Dict, Any
from pydantic import BaseModel

SourceType = Literal["User", "CaMeL", "Tool"]


class Capability(BaseModel):
    provenance: Dict[str, Any]  # e.g. {"type":"Tool","tool_id":"cloud_drive","inner":"file:123"}
    readers: Optional[Set[str]] | Literal["Public"] = "Public"
    tags: Set[str] = set()  # e.g. {"PII","Finance","Secret"}


class Val(BaseModel):
    value: Any
    caps: Capability
