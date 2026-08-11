"""Run Plot Foundation and consumer adapter compatibility checks."""

from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
WORK_ROOT = ROOT.parent
FORBIDDEN_IMPORTS = {
    "core",
    "eigenmode_analysis",
    "jpype",
    "mph",
    "pandas",
    "research_agent_workbench",
}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--myplots",
        type=Path,
        default=WORK_ROOT / ".worktrees" / "myPlots-eigenmode-analysis",
    )
    parser.add_argument(
        "--workbench",
        type=Path,
        default=WORK_ROOT / ".worktrees" / "research-agent-workbench-eigenmode-analysis",
    )
    parser.add_argument(
        "--python-a",
        type=Path,
        default=WORK_ROOT / "myPlots" / ".venv" / "Scripts" / "python.exe",
    )
    parser.add_argument(
        "--python-b",
        type=Path,
        default=WORK_ROOT / "research-agent-workbench" / ".venv" / "Scripts" / "python.exe",
    )
    parser.add_argument(
        "--eigenmode",
        type=Path,
        default=WORK_ROOT / "eigenmode-analysis",
    )
    return parser


def _scan_dependency_boundary() -> None:
    violations = []
    for path in (ROOT / "src" / "plot_foundation").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                root_name = name.split(".", 1)[0]
                if root_name in FORBIDDEN_IMPORTS:
                    violations.append(f"{path}:{node.lineno}: {name}")
    if violations:
        raise SystemExit(
            "Plot Foundation dependency violations:\n" + "\n".join(violations)
        )
    print("[dependency-boundary] no forbidden imports")


def _run(label: str, python: Path, cwd: Path, args: list[str], paths: list[Path]):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONPATH"] = os.pathsep.join(str(path) for path in paths)
    command = [str(python), "-m", "pytest", *args]
    print(f"\n[{label}]\n{' '.join(command)}")
    subprocess.run(command, cwd=cwd, env=env, check=True)


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    _scan_dependency_boundary()
    plot_src = ROOT / "src"
    eigenmode_src = args.eigenmode.resolve() / "src"
    _run("package-a", args.python_a, ROOT, ["-q"], [plot_src])
    _run("package-b", args.python_b, ROOT, ["-q"], [plot_src])
    _run(
        "myplots-adapter",
        args.python_a,
        args.myplots,
        ["-q", "shared_tests/test_shared_plotting_adapter.py"],
        [plot_src, eigenmode_src],
    )
    _run(
        "workbench-adapter",
        args.python_b,
        args.workbench,
        ["-q", "tests/test_shared_band_plotting.py"],
        [plot_src, eigenmode_src, args.workbench.resolve() / "src"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

