from core.policy_engine import Decision, deny, allow
from core.capabilities import Val


def email_policy(tool_name: str, args: dict[str, Val]) -> Decision:
    if tool_name != "send_email":
        return allow("not email")
    # if there is an attachment, ensure recipient is allowed to read it
    attach = args.get("attachment")
    to = args.get("to")
    if attach:
        readers = attach.caps.readers
        if readers != "Public" and to.value not in readers:
            return deny(
                f"Recipient {to.value} is not authorized to read attachment (allowed: {readers})"
            )
    # simple safeguard: block if body comes from untrusted tool and recipient isn't in readers
    body = args.get("body")
    if body and body.caps.provenance.get("type") == "Tool":
        # if attachment missing, still check body readers if present
        readers = body.caps.readers
        if readers != "Public" and to.value not in readers:
            return deny(f"Recipient {to.value} not authorized for body content")
    return allow("email ok")
