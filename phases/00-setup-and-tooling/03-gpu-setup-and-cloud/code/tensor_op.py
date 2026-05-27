"""Device-agnostic matmul + reduction benchmark.
Resolves device as cuda → mps → cpu; designed to run identically
locally (CPU on this Intel Mac) and in Colab (CUDA on T4)."""
