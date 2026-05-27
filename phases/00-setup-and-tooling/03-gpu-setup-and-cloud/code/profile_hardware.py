"""Emit a hardware profile (OS, arch, Python, torch,
accelerator, VRAM if applicable, fp16 capacity estimate) as JSON + MD."""

import argparse
import json
import platform
from datetime import datetime, timezone


def _torch_version() -> str:
    try:
        import torch
        return torch.__version__
    except ImportError:
        return "not installed"


def _detect_accelerator() -> dict:
    try:
        import torch
    except ImportError:
        return {
            "type": "cpu",
            "name": None,
            "vram_gb": None,
            "compute_capability": None,
            "fp16_param_estimate_billions": None,
        }

    if torch.cuda.is_available():
        try:
            name = torch.cuda.get_device_name(0)
            props = torch.cuda.get_device_properties(0)
            vram_gb = round(props.total_memory / 1e9, 2)
            cc = f"{props.major}.{props.minor}"
            fp16 = round(vram_gb / 2, 1)
        except Exception:
            name, vram_gb, cc, fp16 = None, None, None, None
        return {
            "type": "cuda",
            "name": name,
            "vram_gb": vram_gb,
            "compute_capability": cc,
            "fp16_param_estimate_billions": fp16,
        }

    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return {
            "type": "mps",
            "name": "Apple Silicon GPU",
            "vram_gb": None,
            "compute_capability": None,
            "fp16_param_estimate_billions": None,
        }

    if getattr(torch.version, "hip", None) is not None:
        return {
            "type": "rocm",
            "name": None,
            "vram_gb": None,
            "compute_capability": None,
            "fp16_param_estimate_billions": None,
        }

    return {
        "type": "cpu",
        "name": None,
        "vram_gb": None,
        "compute_capability": None,
        "fp16_param_estimate_billions": None,
    }


def build_profile() -> dict:
    return {
        "os": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "python": platform.python_version(),
        "torch": _torch_version(),
        "accelerator": _detect_accelerator(),
        "captured_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def render_md(p: dict) -> str:
    o = p["os"]
    acc = p["accelerator"]
    acc_label = acc["type"].upper() if acc["type"] != "cpu" else "CPU only"
    name = acc["name"] if acc["name"] is not None else "—"
    vram = f"{acc['vram_gb']} GB" if acc["vram_gb"] is not None else "—"
    cc = acc["compute_capability"] if acc["compute_capability"] is not None else "—"
    fp16 = (
        f"~{acc['fp16_param_estimate_billions']}B parameters"
        if acc["fp16_param_estimate_billions"] is not None
        else "—"
    )
    return (
        "## Hardware profile\n\n"
        "| Field | Value |\n"
        "|---|---|\n"
        f"| OS | {o['system']} {o['release']} ({o['machine']}) |\n"
        f"| Python | {p['python']} |\n"
        f"| PyTorch | {p['torch']} |\n"
        f"| Accelerator | {acc_label} |\n"
        f"| Device name | {name} |\n"
        f"| VRAM | {vram} |\n"
        f"| Compute capability | {cc} |\n"
        f"| fp16 capacity estimate | {fp16} |\n\n"
        f"Captured: {p['captured_at']}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Emit a hardware profile as JSON (default) or Markdown (--md)."
    )
    parser.add_argument("--md", action="store_true", help="Output Markdown table")
    args = parser.parse_args()

    p = build_profile()
    print(render_md(p) if args.md else json.dumps(p, indent=2))


if __name__ == "__main__":
    main()
