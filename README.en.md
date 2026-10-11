# wave-quantum

**Frequency-to-correlation encoding of a wave packet — validated on real
superconducting hardware.**

> ψ(t) = A · exp(−γ·t) · cos(2πft + φ)
> A = amplitude · f = frequency · φ = phase · γ = damping (post-processing, NOT a gate)

**Author:** Hope (on Máté Róbert's spine) · **Date:** 2026-10-10/11 ·
**Backends:** IBM `ibm_fez`, `ibm_marrakesh`, `ibm_kingston` (156Q Heron r2)

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

## Results — all 7 completed runs

| Run | Backend | Shots | Layout | Pearson | A (contrast) | χ²_red | σ_sys (binomial) |
|---|---|---|---|---|---|---|---|
| 1 | ibm_fez | 512 | free (3 chains) | 0.873 | 0.498 | 23.99 | 0.197 |
| 2 | ibm_fez | 2048 | free (2 chains) | 0.928 | 0.671 | 100.20 | 0.189 |
| 3 | ibm_fez | 1024 | free (3 chains) | 0.953 | 0.632 | 29.96 | 0.148 |
| 4 | ibm_marrakesh | 1024 | free (4 chains) | **0.992** | **0.756** | 15.33 | 0.096 |
| 6 | ibm_kingston | 1024 | free | **0.988** | **0.760** | 9.84 | 0.075 |
| **7** | ibm_fez | 2048 | **fixed** (107,106,105,108…) | **0.997** | **0.740** | **4.69** | **0.035** |
| **7b** | ibm_fez | 2048 | **fixed** (same as 7) | **0.999** | **0.722** | **2.58** | **0.023** |

> **worst 0.873 · median 0.953 · best 0.999**  
> *This table is NOT a trend — the numbers are backend- and layout-dependent.*

**Raw data:** every run has its own `result_run*.json` file in the repo root.

## Status

| Claim | Grade |
|---|---|
| Theorem (13/13 bands, simulation) | ✅ PROVEN (classical) |
| Channel works on real QPUs | 🔬 PROVEN (hardware) — 7 runs, 3 backends, Pearson 0.87–0.999 |
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