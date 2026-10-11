# wave-quantum

**Rabi-görbe demonstráció 14-qubit-es transpilált környezetben — validálva valós szupravezető hardveren.**

> **Eredeti motiváció:** $\psi(t) = A \cdot \exp(-\gamma t) \cos(2\pi f t + \varphi)$ paramétereinek áramköri kódolása.  
> **Fizikai valóság:** Az analitikus levezetés és a hardveres mérések bizonyítják, hogy a mért paritás-megfigyelhető analitikusan független az $A$ amplitúdótól és a $\varphi$ fázistól; a megfigyelhető kizárólag a frekvenciához rendelt $k$ forgatási szöget viszi át.

**Szerző:** Máté Róbert (AI asszisztens / kódgenerálás: Hope) · **Dátum:** 2026-10-10/11 ·  
**Backendek:** IBM `ibm_fez`, `ibm_marrakesh`, `ibm_kingston` (156Q Heron r2)

---

## 1. Mit mérünk valójában

A vizsgált áramkörben összesen 14 qubit vesz részt:
- 1 readout qubit ($q_0$)
- 1 partner qubit ($q_1$)
- 12 spektátor rezervoár-qubit ($q_2..q_{13}$)

### Bázisok és mérés definíciója
A kvantumprocesszoron minden fizikai mérés a standard komputációs ($Z$) bázisban történik. Mivel a mérés előtt mind a readout ($q_0$), mind a partner ($q_1$) qubit kap egy Hadamard ($H$) kaput, a komputációs $Z$ mérés a Hadamard előtti állapot $X$ Pauli-megfigyelhetőjét méri ($H^\dagger Z H = X$). Amikor a szövegben $\langle Z_1 \rangle$-et vagy $\langle Z_0 Z_1 \rangle$-et írunk, az a záró Hadamard kapuk utáni komputációs mérésekből számított várható értékeket jelöli.

### Az analitikus azonosság
A Heisenberg-képben visszakövetve az operátort a $CX(q_1 \to q_0)$ kapun át:
```
(CX)† (X_partner ⊗ X_readout) CX = X_partner ⊗ I_readout
```
A readout qubit ($q_0$) és a 12 spektátor qubit teljesen kiesik a megfigyelhetőből. A megelőző $H(q_1)$ kapu az $X_1$-et $Z_1$-re fordítja, így a kezdeti $|0\rangle$ állapotra ható $RX(\theta_k)$ forgatás pontosan egy egyqubites **Rabi-görbét** ad:
```
⟨Z₀ · Z₁⟩ = ⟨Z₁⟩ = cos(2π·k/N)      (N = 13 sáv)
```

### A readout marginális szerepe
- A readout qubit ($q_0$) marginálisa nem hordoz információt a frekvencia-sáv $k$-ról (ezért hiúsult meg a korábbi v1 frekvencia-dekódolás), de követi az $A$ amplitúdót ($A$-sweep során $0.54 \to 0.88 \to 0.54$).
- A partner qubit ($q_1$) saját marginálisa közvetlenül és teljes kontraszttal hordozza a frekvenciát: $\langle Z_1 \rangle = \cos(2\pi k/13)$.

---

## 2. Eredmények — 7 befejezett futás

| Run | Backend | Shots | Layout | Pearson | Kontraszt A | χ²_red | σ_sys (binomiális) |
|---|---|---|---|---|---|---|---|
| 1 | fez | 512 | free (3 lánc / 13 sáv) | 0.8732 | 0.4978 | 23.99 | 0.1973 |
| 2 | fez | 2048 | free (2 lánc) | 0.9279 | 0.6712 | 100.20 | 0.1895 |
| 3 | fez | 1024 | free (3 lánc) | 0.9528 | 0.6319 | 29.96 | 0.1480 |
| 4 | marrakesh | 1024 | free (4 lánc) | **0.9921** | **0.7558** | 15.33 | 0.0957 |
| 6 | kingston | 1024 | free (dinamikus) | **0.9880** | **0.7597** | 9.84 | 0.0749 |
| **7** | fez | 2048 | **fixed** (`q₀=107, q₁=106...`) | **0.9973** | **0.7396** | **4.69** | **0.0348** |
| **7b** | fez | 2048 | **fixed** (azonos a 7-tel) | **0.9989** | **0.7218** | **2.58** | **0.0231** |

> *A fenti táblázat nem javuló trendet mutat: a szabad futásoknál a transpiler sávonként 2–4 különböző láncot választott. A rögzített layout futások (7 és 7b) két egymást követő mérésből állnak ugyanazon a fizikai láncon, ahol a drift minimális ($\Delta A = 0.0178$).*  
> *Run 7b Job ID megjegyzés: az első próba (`db5frpkv...`) manuális 156Q nem-ISA sablon volt, lemondva; a második (`db5g2jg4...`) az érvényes lefutott mérés.*

**Nyers adatok:** Minden futás nyers bitstring-számlálása megtalálható az egyedi `result_run*.json` fájlokban és a konszolidált `raw_counts_all_runs.json`-ban.

---

## 3. A döntő skálázási kísérlet (1Q vs 2Q vs 14Q és A/φ szétcsatolás)

Lefuttatva egyetlen jobban az `ibm_marrakesh` processzoron (Job ID: `db5pe8clf4us73c4cfag`, 2048 shots, fizikai lánc `[89, 88, 87, 78, 69, 70, 71, 58, 51, 52, 53, 54, 55, 59]`, readout $q_0 = 89$, partner $q_1 = 88$):

