from pydantic import BaseModel


class Decision(BaseModel):
    allowed: bool
    reason: str


def allow(reason: str = "allowed") -> Decision:
    return Decision(allowed=True, reason=reason)


def deny(reason: str = "denied") -> Decision:
    return Decision(allowed=False, reason=reason)
