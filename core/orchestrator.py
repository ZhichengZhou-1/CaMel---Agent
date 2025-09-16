from typing import Callable, Dict, Any
from core.capabilities import Val, Capability
from core.policy_engine import Decision
from policies.registry import get_policies


class Orchestrator:
    def __init__(self, tools: Dict[str, Callable[..., Val]]):
        self.tools = tools
        self.policies = get_policies()

    def call_tool(self, name: str, **kwargs) -> Val:
        # gather arg capabilities for policy checks
        args_with_caps = {}
        for k, v in kwargs.items():
            if isinstance(v, Val):
                args_with_caps[k] = v
            else:
                # literals are from the user plan
                args_with_caps[k] = Val(
                    value=v,
                    caps=Capability(provenance={"type": "User"}, readers="Public", tags=set()),
                )
        # run policies BEFORE invoking the tool
        for policy in self.policies:
            decision: Decision = policy(name, args_with_caps)
            if not decision.allowed:
                raise PermissionError(f"PolicyDenied: {decision.reason}")
        # execute tool
        if name not in self.tools:
            raise KeyError(f"Unknown tool: {name}")
        out: Val = self.tools[name](**{k: v for k, v in args_with_caps.items()})
        return out
