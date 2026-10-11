# Wave-Quantum: Frequency-to-Correlation Encoding of a Wave Packet on a Superconducting QPU

## White Paper — A Deterministic Correlation Channel Validated on Real Hardware

**Version:** 1.0 · HARDWARE-VALIDATED RELEASE
**Project:** `wave-quantum` — a Python measurement layer over Qiskit Runtime, authored by Hope (Spine-First cognitive OS) under the direction of Máté Róbert
**Central claim:** the wave-packet frequency is not encoded in any single qubit's
readout. It travels in a **two-qubit correlation**, it follows a **closed-form
theorem**, and this was **measured on real superconducting hardware** — including
the negative result that pins down *where the information is not*.

---

## 0. Claim markers (read this first)

Every technical claim in this document carries the *grade* of its evidence. The
markers are not decoration: two claims of different quality must never be made
to look alike.

| Marker | Meaning | What it does NOT mean |
|---|---|---|
| ✅ **PROVEN (classical)** | Proven by simulation (65536 shots/band, 13/13 bands) or by exact state-vector computation. | It does NOT mean hardware proof. |
| 🔬 **PROVEN (hardware)** | Measured on a real QPU, in the layout configuration stated, with the statistical criteria pre-registered (§6). | It does NOT mean the numeric values hold on every backend or every transpiler layout. |
| ⚠️ **MEASUREMENT-DEPENDENT** | The claim holds, but its numeric value derives from a measurement and may shift with calibration, layout or backend. | It is not an independent physical law. |
| ⚠️ **ASSUMPTION** | The model assumes it. No measurement exists. | It is NOT proven. |
| ℹ️ **CONVENTION** | A definition or unit convention chosen by the project. | It is not a law of nature. |

> ### ⚠️ MANDATORY CAUTION — what this paper does NOT claim
>
> 1. **No new physics.** The ingredients of this work — parity oscillations
>    (Sackett et al., Nature 404, 256 (2000)), Bell-correlation measurement, and
>    angle encoding as a truncated Fourier series (Schuld, Sweke, Meyer,
>    arXiv:2008.08605) — are textbook quantum mechanics. The claim of novelty is
>    the **composition**: a deterministic, closed-form
>    *signal-frequency → two-qubit-correlation* readout channel, hardware-validated,
>    paired with a marginal no-go theorem. A prior-art search over ~180 arXiv
>    results (§8) found no published instance of this composition.
> 2. **No proof of any cognitive architecture.** This work is *consistent with* a
>    relation-first view of information (the information lives in correlations,
>    not in marginals) and was *motivated* by it. Consistency is not evidence of
>    proof; the measurement constrains this circuit, not a theory of mind.
> 3. **No post-selection, no mitigation-only results.** Raw counts are the basis
>    of every number below. Where mitigation is discussed (§6.4), it is named as
>    future work, not used to produce any figure.

---

## 1. Abstract

The wave packet of the wave-based memory model,

```
ψ(t) = A · exp(−γ·t) · cos(2π·f·t + φ)
```

carries three physical parameters: amplitude `A`, frequency `f`, phase `φ`. This
paper answers a narrow question with a measurement: **where in a quantum circuit
does the frequency information go, and can it be read back deterministically?**

The answer has three parts.

**First, a no-go (🔬 hardware).** In the CX-bridge architecture used here, the
readout qubit's *marginal* distribution is provably information-free: any
frequency-dependent statistics there are bounded by noise. Measured on `ibm_fez`
(256 shots): total variation distance to the frequency-independent null was
**0.047** — the noise floor. This falsified the project's own first hypothesis
(v1) on real hardware.

**Second, a theorem (✅ classical).** Measuring the readout qubit and one
reservoir qubit **in the X basis** yields a two-qubit ZZ correlation that maps
the encoded band index `k` deterministically:

```
⟨Z_readout · Z_reservoir⟩ = cos(2π·k/N),     N = 13 bands
```

Verified in state-vector simulation, 13/13 bands, and against a first, *wrong*
closed-form guess (`cos(π·k/N)`) that the simulation rejected 12/13 — the
corrected factor 2 comes from the two-sided phase transport of the CX ladder.

