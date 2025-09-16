from pydantic import BaseModel


class Decision(BaseModel):
    allowed: bool
    reason: str


def deny(reason: str) -> Decision:
    return Decision(allowed=False, reason=reason)


def allow(reason: str = "ok") -> Decision:
    return Decision(allowed=True, reason=reason)
