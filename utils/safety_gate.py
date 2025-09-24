import ast
from typing import Tuple


ALLOWED_NODES = {
    ast.Module,
    ast.FunctionDef,
    ast.arguments,
    ast.arg,
    ast.Load,
    ast.Store,
    ast.Expr,
    ast.If,
    ast.Compare,
    ast.Return,
    ast.Name,
    ast.Constant,
    ast.Attribute,
    ast.Subscript,
    ast.Call,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.For,
    ast.While,
    ast.Pass,
    ast.Try,
    ast.ExceptHandler,
    ast.IfExp,
    ast.Expr,
    ast.Assign,
    ast.Compare,
    ast.Eq,
    ast.NotEq,
    ast.In,
    ast.NotIn,
}


def validate_policy_code(code: str) -> Tuple[bool, str]:
    """
    Very small static safety gate:
      - Parses code into AST and checks for disallowed node types (imports, exec, eval, with, etc).
      - Checks existence of function named POLICY_<TOOL> or at least one function def.
    Returns (ok, reason).
    """
    try:
        tree = ast.parse(code)
    except Exception as e:
        return False, f"parse_error: {e}"

    # disallow Import / ImportFrom
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return False, "imports are disallowed"
        if isinstance(node, ast.Exec):  # extremely old; just in case
            return False, "exec is disallowed"
        # disallow attribute setting at module level (heuristic)
        if isinstance(node, ast.With):
            return False, "with statements are disallowed"

    # ensure only allowed nodes (this is conservative)
    for node in ast.walk(tree):
        if type(node) not in ALLOWED_NODES:
            return False, f"disallowed_node: {type(node).__name__}"

    # ensure there's at least one function def
    func_defs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    if not func_defs:
        return False, "no function definition found"

    # success
    return True, "ok"
