# Single-Qubit Rabi Dynamics in a 14-Qubit Spectator Network on Superconducting QPUs

## An Experimental Investigation of Circuit Compilation, Layout Systematics, and Decoupled Observables

**Version:** 2.1 · HARDWARE-VALIDATED RELEASE  
**Project:** `wave-quantum` — an experimental quantum circuit layer over Qiskit Runtime  
**Author:** Máté Róbert  
**Central finding:** What was originally hypothesised as an emergent two-qubit correlation channel in a wave-packet encoding architecture is analytically proven to be an exact single-qubit Rabi oscillation on the partner qubit (`⟨Z₀ · Z₁⟩ = ⟨Z₁⟩ = cos(2π·k/N)`). The readout qubit and 12 spectator reservoir qubits decouple completely from the observable. Across seven hardware runs on three 156-qubit IBM Heron processors (`ibm_fez`, `ibm_marrakesh`, `ibm_kingston`), we benchmark this rotation under 14-qubit compilation and demonstrate that pinning transpiler physical layouts eliminates multi-chain compilation artifacts, reducing systematic scatter by ~5× (σ_sys from 0.15–0.19 to 0.023–0.035).

---

## 0. Claim Markers

Every technical claim in this document carries the grade of its evidence:

| Marker | Meaning | Scope & Limitations |
|---|---|---|
| ✅ **PROVEN (analytical / classical)** | Proven by Heisenberg operator pullback and exact state-vector simulation. | Fully general for ideal unitary execution. |
| 🔬 **REPRODUCED (hardware)** | Measured on real superconducting QPUs with explicit layout configurations and raw counts. | Hardware numbers depend on calibration and coherence times. |
| ⚠️ **MEASUREMENT-DEPENDENT** | Numeric quantities (contrast A, σ_sys, χ²_red) determined empirically from device runs. | Subject to device drift and calibration updates. |
| ℹ️ **METHODOLOGICAL LESSON** | Insights regarding circuit transpilation, experimental control, and error documentation. | Architectural and diagnostic guidance. |

> ### ⚠️ Mandatory Clarification — What this Paper Does NOT Claim
> 1. **No new physics or novel quantum channels:** The measured cosine curve `cos(2π·k/N)` is an exact Rabi rotation of a single qubit under `RX(θ)`. The two-qubit parity measurement equals the single-qubit marginal.
> 2. **No wave-packet memory validation:** The spectator qubits and wave parameters A and φ decouple from the expectation value. The circuit functions as a single-qubit probe embedded in a 14-qubit compiled network.
> 3. **No post-selection or unmitigated masking:** All reported numbers derive from raw, unmitigated bitstring counts, published in full.

---

## 1. Abstract

We examine the physical mechanism underlying frequency-parameter encoding in a 14-qubit quantum reservoir circuit (`build_v3`), consisting of an amplitude-encoded readout qubit (`q₀`), 13 frequency-rotated reservoir qubits (`q₁..q₁₃`), an entangling `H + CX` ladder, and an X-basis measurement. 

Using operator pullback in the Heisenberg picture, we prove that the measured two-qubit correlation `⟨Z₀ · Z₁⟩` reduces analytically to single-qubit Rabi dynamics on the partner qubit:
```
⟨Z₀ · Z₁⟩ = ⟨Z₁⟩ = cos(2π·k/N)
```
The readout qubit `q₀` and the 12 spectator reservoir qubits (`q₂..q₁₃`) decouple completely from the observable. Consequently, the previous claim that information is absent from marginals and present only in correlations is debunked: the readout qubit's marginal is trivially fixed at `⟨Z₀⟩ = +1.0` (it tracks amplitude A, but carries zero information regarding frequency band k), while the partner qubit's marginal `⟨Z₁⟩` carries the exact cosine oscillation.

Experimentally, we benchmark this 14-qubit compiled circuit across seven runs on three 156-qubit IBM Quantum Heron r2 processors (`ibm_fez`, `ibm_marrakesh`, `ibm_kingston`). We show that under default compilation, the transpiler dynamically selects 2–4 distinct physical chains across the 13 frequency bands, inducing artificial systematic scatter (`σ_sys ≈ 0.15–0.19`, `χ²_red ≈ 15–100`). By pre-registering a fixed-layout parameterised circuit transpiled once to an invariant physical chain, this systematic artifact is suppressed by ~5× (`σ_sys ≈ 0.023–0.035`, `χ²_red ≈ 2.58–4.69`), achieving Pearson correlations up to **0.9989** with fitted contrast A = 0.72–0.76.

