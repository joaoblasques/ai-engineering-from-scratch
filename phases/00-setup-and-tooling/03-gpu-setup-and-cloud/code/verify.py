"""L03 cumulative env check (CPU/CUDA/MPS aware)."""

import sys
import os
import importlib.util


def _load_verify(unique_name, rel_path):
    # Use a unique module name so `from verify import` inside L02's verify.py
    # doesn't collide with the partially-initialised 'verify' module when
    # this file is itself being imported (rather than run as __main__).
    abs_path = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), rel_path)
    )
    spec = importlib.util.spec_from_file_location(unique_name, abs_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[unique_name] = mod
    spec.loader.exec_module(mod)
    return mod


_l02 = _load_verify("l02_verify", "../../02-git-and-collaboration/code/verify.py")

L01_CHECKS = _l02.L01_CHECKS
L02_CHECKS = _l02.L02_CHECKS
L02_WARN_CHECKS = _l02.L02_WARN_CHECKS
GPU_CHECKS = _l02.GPU_CHECKS
run_check = _l02.run_check
run_warn_check = _l02.run_warn_check


def _torch_version_ok() -> bool:
    try:
        import torch
        major, minor = (int(x) for x in torch.__version__.split(".")[:2])
        return (major, minor) >= (2, 2)
    except Exception:
        return False


def _torch_version_str() -> str:
    try:
        import torch
        return torch.__version__
    except Exception:
        return "not installed"


def _any_accelerator() -> bool:
    try:
        import torch
        if torch.cuda.is_available():
            return True
        if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            return True
        if getattr(torch.version, "hip", None) is not None:
            return True
        return False
    except Exception:
        return False


def _accelerator_label() -> str:
    try:
        import torch
        if torch.cuda.is_available():
            return f"CUDA — {torch.cuda.get_device_name(0)}"
        if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            return "MPS — Apple Silicon"
        if getattr(torch.version, "hip", None) is not None:
            return f"ROCm {torch.version.hip}"
        return "CPU only — use Colab for GPU lessons"
    except Exception:
        return "torch not installed"


L03_CHECKS = [
    ("PyTorch >= 2.2", _torch_version_ok, _torch_version_str),
]

L03_WARN_CHECKS = [
    ("Local accelerator", _any_accelerator, _accelerator_label),
]


def main():
    print("\n=== AI Engineering from Scratch — Environment Check ===")
    print("    (cumulative through Phase 00 / Lesson 03)\n")

    print("Lesson 01 — Dev Environment:")
    l01_passed = sum(run_check(n, f, d) for n, f, d in L01_CHECKS)
    l01_total = len(L01_CHECKS)

    print("\nGPU (optional, L01 baseline):")
    gpu_passed = sum(run_check(n, f, d) for n, f, d in GPU_CHECKS)
    gpu_total = len(GPU_CHECKS)

    print("\nLesson 02 — Git & Collaboration:")
    l02_passed = sum(run_check(n, f, d) for n, f, d in L02_CHECKS)
    l02_total = len(L02_CHECKS)

    print("\nLesson 02 — Git identity (warnings, not gating):")
    for item in L02_WARN_CHECKS:
        run_warn_check(*item)

    print("\nLesson 03 — GPU Setup & Cloud:")
    l03_passed = sum(run_check(n, f, d) for n, f, d in L03_CHECKS)
    l03_total = len(L03_CHECKS)

    print("\nLesson 03 — Accelerator profile (informational, not gating):")
    for item in L03_WARN_CHECKS:
        run_warn_check(*item)

    total_passed = l01_passed + l02_passed + l03_passed
    total = l01_total + l02_total + l03_total

    print(f"\nResult: {total_passed}/{total} core checks passed", end="")
    if gpu_passed > 0:
        print(f", {gpu_passed}/{gpu_total} GPU checks passed")
    else:
        print(" (no GPU — that's fine, most lessons work on CPU)")

    if total_passed == total:
        print("\nYou're ready for Lesson 04.\n")
    else:
        print("\nFix the failed checks above, then run this script again.\n")

    return 0 if total_passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