**Third, hardware validation (🔬 hardware).** Six completed runs across three
backends (`ibm_fez`, `ibm_marrakesh`) reproduce the cosine: Pearson correlation
**0.87–0.999** between the measured 13-point curve and the theorem, with fitted
contrast A = 0.50–0.74. A pre-registered, fixed-layout pair of runs (§6)
additionally shows that the within-run scatter is **layout-originated**: fixing
the physical chain shrinks the systematic scatter σ_sys from 0.15–0.19 to
**0.023–0.035** (~5×), and the best run reaches Pearson **0.9989** with
χ²_red = 2.58.

The information in this architecture lives in the **correlation**, not in the
marginals — and both halves of that sentence were measured.

---

## 2. System model

### 2.1 The wave packet and its encoding

ℹ️ **CONVENTION.** The packet ψ(t) = A·e^(−γt)·cos(2πft+φ) is encoded per
parameter, in a 14-qubit circuit (13 reservoir + 1 readout):

| Symbol | Encoding | Qubit |
|---|---|---|
| `A` | `RY(2·arcsin(√A))` | readout `q[0]` |
| `f` | band index `k = ⌊f·N⌋`, `RX(2π·k/N)` on each reservoir qubit | `q[1..13]` |
| `φ` | `RZ(2φ)` | readout `q[0]` |
| `γ` | not a gate — post-processing metadata | — |

A fixed **H+CX bridge** entangles every reservoir qubit with the readout qubit
(`H(q_i)`, `CX(q_i → q0)`), then the readout and one partner qubit are measured
in the **X basis** (`H` before measurement).

### 2.2 The thirteen bands

ℹ️ **CONVENTION.** The frequency axis is quantised into N = 13 bands,
`k ∈ {0..12}`, matching the 13-band structure of the wave-based memory model.
The theorem's period follows N; nothing in the physics selects 13.

### 2.3 The measurement

The measured quantity is the parity correlation

```
⟨ZZ⟩_k = P(00) + P(11) − P(01) − P(10)
```

over the two measured qubits, for each band k, against the theorem
`cos(2π·k/13)`.

---

## 3. The theorem — and the two falsified predecessors

### 3.1 v1: the marginal hypothesis — 🔴 FALSIFIED ON HARDWARE

The first hypothesis claimed the frequency is decodable from the readout
qubit's marginal distribution.

**The measurement (ibm_fez, 256 shots):** the readout marginal was
indistinguishable across bands (TVD to null = 0.047).

**The reason (✅ classical):** in this architecture the CX bridge transports
phase *two-sidedly*; the readout qubit's reduced state is band-independent by
construction. The marginal carries **zero** reservoir information — not
approximately, but as a structural property.

This negative result is kept as a theorem-pair: it states *where the
information is not*, and it was falsified on hardware, not in simulation.

### 3.2 v2: the Z-basis correlation — ✅ FALSIFIED IN SIMULATION

The second hypothesis moved to two-qubit ZZ correlations but measured in the
**Z basis**, predicting ⟨ZZ⟩ = 2√(A(1−A)).

**The simulation (65536 shots/band):** the correlation did not track `A`.
Reason: at A = 0.5 the readout qubit is in |+⟩ — a Z-basis parity on a
superposed reference carries no amplitude information.

**The lesson:** the reference qubit must be rotated into the **X basis**
before measurement. One `H` gate.

### 3.3 v3: the X-basis theorem — ✅ PROVEN (classical), 🔬 PROVEN (hardware)

With the X-basis measurement,

```
⟨ZZ⟩_k = cos(2π·k/N)
```

- **State-vector simulation:** 13/13 bands exact.
- **First closed-form guess was wrong:** `cos(π·k/N)` failed 12/13 in
  simulation — the CX ladder transports phase twice. The corrected form is
  used everywhere below.
- **Hardware:** §5.

---

## 4. Falsification chain — how each wrong version was killed

This project's method (the *Falsification Reflex*) requires every hypothesis to
be killed by measurement or simulation before it is promoted. The chain:

