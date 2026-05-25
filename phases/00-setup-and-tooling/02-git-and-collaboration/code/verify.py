import sys
import os
import shutil
import subprocess

# Cumulative: pull in all Lesson 01 checks so this script covers the full
# Phase 00 stack up through Lesson 02.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../01-dev-environment/code"))
from verify import CHECKS as L01_CHECKS, GPU_CHECKS, run_check


def _git_config(key: str) -> str:
    r = subprocess.run(["git", "config", "--global", key], capture_output=True, text=True)
    return r.stdout.strip()


def _repo_gitignore_has_ml_patterns() -> bool:
    # Walk up from CWD to find the nearest .gitignore (repo root wins).
    path = os.path.abspath(".")
    while True:
        candidate = os.path.join(path, ".gitignore")
        if os.path.exists(candidate):
            text = open(candidate).read()
            return all(pat in text for pat in ("*.pt", "*.pth", "*.safetensors"))
        parent = os.path.dirname(path)
        if parent == path:
            return False
        path = parent


L02_CHECKS = [
    ("Git", lambda: shutil.which("git") is not None, None),
    (".gitignore covers ML checkpoints (.pt / .pth / .safetensors)",
     _repo_gitignore_has_ml_patterns, None),
]

# WARN checks: print [WARN] but do not gate the exit code.
L02_WARN_CHECKS = [
    ("git user.name",
     lambda: bool(_git_config("user.name")),
     lambda: _git_config("user.name") or
             "not set — fix: git config --global user.name 'Your Name'"),
    ("git user.email",
     lambda: bool(_git_config("user.email")),
     lambda: _git_config("user.email") or
             "not set — fix: git config --global user.email 'you@example.com'"),
]


def run_warn_check(name, check_fn, detail_fn=None):
    try:
        ok = check_fn()
        detail_val = detail_fn() if callable(detail_fn) else (detail_fn or "")
        detail = f" ({detail_val})" if detail_val else ""
        if ok:
            print(f"  [PASS] {name}{detail}")
        else:
            print(f"  [WARN] {name} — {detail_val}")
    except Exception as exc:
        print(f"  [WARN] {name} — {exc}")


def main():
    print("\n=== AI Engineering from Scratch — Environment Check ===")
    print("    (cumulative through Phase 00 / Lesson 02)\n")

    print("Lesson 01 — Dev Environment:")
    l01_passed = sum(run_check(n, f, d) for n, f, d in L01_CHECKS)
    l01_total = len(L01_CHECKS)

    print("\nGPU (optional):")
    gpu_passed = sum(run_check(n, f, d) for n, f, d in GPU_CHECKS)
    gpu_total = len(GPU_CHECKS)

    print("\nLesson 02 — Git & Collaboration:")
    l02_passed = sum(run_check(n, f, d) for n, f, d in L02_CHECKS)
    l02_total = len(L02_CHECKS)

    print("\nLesson 02 — Git identity (warnings, not gating):")
    for item in L02_WARN_CHECKS:
        run_warn_check(*item)

    total_passed = l01_passed + l02_passed
    total = l01_total + l02_total

    print(f"\nResult: {total_passed}/{total} core checks passed", end="")
    if gpu_passed > 0:
        print(f", {gpu_passed}/{gpu_total} GPU checks passed")
    else:
        print(" (no GPU — that's fine, most lessons work on CPU)")

    if total_passed == total:
        print("\nYou're ready for Lesson 03.\n")
    else:
        print("\nFix the failed checks above, then run this script again.\n")

    return 0 if total_passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
