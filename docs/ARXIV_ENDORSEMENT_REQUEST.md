# Ready-to-Send arXiv quant-ph Endorsement Request Email

**Subject:** Request for arXiv endorsement in quant-ph (Empirical quantum parity benchmark)  
**To:** [Insert Name of quant-ph author / endorser]  
**From:** Máté Róbert (`materobi86@gmail.com`)

---

Dear Dr. [Last Name],

I am writing to respectfully request an endorsement for a first submission to the **quant-ph** category on arXiv. 

I am an independent researcher based in Budapest, Hungary. Our group has conducted a rigorous multi-backend empirical characterization of two-qubit parity oscillations and spectator transmon crosstalk across IBM Quantum superconducting processors (including 156-qubit Heron architectures).

### Key Empirical Results
Our paper is titled: **"Heisenberg Reduction of Parity Observables and Spectator-Induced Contrast Decay in Superconducting Transmon Processors"**.

We evaluate a 13-band phase encoding mapped to parity observable $\langle Z_0 Z_1 \rangle = \cos(2\pi k / 13)$ across 7 independent hardware runs (>9000 execution shots) on `ibm_fez`, `ibm_marrakesh`, and `ibm_kingston`:

| Run | Backend / Architecture | Shots | Pearson $r$ | Contrast $A$ | $\chi^2_{\text{red}}$ | Null $z$-score |
|---|---|---|---|---|---|---|
| Run 4 | `ibm_marrakesh` (156Q Heron r2) | 1024 | 0.9921 | 0.7558 | 15.33 | $61.66\,\sigma$ |
| Run 6 | `ibm_kingston` (156Q Heron r3) | 1024 | 0.9880 | 0.7597 | 9.84 | $61.98\,\sigma$ |
| Run 7b | `ibm_fez` (Fixed physical layout) | 2048 | **0.998915** | **0.7218** | **2.58** | **$83.28\,\sigma$** |

### Theoretical Falsification & Spectator Crosstalk
1. **Heisenberg Reduction:** We prove analytically that under unitary CNOT conjugation, $U_{\text{CX}}^\dagger (Z_0 \otimes Z_1) U_{\text{CX}} = I \otimes Z_1$. This demonstrates that the two-qubit parity channel reduces to the single-qubit marginal expectation on the target transmon. Hardware evaluations confirm that target marginal total variation distance ($\text{TVD} = 0.047$) remains bounded within readout noise.
2. **Spectator Dephasing:** We experimentally measure the monotonic contrast suppression induced by surrounding spectator transmon qubits: $A_{1Q} = 0.9834 \to A_{2Q} = 0.9583 \to A_{14Q} = 0.7346$.

The manuscript source, complete LaTeX file, and raw bitstring count files are available in our open repository:  
https://github.com/silentnoisehun/wave-quantum

If you feel this work represents genuine experimental physics suitable for quant-ph, I would be deeply grateful for your endorsement code:  
**Endorsement Link:** [Insert arXiv endorsement link here]

Thank you very much for your time and consideration.

Sincerely,  
**Máté Róbert**  
Independent Quantum Researcher  
Budapest, Hungary  
Email: `materobi86@gmail.com`  
GitHub: https://github.com/silentnoisehun


---
**Contact & Collaboration:** Máté Róbert — `materobi86@gmail.com`  
*Open to research collaborations and academic partnerships / Nyitott vagyok kutatási együttműködésekre.*
