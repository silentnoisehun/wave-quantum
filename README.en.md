# wave-quantum

**Frequency-to-correlation encoding of a wave packet — validated on real
superconducting hardware.**

> ψ(t) = A · exp(−γ·t) · cos(2πft + φ)
> A = amplitude · f = frequency · φ = phase · γ = damping (post-processing, NOT a gate)

**Author:** Hope (on Máté Róbert's spine) · **Date:** 2026-10-10/11 ·
**Backends:** IBM `ibm_fez`, `ibm_marrakesh` (156Q Heron r2)

## What this is

The theorem:

```
⟨Z_readout · Z_reservoir⟩ = cos(2π·k/N)      N = 13 bands, X-basis readout
```

A wave packet's frequency is encoded as a band index `k` (RX rotations on 13
reservoir qubits), bridged to a readout qubit with H+CX, and read back as a
**two-qubit ZZ correlation measured in the X basis** — deterministically, in
closed form.

And the paired no-go:

```
the readout qubit's MARGINAL carries zero reservoir information
(CX target-marginal theorem — falsified on hardware: TVD = 0.047, noise floor)
```

The information lives in the correlation, not in the marginals. Both halves
were measured.

## Status

| Claim | Grade |
|---|---|
| Theorem (13/13 bands, simulation) | ✅ PROVEN (classical) |
| Channel works on real QPUs | 🔬 PROVEN (hardware) — 6 runs, 3 backends, Pearson 0.87–0.999 |
| Within-run scatter is layout-originated | 🔬 PROVEN (pre-registered) — σ_sys 0.15–0.19 → 0.023–0.035 |
| New physics | ❌ NOT CLAIMED — the composition is new, the ingredients are textbook |

Best measurement: **Pearson 0.9989, χ²_red 2.58** (fixed layout, 2048 shots,
bit-identical ISA circuits on two independent API keys).

## The falsification chain (the method)

| Version | Claim | Killed by |
|---|---|---|
| v1 | marginal carries frequency | 🔬 hardware: TVD = 0.047 |
| v2 | Z-basis correlation tracks A | ✅ simulation |
| (v3 first guess) | cos(π·k/N) | ✅ simulation: 12/13 bands failed |
| v3 | **cos(2π·k/N)** | — current, ✅ + 🔬 |

Falsified results are preserved as results. The full history — including the
statistical errors caught in review and the pre-registered verdict chain — is
in [CHRONICLE.md](CHRONICLE.md).

## Documents

- **[White paper (EN)](docs/WHITE_PAPER.en.md)** — full paper, scs-quantum
  style: claim markers, all runs written out, caught errors, prior-art table,
  levels of proof.
- **[Chronicle](CHRONICLE.md)** — how we got here, wrong data included.
- **[Pre-registered criteria](REFEREE_STATS.md)** — the layout-verdict
  thresholds, committed to git *before* the decisive runs returned.

## Run it

```bash
# Simulation sweep (no quota) — 13 bands vs theorem
python wave_quantum_v3.py --sweep

# Hardware run — one job, 13 band-circuits batched
python wave_quantum_v3.py --backend ibm_fez --shots 2048 --fixed-layout

# Statistics (binomial sigma everywhere)
python _referee_stats.py
```

Requires `qiskit`, `qiskit-ibm-runtime` ≥ 0.50, an IBM Quantum token.

## Citation

If you use this work, cite the ingredients honestly: parity oscillations
(Sackett et al., Nature 404, 256 (2000)), the Fourier structure of encoded
parameters (Schuld, Sweke, Meyer, arXiv:2008.08605), and QRC on superconducting
hardware (Suzuki arXiv:2107.05808, Chen arXiv:2001.09498). The composition and
the no-go pairing are what this repo adds.
