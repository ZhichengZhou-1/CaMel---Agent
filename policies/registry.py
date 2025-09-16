from typing import Callable, List
from policies.email_policy import email_policy


def get_policies() -> List[Callable]:
    return [email_policy]
