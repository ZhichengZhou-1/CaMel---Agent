from core.policy_engine import Decision, allow, deny
from core.capabilities import Val


def email_policy(tool_name: str, args: dict[str, Val]) -> Decision:
    """
    Baseline policy: For send_email:
     - If there is an attachment with readers != Public, require recipient in readers.
     - If body provenance is Tool and readers != Public, require recipient in readers.
    """
    if tool_name != "send_email":
        return allow("not email")

    to = args.get("to")
    if to is None:
        return deny("no recipient provided")

    attachment = args.get("attachment")
    if attachment:
        readers = attachment.caps.readers
        if readers != "Public" and to.value not in readers:
            return deny(
                f"Recipient {to.value} is not authorized to read attachment (allowed: {readers})"
            )

    body = args.get("body")
    if (
        body
        and isinstance(body.caps.provenance, dict)
        and body.caps.provenance.get("type") == "Tool"
    ):
        readers = body.caps.readers
        if readers != "Public" and to.value not in readers:
            return deny(f"Recipient {to.value} not authorized for body content")

    return allow("email ok")
