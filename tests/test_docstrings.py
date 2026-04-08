import ast
from pathlib import Path


def test_all_source_modules_have_docstrings():
    missing = []
    for path in sorted(Path("src/newsdom_api").glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        if not ast.get_docstring(tree):
            missing.append(f"module:{path}")
        for node in tree.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                if not ast.get_docstring(node):
                    missing.append(f"{path}:{node.lineno}:{node.name}")
    assert not missing, missing