| Architektúra | Mért megfigyelhető | Kontraszt A | Pearson r | χ²_red | σ_sys |
|---|---|---|---|---|---|
| **1-qubit** (kizárólag partner $q_{88}$) | $\langle Z_1 \rangle$ | **0.9834** | **0.9996** | 2.23 | 0.0104 |
| **2-qubit** ($q_{89}, q_{88}$) | $\langle Z_0 \cdot Z_1 \rangle$ | **0.9583** | **0.9998** | **0.82** | **< 0.001\*** |
| **2-qubit** (partner marginális) | $\langle Z_1 \rangle$ | **0.9599** | **0.9998** | **0.87** | **< 0.001\*** |
| **14-qubit** (teljes lánc) | $\langle Z_0 \cdot Z_1 \rangle$ | **0.7346** | **0.9993** | 4.09 | 0.0320 |
| **14-qubit** (partner marginális)| $\langle Z_1 \rangle$ | **0.8386** | **0.9995** | 6.18 | 0.0371 |

*\*Megjegyzés: A 2-qubites mérésnél $\chi^2_{\text{red}} < 1.0$, azaz a szisztematikus hiba nem mutatható ki, a binomiális statisztikai zaj dominál.*

### Főbb kísérleti megfigyelések
1. **Marginalis == korreláció:** A 2-qubites áramkörben a paritáskorreláció $\langle Z_0 Z_1 \rangle$ (0.9583) és a partner marginálisa $\langle Z_1 \rangle$ (0.9599) **0.0016-on belül megegyezik**.
2. **Monoton kontraszt-csökkenés a spektátorok számával:**
   $$ A = 0.9834 \text{ (1Q)} \longrightarrow 0.9583 \text{ (2Q)} \longrightarrow 0.7346 \text{ (14Q)} $$
3. **A 0.10-es rés fizikai oka a 14-qubites áramkörnél:**  
   A 14-qubites mérésben a partner marginálisa $A = 0.8386$, míg a kétqubites paritás $A = 0.7346$. Az ideális összefüggés $\langle Z_0 Z_1 \rangle = \langle Z_0 \rangle \langle Z_1 \rangle$ alapján ez a rés közvetlenül a readout qubit hibájára vezethető vissza: a $q_0$ a 13 CX kapu célpontjaként és a readout relaxáció miatt sávonként $\langle Z_0 \rangle \approx 0.82–0.88$ között ingadozik (átlagosan $\approx 0.86$). A $0.86 \times 0.8386 \approx 0.721$ szorzat a $0.10$-es rés túlnyomó részét ($\approx 85\%$-át) megmagyarázza, a maradék pedig a spektátor crosstalknak és a korrelált kiolvasási zajnak tulajdonítható.
4. **$A$ és $\varphi$ függetlenség:**
   - $A \in [0.1, 0.9]$ között a mért $\langle Z_0 Z_1 \rangle$ konstans $0.415 \pm 0.029$ marad (elmélet: 0.5681), miközben a readout marginal $0.54 \to 0.88 \to 0.54$ között változik.
   - $\varphi \in [0.0, 2.0]$ között a paritás lapos ($0.476 \pm 0.059$), miközben a partner marginálisa lengeti az előjelét.

---

## 4. Falszifikációs lánc (a projekt története)

| Verzió | Hipotézis | Falszifikáció módja |
|---|---|---|
| v1 | A readout marginális hordozza a frekvenciát | 🔬 Hardveren falszifikálva: TVD = 0.047 (zajszint). |
| v2 | A Z-bázisú korreláció követi az $A$ amplitúdót | ✅ Szimulációban cáfolva ($A=0.5$-nél $q_0$ $|+\rangle$-ban van). |
| v3 (első tipp) | $\langle ZZ \rangle = \cos(\pi k/N)$ | ✅ Szimulációban cáfolva: 12/13 sáv elbukott. |
| v3 | $\langle ZZ \rangle = \cos(2\pi k/N)$ | ✅ Analitikusan és 🔬 hardveren igazolva (Rabi-görbe). |
| v3 (értelmezés) | "Új kétqubites hullám-korrelációs csatorna" | ⚠️ Analitikusan cáfolva: az operátor $\langle Z_1 \rangle$-re redukálódik. |

---

## 5. Futtatás és reprodukció

```bash
# 1. Helyi szimulációs sweep (nulla kvóta, nem kell API kulcs)
python wave_quantum_v3.py --sweep

# 2. Hardveres futtatás (QPU)
python wave_quantum_v3.py --backend ibm_fez --shots 2048 --fixed-layout

# 3. Statisztikai kiértékelés a helyi JSON fájlokból
python _referee_stats.py
```

---

## 6. Hivatkozások

Ha használod a munkát vagy az adatokat, idézd az összetevőket:
- Paritás-oszcillációk mérése: Sackett et al., *Nature* 404, 256–259 (2000).
- Kvantum forgatási szögkódolás Fourier-struktúrája: Schuld, Sweke, Meyer, *Phys. Rev. A* 103, 032430 (2021) [arXiv:2008.08605].
- Kvantum rezervoár architektúrák szupravezető hardveren: Suzuki et al., *Sci. Rep.* 12, 1353 (2022) [arXiv:2107.05808]; Chen, Nurdin, Yamamoto, *Phys. Rev. Applied* 14, 024065 (2020) [arXiv:2001.09498].
