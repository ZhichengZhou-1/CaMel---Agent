from core.orchestrator import Orchestrator
from tools.read_cloud_doc import read_cloud_doc
from tools.send_email import send_email
from core.capabilities import Val, Capability

TOOLS = {"read_cloud_doc": read_cloud_doc, "send_email": send_email}


def main():
    orch = Orchestrator(TOOLS)

    # P-LLM plan simulated by hand:
    doc_id = Val(
        value="doc:meeting", caps=Capability(provenance={"type": "User"}, readers="Public")
    )
    doc = orch.call_tool("read_cloud_doc", doc_id=doc_id)

    to = Val(value="alice@acme.com", caps=Capability(provenance={"type": "User"}, readers="Public"))
    subject = Val(
        value="Re: Q3 Budget", caps=Capability(provenance={"type": "User"}, readers="Public")
    )

    out = orch.call_tool("send_email", to=to, subject=subject, body=doc, attachment=doc)
    print("OK:", out.value)


if __name__ == "__main__":
    main()
