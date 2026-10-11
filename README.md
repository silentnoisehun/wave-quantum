# wave-quantum

**Rabi-görbe demonstráció 14-qubit-es routinggal — validálva valós szupravezető hardveren.**

> ψ(t) = A · exp(−γ·t) · cos(2πft + φ)
> A = amplitúdó · f = frekvencia · φ = fázis · γ = csillapítás (post-processing, NEM kapu)

**Szerző:** Hope (Máté Róbert gerincén) · **Dátum:** 2026-10-10/11 ·
**Backendek:** IBM `ibm_fez`, `ibm_marrakesh`, `ibm_kingston` (156Q Heron r2)

## Mit valójában mérünk

A kód a partner qubiton (q1) egy **Rabi-görbét** produkál:

```
⟨Z₁⟩ = cos(2π·k/N)      N = 13 sáv, X-bázisú mérés
```

A 13 rezervoár-qubit mind RX(2πk/N)-el elforgatva, a CX(q₁→q₀) bridge-en keresztül
a readout qubit (q₀) csak zajt ad a méréshez. A korreláció ⟨Z₀Z₁⟩ ebben az
architektúrában **egyenlő** a partner qubit saját marginálisával ⟨Z₁⟩-vel.
A "tétel" ⟨ZZ⟩ = cos(2πk/N) egy ismert kvantummechanikai azonosság
(Rabi-görbe), nem új fizika.

A párosított "no-go" (a readout qubit marginalisa nem hordoz információt)
csak a readout qubitra (q₀) igaz, ott triviális: A=0.5, φ=0 beállításnál
a q₀ |+⟩ állapotban van, így bármilyen CX után is zajban marad.

**Mi valójában új:** egy ismert kvantummechanikai görbe reprodukálása
14-qubit-es routinggal, 3 backend-en, stabil kontraszt (0.72–0.76)
és remek reprodukálhatósággal (ΔA = 0.018 két független kulccsal).

## Eredmények — 7 befejezett futás

| Run | Backend | Shots | Layout | Pearson | Kontraszt | χ²_red | σ_sys |
|---|---|---|---|---|---|---|---|
| 1 | fez | 512 | free (3 chains) | 0.873 | 0.498 | 23.99 | 0.197 |
| 2 | fez | 2048 | free (2 chains) | 0.928 | 0.671 | 100.20 | 0.189 |
| 3 | fez | 1024 | free (3 chains) | 0.953 | 0.632 | 29.96 | 0.148 |
| 4 | marrakesh | 1024 | free (4 chains) | **0.992** | **0.756** | 15.33 | 0.096 |
| 6 | kingston | 1024 | free | **0.988** | **0.760** | 9.84 | 0.075 |
| **7** | fez | 2048 | **fixed** (107,106,105,108…) | **0.997** | **0.740** | **4.69** | **0.035** |
| **7b** | fez | 2048 | **fixed** (same as 7) | **0.999** | **0.722** | **2.58** | **0.023** |

> **worst 0.873 · median 0.953 · best 0.999**  
> *Nem trend — a számok backend- és layout-függőek.*

**Raw adatok:** minden futás `result_run*.json` fájlban a gyökérben.

## Státusz

| Érv | Minősítés |
|---|---|
| Rabi-görbe reprodukálása szimulációban (13/13 sáv) | ✅ reprodukálható |
| Ugyanaz a görbe 3 backend-en, 7 futásban | 🔬 hardveren reprodukálva |
| Rögzített layout stabilizálja a kontrasztot (σ_sys 5× csökkenés) | 🔬 reprodukálva (pre-regisztrált) |
| ΔA = 0.018 stabilitás két független API kulccsal | 🔬 reprodukálva |
| Új fizika / új kvantum-algoritmus | ❌ NEM — ismert Rabi-görbe |
| "Tétel" újdonsága | ❌ NEM — cos(2πk/N) = Rabi-görbe |

Legjobb mérés: **Pearson 0.9989, χ²_red 2.58** (rögzített layout, 2048 shots,
bitre-azonos ISA áramköreket futtatva két független API kulccsal).

## Falszifikációs lánc (a módszer)