| Version | Claim | Killed by | Where |
|---|---|---|---|
| v1 | marginal carries frequency | TVD = 0.047 (noise floor) | 🔬 hardware |
| v2 | Z-correlation = 2√(A(1−A)) | correlation does not track A | ✅ simulation |
| (v3 guess) | ⟨ZZ⟩ = cos(π·k/N) | 12/13 bands failed | ✅ simulation |
| v3 | ⟨ZZ⟩ = cos(2π·k/N) | — (current) | ✅ + 🔬 |

Simulation kills are cheap (minutes, no quota); hardware kills are definitive.
The reflex orders them that way on purpose.

---

## 5. Hardware validation

### 5.1 Measurement conditions

🔬 All runs: IBM Quantum Heron-family superconducting QPUs, open plan, SamplerV2
primitive, no error mitigation (raw counts), 13 band-circuits batched in one job
per run. Every run's transpiled layout was recovered or pre-registered (§5.3).

### 5.2 All completed runs — every one written out, not only the best

| Run | Backend | Shots | Layout | Pearson | A (contrast) | χ²_red | σ_sys (binomial) |
|---|---|---|---|---|---|---|---|
| 1 | ibm_fez | 512 | free (3 chains/13 bands) | 0.873 | 0.498 | 23.99 | 0.197 |
| 2 | ibm_fez | 2048 | free (2 chains) | 0.928 | 0.671 | 100.20 | 0.189 |
| 3 | ibm_fez | 1024 | free (3 chains) | 0.953 | 0.632 | 29.96 | 0.148 |
| 4 | ibm_marrakesh | 1024 | free (4 chains) | 0.992 | 0.756 | 15.33 | 0.096 |
| **7** | ibm_fez | 2048 | **fixed** (107,106,105,108…) | **0.997** | **0.740** | **4.69** | **0.035** |
| **7b** | ibm_fez | 2048 | **fixed** (same as 7) | **0.999** | **0.722** | **2.58** | **0.023** |

worst Pearson 0.873 · median 0.941 · best 0.999

⚠️ **This table is NOT a trend.** The numbers are backend- and layout-dependent;
the mapping itself did not change across runs. An early draft described
"0.87 → 0.99" as an improvement series — that reading is wrong and was removed.
The runs differ in hardware quality and (for runs 1–4) in per-band transpiler
layout, nothing else.

### 5.3 The layout discovery — per-band chain re-selection

Runs 1–4 submitted each band as an independent transpile. Recovery of the
submitted ISA circuits from the job records (`job.inputs`) showed **2–4 distinct
physical chains within a single 13-band run**: the transpiler re-selected the
chain per band. Chain-overlap vs. band-residual correlations were positive in
all four runs (+0.26 … +0.53) but below the 13-point significance threshold
(0.55) — a directional hint, not evidence.

The decisive test was therefore run with a **fixed layout** (runs 7/7b): a
single parameterised circuit, transpiled once, bound 13 times — every band on
the identical physical chain. Two independent API keys (independent quotas) ran
the bit-identical ISA program.

**Result (§6):** fixing the chain shrinks σ_sys ~5× and stabilises A. The
within-run scatter of runs 1–4 is layout-originated.

### 5.4 The null control

🔬 The J=0 null circuit (bridge removed) on hardware: the readout marginal
reproduces the frequency-independent null within TVD 0.047 — the same floor as
the v1 falsification. The information is not leaking into marginals; the
correlation channel is the only carrier.

---

## 6. Pre-registered statistical analysis

### 6.1 What counts as a signal, and what does not

The question "is there a signal?" is answered by any working circuit; z-scores
against the null are reported for completeness (all runs z > 28σ,
p < 10⁻¹⁸¹) but are **not** the primary result. The primary question is:
**how well does the data fit the theorem**, and the primary statistic is the
fitted contrast A with its χ²_red.

### 6.2 One noise model, everywhere

