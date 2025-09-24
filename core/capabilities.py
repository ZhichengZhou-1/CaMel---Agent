from __future__ import annotations
from typing import Any, Dict, Optional, Set
from pydantic import BaseModel, Field
import uuid


class Capability(BaseModel):
    provenance: Dict[str, Any] = Field(default_factory=dict)
    readers: Optional[Set[str]] | str = "Public"  # "Public" or set of emails
    tags: Set[str] = Field(default_factory=set)

    def merge(self, other: "Capability") -> "Capability":
        """Return a new capability that is the union of self and other."""
        # provenance: collect both as list entries
        prov = {"merged_from": [self.provenance, other.provenance]}
        # readers: if either is Public -> Public; else union sets
        if self.readers == "Public" or other.readers == "Public":
            readers = "Public"
        else:
            readers = set(self.readers) | set(other.readers)
        tags = set(self.tags) | set(other.tags)
        return Capability(provenance=prov, readers=readers, tags=tags)


class Val(BaseModel):
    val_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    value: Any
    caps: Capability

    def derive_from(self, parents: list["Val"], op: str) -> "Val":
        """Create derived Val whose capability is merged from parents + this."""
        if not parents:
            return self
        merged = parents[0].caps
        for p in parents[1:]:
            merged = merged.merge(p.caps)
        # also merge this.caps
        merged = merged.merge(self.caps)
        return Val(value=self.value, caps=merged)