| Verzió | Feltételezés | Cáfolva |
|---|---|---|
| v1 | readout marginal hordozza a frekvenciát | 🔬 hardware: TVD = 0.047 |
| v2 | Z-bázisú korreláció követi az A-t | ✅ szimuláció |
| v3 első tipp | ⟨ZZ⟩ = cos(πk/N) | ✅ szim: 12/13 sáv fail |
| v3 | ⟨ZZ⟩ = cos(2πk/N) | — aktuális, ✅ + 🔬 |

A cáfolt eredmények megmaradnak eredményként. A teljes történet — statisztikai
hibák, review-körök, előregisztráció — a [CHRONICLE.md](CHRONICLE.md)-ben.

## Dokumentumok

- **[White paper (EN)](docs/WHITE_PAPER.en.md)** — teljes papír: claim markers,
  minden futás kiírva, elkapott hibák, prior-art, evidence levels.
- **[Krónika](CHRONICLE.md)** — hogyan jutottunk ide, minden hiba be.
- **[Előregisztrált kritériumok](REFEREE_STATS.md)** — a(layout) és drift
  küszöbök, git-be commitolva az eredmények **előtt**.

## Futtatás

```bash
# Szimuláció — 13 sáv vs cos(2πk/13)
python wave_quantum_v3.py --sweep

# Hardveres futás — 13 sáv egyetlen jobban
python wave_quantum_v3.py --backend ibm_fez --shots 2048

# Statisztika (binomiális szigma mindenhol)
python _referee_stats.py
```

Követelmények: `qiskit`, `qiskit-ibm-runtime` ≥ 0.50, IBM Quantum token.

## A döntő skálázási kísérlet (1Q vs 2Q vs 14Q és A/φ szétcsatolás)

Lefuttatva egyetlen jobban `ibm_marrakesh` hardveren (Job ID: `db5pe8clf4us73c4cfag`, 2048 shots):

| Architektúra | Megfigyelhető | Kontraszt A | Pearson r | χ²_red | σ_sys |
|---|---|---|---|---|---|
| **1-qubit** (partner q88) | `⟨Z₁⟩` | **0.9834** | **0.9996** | 2.23 | 0.0104 |
| **2-qubit** (q89, q88) | `⟨Z₀ · Z₁⟩` | **0.9583** | **0.9998** | **0.82** | **0.0000** |
| **2-qubit** (partner marginal) | `⟨Z₁⟩` | **0.9599** | **0.9998** | **0.87** | **0.0000** |
| **14-qubit** (teljes lánc) | `⟨Z₀ · Z₁⟩` | **0.7346** | **0.9993** | 4.09 | 0.0320 |
| **14-qubit** (partner marginal)| `⟨Z₁⟩` | **0.8386** | **0.9995** | 6.18 | 0.0371 |

**Főbb megfigyelések:**
1. **Marginalis == korreláció:** A 2-qubites áramkörben a korreláció `⟨ZZ⟩` (0.9583) és a partner marginálisa `⟨Z₁⟩` (0.9599) 0.0016-on belül megegyezik, mindkettő szub-egységnyi $\chi^2_{\text{red}}$-del (0.82 < 1.0).
2. **Monoton kontraszt-csökkenés a mérettel:** $0.9834 \text{ (1Q)} \to 0.9583 \text{ (2Q)} \to 0.7346 \text{ (14Q)}$. A 12 spektátor qubit kizárólag kapuhibát és dekoherenciát ad hozzá.
3. **A és φ függetlenség:** $A \in [0.1, 0.9]$ között a mért `⟨ZZ⟩` konstans $0.415 \pm 0.029$ marad (elmélet: 0.5681), miközben a readout marginal $0.54 \to 0.88 \to 0.54$ között változik. A kétqubites paritás teljesen független $A$-tól és $\varphi$-től!

## Hivatkozás

Ha használod a munkát, idézd az összetevőket tisztességgel: paritás-oszcilláció
(Sackett et al., Nature 404, 256 (2000)), Rabi-görbe mérés, QRC szupravezető
hardveren (Suzuki arXiv:2107.05808, Chen arXiv:2001.09498). A 14-qubit-es
routinggal való demonstráció és a párosított marginal-no-go megfigyelés az,
amit ez a repo hozzáad.