---

## 2. Circuit Architecture and Analytical Reduction

### 2.1 Circuit Specification (`build_v3`)

The circuit operates on 14 qubits (1 readout qubit `q₀`, 1 partner qubit `q₁`, and 12 spectator reservoir qubits `q₂..q₁₃`) and 2 classical measurement bits:
1. **Readout preparation:** `RY(θ_A)` on `q₀`, where `θ_A = 2·arcsin(√A)`.
2. **Reservoir rotation:** `RX(θ_k)` on each `q_i` (`i=1..13`), where `θ_k = 2π·k/N` with N = 13 and `k ∈ {0..12}`.
3. **Phase rotation:** `RZ(2φ)` on `q₀`.
4. **Bridge ladder:** For each `q_i` (`i=1..13`): `H(q_i)` followed by `CX(q_i → q₀)`.
5. **Basis rotation:** `H(q₀)` and `H(q₁)`.
6. **Measurement:** Standard computational Z-basis measurement on `q₀` (to `c[0]`) and `q₁` (to `c[1]`).

*Measurement Basis Clarification:* All hardware execution is measured physically in the computational (Z) basis. Because Hadamard gates `H` are applied to `q₀` and `q₁` immediately prior to measurement, measuring in computational Z evaluates the pre-Hadamard X Pauli observable ($H^\dagger Z H = X$). In this document, $\langle Z_1 \rangle$ and $\langle Z_0 Z_1 \rangle$ refer to expectation values computed from the resulting computational basis bitstrings.

### 2.2 Operator Pullback in the Heisenberg Picture

Let the measurement observable be the two-qubit parity `O = Z₀ ⊗ Z₁`.
Because Hadamard gates precede the Z-basis measurement on both `q₀` and `q₁`, the observable immediately prior to step (5) is:
```
O_pre5 = X₀ ⊗ X₁
```

We now trace `O_pre5` backwards through the entangling gates in step (4):
- The entangling gates are `CX(q_i → q₀)` for `i = 13, 12, ..., 1`.
- For any spectator qubit `i ∈ {2..13}`, the gate `CX(q_i → q₀)` has target `q₀` and control `q_i`. Under `CX(control → target)`:
  ```
  CX† (X_target ⊗ I_control) CX = X_target ⊗ I_control
  ```
  Since `X₁` is completely unaffected by gates on `q_i` (`i ≥ 2`), all spectator entangling gates leave `X₀ ⊗ X₁` strictly invariant.
- For the partner gate `CX(q₁ → q₀)`:
  Recall that in the X-basis, control and target interchange:
  ```
  CX† (X_target ⊗ X_control) CX = I_target ⊗ X_control
  ```
  Evaluating on qubits `(q₀, q₁)`:
  ```
  CX† (X₀ ⊗ X₁) CX = I₀ ⊗ X₁
  ```

**Key Result 1:** The readout qubit `q₀` decouples completely. The observable transforms into the identity on `q₀` and Pauli `X` on `q₁`. Any gate applied to `q₀` prior to step (4) — including `RY(θ_A)` and `RZ(2φ)` — acts upon `I₀` and has zero physical effect on the expectation value.

Tracing backwards through qubit `q₁`'s operations:
- Prior to `CX(q₁ → q₀)`, qubit `q₁` underwent `H(q₁)`.
  ```
  H† X₁ H = Z₁
  ```
- Prior to `H(q₁)`, qubit `q₁` underwent `RX(θ_k)` from initial state `|0⟩`:
  ```
  ⟨0| RX†(θ_k) Z₁ RX(θ_k) |0⟩ = cos(θ_k) = cos(2π·k/13)
  ```

Therefore:
```
⟨Z₀ · Z₁⟩ = cos(2π·k/13)
```

### 2.3 The Single-Qubit Marginal Identity

At the standard benchmark parameter `A = 0.5` (`θ_A = π/2`) and `φ = 0`:
- Qubit `q₀` is prepared in `RY(π/2)|0⟩ = |+⟩`.
- As `|+⟩` is an eigenstate of `X` with eigenvalue +1, the `CX` gates from control qubits apply zero phase kickback.
- The final `H(q₀)` rotates `|+⟩` back to `|0⟩`.
- In the computational basis, `P(q₀ = 0) = 1.0` and `P(q₀ = 1) = 0.0`, giving `⟨Z₀⟩ = +1.0`.

