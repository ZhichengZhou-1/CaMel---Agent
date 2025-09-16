from core.orchestrator import Orchestrator
from tools.read_cloud_doc import read_cloud_doc
from tools.send_email import send_email
from core.capabilities import Val, Capability

TOOLS = {"read_cloud_doc": read_cloud_doc, "send_email": send_email}

if __name__ == "__main__":
    orch = Orchestrator(TOOLS)
    # PLAN (pretend P-LLM wrote this plan)
    doc = orch.call_tool("read_cloud_doc", doc_id="doc:meeting")
    to = Val(
        value="alice@acme.com",
        caps=Capability(provenance={"type": "User"}, readers="Public", tags=set()),
    )
    subject = Val(
        value="Re: Q3 Budget",
        caps=Capability(provenance={"type": "User"}, readers="Public", tags=set()),
    )
    body = doc  # sending doc text in body (allowed, alice is a reader)
    out = orch.call_tool("send_email", to=to, subject=subject, body=body, attachment=doc)
    print("OK:", out.value)
