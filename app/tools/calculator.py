from __future__ import annotations

import ast
import operator
from typing import Any

from .base import ToolSpec
from app.core.permissions import PermissionLevel


_BINOPS: dict[type[ast.operator], Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARYOPS: dict[type[ast.unaryop], Any] = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _evaluate(node: ast.AST) -> float | int:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARYOPS:
        return _UNARYOPS[type(node.op)](_evaluate(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
        left, right = _evaluate(node.left), _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("Exponent is too large.")
        return _BINOPS[type(node.op)](left, right)
    raise ValueError("Only numeric arithmetic is supported.")


class CalculatorTool:
    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="calculator",
            description="Evaluate a numeric arithmetic expression without executing code.",
            parameters={"expression": {"type": "string", "maxLength": 500}},
            permission_level=PermissionLevel.SAFE,
        )

    async def execute(self, *, expression: str) -> str:
        if len(expression) > 500:
            raise ValueError("Expression is too long.")
        tree = ast.parse(expression, mode="eval")
        return str(_evaluate(tree.body))