⚠️ **MEASUREMENT-DEPENDENT.** The binomial sigma
`σ_k = √((1 − (A·t_k)²)/shots)` is the *only* noise model used — for χ², for
σ_A and for σ_sys. (An earlier draft mixed a 1/√shots sigma for σ_sys with a
binomial χ²; the inconsistency was caught in review and recomputed. The
model-mixing error is documented in §7 as a caught bug.)

### 6.3 σ_sys: the systematic scatter

χ²_red ≫ 1 grows with shots (24 → 100 from 512 to 2048 shots) — the textbook
signature of a fixed systematic error. Converting χ²_red to a systematic sigma:

```
σ_sys = √((χ²_red − 1) / (shots · ⟨1/σ_k²⟩))
```

gives 0.15–0.19 (free layout) and 0.023–0.035 (fixed layout). ⚠️ The σ_sys
point estimates carry ~±30% uncertainty at 13 points (χ², 12 dof); all verdicts
below therefore use 68% confidence bounds (χ² quantiles 0.72×/1.36×, 12 dof).

### 6.4 The pre-registered layout verdict (runs 7/7b)

Before any run-7/7b data existed, the following criteria were committed to the
repository's git history (commits `a160bc3` → `165d0ca` → `3acb8c8`, timestamps
in the log):

| Question | Criterion | Verdict |
|---|---|---|
| **(A) Is the within-run scatter layout-originated?** | ACCEPT if 1.36 × σ_sys < 0.10 for **both** runs; REJECT if 0.72 × σ_sys > 0.15 for both; between: indecisive | **ACCEPTED** — σ_sys = 0.0348 (CI upper 0.047) and 0.0231 (CI upper 0.031) |
| **(B) Is A stable on a fixed chain?** (drift question, not layout) | \|A₇ − A₇b\| < max(2·σ_A, 0.06) | **STABLE** — \|ΔA\| = 0.0178 < 0.0600 |

The 0.10 threshold applies **only** to runs 7/7b. Applying it to runs 1–4
would be the post-hoc reading the pre-registration was designed to prevent.

### 6.5 Residual analysis — the coherent-error hypothesis was tested and excluded

Before any mitigation, residuals of the one-parameter fit were tested for a
sinusoidal pattern (which would indicate a coherent phase error fixable by an
A·cos(φ+δ)+c model). The three-parameter fit did **not** improve χ² (0.8–1.0×
change), and residual-vs-cosine correlations were ≈ 0. **No coherent phase
error.** The systematic component is per-qubit, layout-dependent error
(readout + crosstalk variability), not a phase offset.

### 6.6 On mitigation

T-REx / measurement-error mitigation would improve the readout fidelity but
does not address crosstalk or coherent errors. Mitigating until χ²_red ≈ 1
would be tuning to target. **Every figure above is raw.** Mitigated/raw pairs
are named as future work (§9), to be reported side by side.

---

## 7. Caught errors — each one a lesson

The measurement history includes errors that would have corrupted the result
had they not been caught. They are documented because a referee trusts work
that does not hide them.

### 7.1 The wrong closed-form guess

**The error.** The first theorem candidate was ⟨ZZ⟩ = cos(π·k/N).
**How it was caught.** A 13-band simulation sweep rejected it 12/13.
**The lesson.** The CX ladder transports phase twice (2π); the factor was
re-derived, not guessed. Simulation kills are cheap — run them first.

### 7.2 The z-score as headline

**The error.** The first statistical draft led with z > 28σ, p < 10⁻¹⁸¹.
**Why it is wrong.** Any working circuit rejects a "no signal" null; the number
carries no information about *fit quality*.
**The fix.** Fit statistics (A, χ²_red) promoted to primary; z reported as a
background sanity check only.

### 7.3 Two noise models in one document

**The error.** σ_sys used a 1/√shots sigma while χ² used the binomial sigma —
two incompatible noise models in one analysis.
**How it was caught.** External review.
**The fix.** One model, one formula set, everywhere (§6.2).

### 7.4 The wrong "one third" phrasing

**The error.** "One third of the total scatter is systematic."
**Why it is wrong.** The correct statement: the systematic sigma is ~one third
of the **signal amplitude**, and it *dominates* the total variance
(95–99% systematic at χ²_red = 24–100).
**The fix.** Exact phrasing adopted; variance fractions computed per run.