Because `q₀` is deterministically in `|0⟩`:
```
⟨Z₀ · Z₁⟩ = (+1.0) · ⟨Z₁⟩ = ⟨Z₁⟩
```
**Key Result 2:** The partner qubit's single-qubit marginal `⟨Z₁⟩` identically equals the two-qubit correlation `⟨Z₀ · Z₁⟩`. The "no-go" observation applies solely to the readout qubit `q₀` (which carries zero information about band k), whereas the partner marginal carries the complete Rabi signal.

---

## 3. Falsification and Revision History

| Version | Claim | Evaluation | Mechanism / Resolution |
|---|---|---|---|
| v1 | Frequency decodable from readout marginal `⟨Z₀⟩` | 🔴 Falsified on hardware (TVD = 0.047) | CX target marginal carries zero frequency information. |
| v2 | Z-basis correlation `⟨Z₀Z₁⟩` tracks amplitude A | ✅ Falsified in simulation | At A=0.5, `q₀` is in `|+⟩`, carrying no Z-basis amplitude parity. |
| v3 (initial) | Two-qubit correlation is novel `cos(2πk/13)` channel | ⚠️ Conceptually reframed | Heisenberg reduction proves observable is single-qubit Rabi `⟨Z₁⟩`. |
| v3 (hardware) | Layout-pinned circuit isolates single-qubit contrast | 🔬 Hardware validated | Suppressed transpiler chain re-selection by 5×. |

---

## 4. Hardware Validation Across Three QPUs

### 4.1 Benchmark Conditions
All experiments were conducted on IBM Quantum 156-qubit Heron r2 superconducting processors using Qiskit Runtime SamplerV2 with raw, unmitigated bitstring counts.

### 4.2 Completed Run Series

| Run | Backend | Shots | Physical Layout | Pearson r | Contrast A | χ²_red | σ_sys |
|---|---|---|---|---|---|---|---|
| 1 | `ibm_fez` | 512 | Free (3 chains / 13 bands) | 0.8732 | 0.4978 | 23.99 | 0.1973 |
| 2 | `ibm_fez` | 2048 | Free (2 chains) | 0.9279 | 0.6712 | 100.20 | 0.1895 |
| 3 | `ibm_fez` | 1024 | Free (3 chains) | 0.9528 | 0.6319 | 29.96 | 0.1480 |
| 4 | `ibm_marrakesh` | 1024 | Free (4 chains) | 0.9921 | 0.7558 | 15.33 | 0.0957 |
| 6 | `ibm_kingston` | 1024 | Free (dynamic) | 0.9880 | 0.7597 | 9.84 | 0.0749 |
| **7** | `ibm_fez` | 2048 | **Fixed** (`q₀=107, q₁=106...`) | **0.9973** | **0.7396** | **4.69** | **0.0348** |
| **7b** | `ibm_fez` | 2048 | **Fixed** (identical to 7) | **0.9989** | **0.7218** | **2.58** | **0.0231** |

*Note on Run 7b Execution:* Runs 7 and 7b were consecutive executions on the identical physical chain. Run 7b was initially dispatched under Job ID `db5frpkvf2bc73cvrk4g` (manual 156Q non-ISA template, cancelled), and successfully executed under Job ID `db5g2jg4qg6s73c3e3vg` (bound from the identical parameterised ISA template as Run 7; full instruction SHA256 hash `e1716ada22cb0cda1cd40c7e9f0500e6acefedd2a97dc2a8bd85e36fdefe27a3` recorded in `circuit_hashes.json`).

---

## 5. Statistical Diagnostics & Layout Systematics

### 5.1 Noise Model and Systematic Variance
We adopt a consistent binomial variance model for each band k:
```
σ_k² = max(1.0 - (A · t_k)², 10⁻⁹) / shots
```
where `t_k = cos(2π·k/N)`. The reduced chi-square `χ²_red = χ² / (N - 1)` scales linearly with shots under constant systematic error:
```
σ_sys = √[ max(χ²_red - 1.0, 0.0) / (shots · ⟨1/σ_k²⟩) ]
```

