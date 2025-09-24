from core.capabilities import Val, Capability

SENT = []


def send_email(to: Val, subject: Val, body: Val, attachment: Val | None = None) -> Val:
    # For Phase 0, just log sends to SENT
    entry = {
        "to": to.value,
        "subject": subject.value,
        "body": body.value,
        "attachment": getattr(attachment, "value", None),
    }
    SENT.append(entry)
    out_caps = Capability(provenance={"type": "Tool", "tool_id": "email"}, readers="Public")
    return Val(value="sent", caps=out_caps)