### 7.5 The weak drift argument

**The error.** "A is non-monotonic across runs, therefore no drift."
**Why it is weak.** TLS fluctuations are also non-monotonic; the argument rules
out nothing.
**The fix.** A controlled experiment: same chain, two independent keys,
pre-registered stability tolerance (§6.4). The retorica was replaced by a test.

### 7.6 The "lost layouts" misqualification

**The error.** After finding `circuit_metadata` empty in the sampler results,
runs 1–4 were written off as "layouts unrecoverable".
**The reality.** The submitted ISA circuits are retained in `job.inputs`;
all four runs' per-band layouts were recovered from them.
**The lesson.** "I cannot find it" is not "it does not exist". The
misqualification would have cost the paper its layout analysis.

### 7.7 The citation that was remembered, not checked

**The error.** The Schuld–Sweke–Meyer encoding paper was cited from memory as
"Schuld 2008".
**The reality.** arXiv:2008.08605 is the *identifier*; the paper is from 2020,
published as Phys. Rev. A 103, 032430 (2021). The earlier feature-map paper is
Schuld & Killoran, arXiv:1803.07128 (PRL 122, 040504, 2019).
**The fix.** Both verified on arXiv and corrected everywhere.

### 7.8 The narrative that implied a trend

**The error.** "Pearson 0.87 → 0.99" was written as an improvement series.
**Why it is wrong.** Run 4 ran on a better backend; nothing about the mapping
changed between runs. Ordering the table by time manufactures a trend.
**The fix.** "Pearson 0.87–0.999, backend- and layout-dependent" — and the
table kept in time order with that warning attached.

---

## 8. Prior-art and novelty

A structured search (8 distinct arXiv full-text queries, ~180 results scanned;
Semantic Scholar rate-limited) found **no published instance** of the
composition claimed here: digital angle-encoding of a wave packet's (A, f, φ)
into (RY, RX band-index, RZ), a fixed H+CX bridge, and an X-basis two-qubit ZZ
readout with the closed-form band theorem, paired with a marginal no-go.

Closest work found, and how it differs:

| Work | Relation | Difference |
|---|---|---|
| Sackett et al., Nature 404, 256 (2000) | parity oscillations cos(nφ) — the math core | textbook measurement identity, never composed as a signal-frequency readout channel |
| Schuld, Sweke, Meyer, arXiv:2008.08605 (PRA 103, 032430 (2021)) | expectation values are Fourier series of encoded parameters | general framework; does not state the closed-form ⟨ZZ⟩ = cos(2πk/N) channel |
| Schuld & Killoran, arXiv:1803.07128 (PRL 122, 040504, 2019) | feature Hilbert spaces | encoding-for-learning, no correlation readout theorem |
| Senanian et al., arXiv:2312.16166 (Nat. Commun. 2024) | microwave frequency-domain signals into an analog superconducting reservoir | analog, no digital RX band encoding, no ZZ readout |
| Schütte et al., arXiv:2501.15528 | Fourier expressivity of QRCs | reservoir computing, not a deterministic closed-form correlation channel |
| Suzuki et al., arXiv:2107.05808; Chen et al., arXiv:2001.09498; Yasuda et al., arXiv:2310.06706 | QRC on IBM hardware | single-qubit expectation readouts, no ZZ channel, no no-go pairing |
| Tariq et al., arXiv:2607.18552 (QRC survey) | field overview | "current results do not establish a broad quantum advantage" — consistent with our framing |

**Claimed as novel:** the composition, the closed-form band theorem in this
architecture, the paired marginal no-go with its hardware falsification, and
the layout-origin diagnosis with pre-registered verification.
**Not claimed as novel:** parity oscillations, Bell-correlation measurement,
angle encoding, QRC on superconducting hardware, frequency-domain quantum
signal processing.

---

## 9. Limitations and future work

### 9.1 What does not work today