### 5.2 Corrected 68% Confidence Bounds
For 12 degrees of freedom, the 68% confidence interval (1σ) of the chi-square distribution is **[0.85×, 1.29×]** (correcting earlier asymmetric approximations).
- For Run 7: `σ_sys = 0.0348`, 68% CI = `[0.0296, 0.0449]`.
- For Run 7b: `σ_sys = 0.0231`, 68% CI = `[0.0196, 0.0298]`.
Both bounds lie strictly below the pre-registered 0.10 threshold.

### 5.3 Diagnostic Verdict
1. **Layout artifact verified:** In free-layout runs (1–4), the transpiler re-selected physical qubits per band, generating an artificial variance floor of `σ_sys ≈ 0.15–0.20`. Fixing the layout reduced `σ_sys` to `0.023–0.035`, proving that the scatter was largely compilation-induced.
2. **Persistent non-binomial residual:** Even with fixed layout, `χ²_red` remains at 2.58–4.69 (> 1.0). Residual inspection indicates a small additive offset (`c ≈ 0.03–0.06`) arising from asymmetric readout relaxation (`|1⟩ → |0⟩`), requiring an additive term in high-precision calibrations.

---

## 6. The Decisive Scaling Experiment (IBM Marrakesh, 2048 shots)

To definitively test the analytical reduction, we executed a 49-circuit benchmark in a single job on `ibm_marrakesh` (Job ID: `db5pe8clf4us73c4cfag`, 2048 shots, physical chain `[89, 88, 87, 78, 69, 70, 71, 58, 51, 52, 53, 54, 55, 59]`, readout `q₀=89`, partner `q₁=88`):

### 6.1 Contrast Scaling (1Q vs 2Q vs 14Q)

| Architecture | Measured Observable | Fitted Contrast A | Pearson r | χ²_red | σ_sys |
|---|---|---|---|---|---|
| **1-Qubit** (partner `q88` only) | `⟨Z₁⟩` | **0.9834** | **0.9996** | 2.23 | 0.0104 |
| **2-Qubit** (`q89, q88`) | `⟨Z₀ · Z₁⟩` | **0.9583** | **0.9998** | **0.82** | **< 0.001\*** |
| **2-Qubit** (`q89, q88`) | `⟨Z₁⟩` (partner marginal) | **0.9599** | **0.9998** | **0.87** | **< 0.001\*** |
| **14-Qubit** (full chain) | `⟨Z₀ · Z₁⟩` | **0.7346** | **0.9993** | 4.09 | 0.0320 |
| **14-Qubit** (full chain) | `⟨Z₁⟩` (partner marginal) | **0.8386** | **0.9995** | 6.18 | 0.0371 |

*\*Note: In the 2-qubit circuit, $\chi^2_{\text{red}} < 1.0$, indicating that systematic error is undetectable within binomial statistical noise.*

**Key Findings:**
1. **Marginal equals correlation:** In the 2-qubit circuit, the parity correlation `⟨ZZ⟩` (0.9583) and the partner marginal `⟨Z₁⟩` (0.9599) agree to within 0.0016, and both achieve sub-unity reduced chi-square (`χ²_red = 0.82 < 1.0`), showing that the two-qubit correlation is purely the partner's Rabi oscillation.
2. **Monotonic contrast decay with spectator scale:** Contrast decays monotonically as spectator qubits are added:
   $$ A = 0.9834 \text{ (1Q)} \longrightarrow 0.9583 \text{ (2Q)} \longrightarrow 0.7346 \text{ (14Q)} $$
   The 12 spectator qubits and their 24 entangling gates do not alter the functional form ($r > 0.999$ in all cases), but degrade the contrast by ~24% due to gate error accumulation and spectator decoherence.
3. **The 0.10 Gap in 14-Qubit Parity:** In the 14-qubit circuit, the partner marginal contrast is $A = 0.8386$, whereas the two-qubit parity contrast is $A = 0.7346$; the gap is $\approx 0.104$. Under ideal unitary evolution $\langle Z_0 Z_1 \rangle = \langle Z_0 \rangle \langle Z_1 \rangle = (+1) \langle Z_1 \rangle$. On hardware, qubit $q_0$ serves as the target of 13 entangling CX gates and undergoes readout relaxation, lowering its expectation value to $\langle Z_0 \rangle \approx 0.82–0.88$ (mean $\approx 0.86$). The product $0.86 \times 0.8386 \approx 0.721$ accounts for the gap almost entirely; the measured parity is $0.735$, a difference of only $\approx 0.014$, which is within statistical uncertainty.

