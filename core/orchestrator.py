from typing import Callable, Dict, Any
from core.capabilities import Val, Capability
from core.policy_engine import Decision
from policies.registry import get_policies


class Orchestrator:
    def __init__(self, tools: Dict[str, Callable[..., Val]]):
        self.tools = tools
        self.policies = get_policies()

    def _wrap_literal(self, v: Any) -> Val:
        if isinstance(v, Val):
            return v
        return Val(
            value=v, caps=Capability(provenance={"type": "User"}, readers="Public", tags=set())
        )

    def call_tool(self, name: str, **kwargs) -> Val:
        # normalize args into Val
        args_with_caps: Dict[str, Val] = {}
        for k, v in kwargs.items():
            args_with_caps[k] = self._wrap_literal(v)

        # run policies
        for policy in self.policies:
            decision: Decision = policy(name, args_with_caps)
            if not decision.allowed:
                raise PermissionError(f"PolicyDenied: {decision.reason}")

        # call tool with Val args
        if name not in self.tools:
            raise KeyError(f"Unknown tool: {name}")
        out: Val = self.tools[name](**args_with_caps)
        # tools already return Val
        return out