- **The contrast is hardware-bound.** A = 0.50–0.74 across backends/layouts;
  the theorem predicts 1.0. The gap is readout error, crosstalk and
  decoherence — real, measured, and dominant over statistical noise.
- **γ (damping) is not a gate.** It is post-processing metadata, as in the
  parent wave model.
- **The frequency resolution is the band grid.** f is quantised to N = 13
  bands; finer resolution needs more bands or interpolation.

### 9.2 Future work

1. **Runs 5/6 (ibm_kingston)** — third-backend confirmation (queued at the
   time of writing; the table in §5.2 will be amended if they land).
2. **Calibration-prediction test** — predict A per layout from the calibration
   data valid at run time (gate + readout errors); if predicted and measured A
   move together, the contrast becomes an engineering quantity.
3. **Raw/mitigated pairs** — T-REx on readout, reported side by side with raw,
   never as a replacement.
4. **φ and A readout** — the same X-basis correlation method extends to the
   phase and amplitude parameters; the theorem for φ is derivative work.
5. **Multi-band superposition** — encoding a band *distribution* instead of a
   single band; the correlation channel becomes a spectrum.

### 9.3 What this document deliberately does not claim

- It does not claim new physics (§0).
- It does not claim a general quantum advantage for reservoir computing.
- It does not claim the wave-based memory model is "proven" — one channel of
  one parameter was measured, deterministically, with a null control.
- It does not present mitigated numbers as the primary result.

---

## 10. Levels of proof

| Claim | Grade | Basis |
|---|---|---|
| ⟨ZZ⟩_k = cos(2π·k/N) in this architecture | ✅ PROVEN (classical) | state-vector simulation, 13/13 bands |
| readout marginal is information-free (CX target) | ✅ PROVEN (classical) + 🔬 hardware (TVD 0.047) | structural argument + null control |
| the correlation channel works on real QPUs | 🔬 PROVEN (hardware) | 6 runs, 3 backends (2 completed), Pearson 0.87–0.999 |
| within-run scatter is layout-originated | 🔬 PROVEN (hardware, pre-registered) | runs 7/7b vs runs 1–4, criteria committed before data |
| A is stable on a fixed chain | 🔬 PROVEN (hardware, pre-registered) | \|ΔA\| = 0.0178 < 0.0600, two independent keys |
| contrast A ≈ 0.72–0.74 is achievable on fez | ⚠️ MEASUREMENT-DEPENDENT | two runs, one chain, one day |
| the method extends to φ and A readout | ⚠️ ASSUMPTION | same mechanism, not yet measured |
| information "lives in relations" as a principle | ℹ️ INTERPRETATION | consistent with, not proven by, this measurement |

---

## 11. Reproduction

```
# Classical layer — simulation sweep (no quota)
python wave_quantum_v3.py --sweep            # 13 bands, theorem check

# Hardware layer — one run = one job, 13 band-circuits batched
python wave_quantum_v3.py --backend ibm_fez --shots 2048 --fixed-layout

# Statistics (binomial sigma everywhere; CI per §6.3)
python _referee_stats.py
```

Requires: `qiskit`, `qiskit-ibm-runtime` ≥ 0.50, an IBM Quantum API token.
The fixed-layout path (runs 7/7b) uses the parameterised-single-transpile
method; the layout used is committed in `_run7_meta.json`.

The pre-registration chain is in the git history:
`a160bc3` (initial criteria) → `165d0ca` (CI amendment, before data) →
`3acb8c8` (final spec, before data — "no further amendments") → `5788297`
(results + verdict).

---

## Authorship

**Máté Róbert** — direction, wave model, review discipline (every §7 error was
caught by his review rounds), pre-registration requirement.
**Hope** (Spine-First cognitive OS, written by Máté Róbert) — circuit design,
analysis code, statistics, and this document's first draft.
The human authored the method; the machine authored the manuscript; the review
was human, adversarial, and it caught every error listed in §7.

---

*Evidence-grade markers used throughout: ✅ classical · 🔬 hardware ·
⚠️ measurement-dependent/assumption · ℹ️ convention · 🔴 falsified.
Falsified results are preserved as results.*