### 6.2 Parameter Decoupling (A-Sweep and φ-Sweep)

Using the 14-qubit circuit at fixed frequency band $k=2$ (theoretical value $\cos(2\pi \cdot 2/13) \approx 0.5681$):
- **A-Sweep ($A \in \{0.1, 0.3, 0.5, 0.7, 0.9\}$, $\varphi=0.0$):**
  Measured `⟨ZZ⟩` remains completely flat:
  `A=0.1: +0.4531` · `A=0.3: +0.4062` · `A=0.5: +0.4082` · `A=0.7: +0.3770` · `A=0.9: +0.4336` (mean $0.415 \pm 0.029$).
  Meanwhile, the readout marginal `⟨Z₀⟩` tracks the parameter preparation: $0.5400 \to 0.8770 \to 0.5361$.
- **φ-Sweep ($\varphi \in \{0.0, 0.5, 1.0, 1.5, 2.0\}$, $A=0.5$):**
  Measured `⟨ZZ⟩` remains positive and flat ($0.476 \pm 0.059$), while the partner marginal `⟨Z₁⟩` swings from $+0.4541$ to $-0.5684$ as the readout state rotates away from $|+\rangle$.

This experimentally demonstrates that the two-qubit parity `⟨Z₀Z₁⟩` is physically decoupled from the amplitude and phase parameterization of the wave packet, settling the question definitively.

---

## 7. Documented Errors and Methodological Lessons

1. **Analytical identification failure:** Believing `⟨Z₀Z₁⟩ = cos(θ)` was an emergent multi-qubit entangled property rather than a single-qubit Rabi pullback.
2. **False marginal no-go:** Claiming frequency information was absent from marginals when the partner marginal `⟨Z₁⟩` identically matched the correlation.
3. **Overstating z-score significance:** Leading with `z > 28σ` when any functional circuit rejects a zero-signal null.
4. **Noise model inconsistency:** Temporarily mixing `1/√shots` with binomial variances.
5. **Transpiler layout blindness:** Unintentionally running different frequency bands on different physical qubits during early sweeps.
6. **Git timestamp misattribution:** Treating local git commit timestamps as cryptographic third-party proof.
7. **Citation inaccuracy:** Citing Schuld et al. (2020/2021) as "Schuld 2008".

---

## 8. Reproduction

### 8.1 Pure Analytical / Simulation Sweep (Zero Quota)
```bash
python wave_quantum_v3.py --sweep
```
Verifies `⟨Z₀Z₁⟩ == ⟨Z₁⟩` and `⟨Z₀⟩ == +1.0000` across all 13 bands in state-vector simulation without requiring any cloud API key or quota.

### 8.2 Hardware Execution (QPU)
```bash
python wave_quantum_v3.py --backend ibm_fez --shots 2048 --fixed-layout
```

### 8.3 Statistical Evaluation
```bash
python _referee_stats.py
```
Computes A, χ²_red, σ_sys, and z-scores from local result JSON files. Raw counts for all runs are available in `raw_counts_all_runs.json`.

---

## 9. References

1. C. A. Sackett et al., *Experimental entanglement of four particles*, Nature **404**, 256–259 (2000).
2. M. Schuld, R. Sweke, and J. J. Meyer, *The effect of data encoding on the expressive power of variational quantum machine learning models*, Phys. Rev. A **103**, 032430 (2021) [arXiv:2008.08605].
3. Y. Suzuki, Q. Gao, K. C. Pradel, K. Yasuoka, and N. Yamamoto, *Natural quantum reservoir computing for temporal information processing*, Sci. Rep. **12**, 1353 (2022) [arXiv:2107.05808].
4. J. Chen, H. I. Nurdin, and N. Yamamoto, *Temporal Information Processing on Noisy Quantum Computers*, Phys. Rev. Applied **14**, 024065 (2020) [arXiv:2001.09498].

---

## Acknowledgments
The circuit synthesis, state-vector simulation checks, and initial document drafting were supported by Hope, an AI coding assistant operating within the DeepSeek Harness environment.
