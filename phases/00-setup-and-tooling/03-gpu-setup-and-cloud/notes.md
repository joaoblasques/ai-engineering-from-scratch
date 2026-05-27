# Lesson 03 — notes

## Hardware profile

| Field                          | Intel MacBook (local) | Colab T4 (cloud)              |
|--------------------------------|-----------------------|-------------------------------|
| OS                             | macOS 26.5            | Linux (unobserved — didn't run uname) |
| PyTorch version                | 2.2.2                 | 2.11.0+cu128                  |
| CUDA available                 | False                 | True                          |
| GPU model                      | N/A                   | Tesla T4                      |
| VRAM                           | N/A                   | 15.6 GB                       |
| Compute capability             | N/A                   | 7.5                           |
| CPU matmul time (4000×4000)    | (didn't run)          | 3.4524s                       |
| GPU matmul time (4000×4000)    | (n/a)                 | 0.172s                        |
| Observed speedup               | (n/a)                 | 20×                           |

**Finding:** Intel Mac has no CUDA-capable GPU and is not Apple Silicon (so no MPS either). PyTorch on this machine is CPU-only. All GPU work in this course happens in the cloud, with Colab T4 (free tier) as the primary path.

## fp16 capacity analysis (Llama 3 8B)

Rule of thumb: each fp16 parameter = 2 bytes.

| Scenario                       | Math              | VRAM needed | Fits on T4 (15.6 GB)?           |
|--------------------------------|-------------------|-------------|---------------------------------|
| Inference (weights only)       | 8B × 2 bytes      | ~16 GB      | No — barely (0.4 GB over)       |
| Naive training (~6× weights)   | 16 GB × 6         | ~96 GB      | No — 6× over                    |
| LoRA training (adapter only)   | adapter + frozen base | ~21 GB  | Close — tractable with checkpointing + 8-bit optimizer |

The 6× training multiplier breaks down as: weights + gradients (same size as weights) + optimizer state (Adam = ~4× weights for fp32 momentum/variance) + activations.

LoRA freezes the base model so gradients and optimizer state shrink to the adapter's size (a few million parameters, not billions):

| Component                  | Naive training | LoRA training              |
|----------------------------|----------------|----------------------------|
| Weights (frozen base)      | 16 GB          | 16 GB (loaded, no gradient)|
| Weights (trainable adapter)| —              | ~0.05 GB                   |
| Gradients                  | 16 GB          | ~0.05 GB                   |
| Optimizer state            | 64 GB          | ~0.2 GB                    |
| Activations                | ~5 GB          | ~5 GB                      |
| **Total**                  | **~96 GB**     | **~21 GB**                 |

**Mental model:** LoRA = train a small adapter, not the full model → fine-tuning fits in 10–20× less VRAM. You'll meet LoRA properly in Phase 8.

## Cloud GPU comparison (May 2026)

| Provider     | Cost model                                                                                       | Setup friction                                              | Best for (this course)                                                       | Notable gotcha                                                                                |
|--------------|--------------------------------------------------------------------------------------------------|-------------------------------------------------------------|------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| Google Colab | Free tier; Pro $11.99/mo, Pro+ $49.99/mo; pay-as-you-go $9.99 / 100 CU (~57 hr on T4)            | Zero — opens in browser, no account beyond Google           | Phase 0–5: zero-setup notebooks, free T4 is enough for all early lessons     | 12 hr session cap with 90-min idle disconnect; GPU type not guaranteed; attach can fail at peak |
| Lambda Labs  | Pure on-demand: A100 $1.29/hr, H100 $2.49–$2.99/hr                                               | Medium — account + credit card, launch instance, SSH or Jupyter | Phase 8+: longer fine-tunes or training runs where you need reliability      | No consumer GPUs (no RTX 4090); H100 can sell out at peak; no spot market for most SKUs       |
| RunPod       | On-demand + spot: H100 $2.49/hr on-demand, $1.49/hr spot; RTX 4090 ~$0.34–$0.69/hr               | Medium — container/template-based, slightly more config than Colab | Phase 6+: outgrown Colab's session limits but want cheaper than Lambda       | Community templates vary in quality; spot instances can be preempted mid-run                   |
| Vast.ai      | Peer-to-peer marketplace: RTX 4090 from $0.29/hr; A100 80GB $2.00–3.50/hr on-demand, $1.00–1.80/hr spot | High — shop marketplace by host, SSH into someone's rig | Cost-sensitive experimentation when you can handle failures                  | Variable reliability — may be renting from a home rig with no SLA; security model is "trust the host" |

*Prices as of 2026-05-27. Cloud GPU pricing moves; re-verify before any spend.*

**Operating rules for this course:**

1. **Phases 0–5: stay on free Colab.** T4's 15 GB VRAM is enough; lessons fit comfortably under 90 min of activity.
2. **Phase 8 (fine-tuning) is when this becomes real.** Multi-hour training runs make free Colab painful (disconnects). At that point: either pay $9.99 once for 100 CU (~57 hr T4) or move to RunPod for cheaper A100 time.
3. **Lambda + Vast.ai are end-of-course territory.** Lambda for "real training run, can't babysit." Vast.ai for "comfortable with cloud infra, want to optimize cost."

## Decisions

- **`tensor_op.py` not implemented.** Upstream `gpu_check.py` already covers device-agnostic detection + matmul benchmark. The size-sweep variant was run manually in Phase 4 as an exercise — the learning was in the exercise, not in committed code. Placeholder removed to avoid dead code.

## Open questions

- L01 `code/verify.ts` untracked file — triage at L04 kickoff.
