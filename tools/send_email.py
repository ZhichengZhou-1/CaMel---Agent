from core.capabilities import Val, Capability

SENT = []  # for demo


def send_email(to: Val, subject: Val, body: Val, attachment: Val | None = None) -> Val:
    # send fake emails (not actually sending anything...)
    SENT.append(
        {
            "to": to.value,
            "subject": subject.value,
            "body": body.value,
            "attachment": getattr(attachment, "value", None),
        }
    )
    return Val(
        value="sent",
        caps=Capability(
            provenance={"type": "Tool", "tool_id": "email"}, readers="Public", tags=set()
        ),
    )
