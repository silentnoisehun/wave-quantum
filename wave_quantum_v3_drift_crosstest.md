# Cross-Repo Falsifiability Test — Drift Crosstest Verdict

## 🧪 Átmenihipotézis (a QDS repo által)

> **A qubit-91 fázis-koherencia driftje (T₂_eff: 43–141 µs, 3.62× a mérési zajon túl) egy **általános architekturális korláto** a chipen belül. Ha igaz, akkor a wave-quantum ⟨ZZ⟩ csatornájának Pearson-rje és kontrasztja (A) is erősen ingadozik futásról futásra.

## 🔬 A kísérlet

- **QDS repo** (qubit 91, Hahn-echo → U-delay-U-dagger visszatérésikar): 5 futás, 75 s időköz, `T₂_eff = 43,1 → 140,8 µs` → **43,7% relatív szórás** (3.62× shot noise, χ²=60.7, df=4, p=2·10⁻¹²). A T₁ kontroll-kar kontroll: χ²=7.70, df=4, **p=0,10** (belefer a shot-zajba).
- **wave-quantum repo** (14-qubit ⟨ZZ⟩ csatorna, qubit 91 a layout 9. pozíciójában): ugyanaz a `build_v3` áramkör, ugyanaz a fix fizikai layout (`[107,106,105,108,109,110,111,98,91,92,93,94,95,99]`), ugyanaz a backend (`ibm_kingston`), 5 futás, 75 s időköz, 2048 shots.

## 📊 Eredmény

| Run | Job ID | ⟨ZZ⟩ Pearson r | Kontraszt A (max−min) | Mérésidőpont (QDS drift állapota) |
|-----|--------|---------------|----------------------|-------------------------------------|
| 1 | `dba1g4k24mrc7384og10` | 0.9993 | 1.4844 | QDS run 1 (T₂_eff = 77,5 µs) |
| 2 | `dba1grs24mrc7384ohlg` | 0.9992 | 1.5254 | QDS run 2 (T₂_eff = 43,1 µs — minimum) |
| 3 | `dba1hj1gv2cc73e67lj0` | 0.9994 | 1.4814 | QDS run 3 (T₂_eff = 140,8 µs — maximum) |
| 4 | `dba1iapgv2cc73e67n4g` | 0.9995 | 1.5215 | QDS run 4 (T₂_eff = 117,7 µs) |
| 5 | `dba1j27i0auc7391cl3g` | 0.9996 | 1.5254 | QDS run 5 (T₂_eff = 69,1 µs) |

**Statisztika két független mérőszámmal:**

| Mérőszám | ⟨érték⟩ | szórás | **relatív szórás** |
|----------|---------|--------|---------------------|
| ⟨ZZ⟩ Pearson r | 0.9994 | 0.00013 | **0.013%** |
| Kontraszt A (max−min ⟨ZZ⟩) | 1.5076 | 0.0226 | **1.50%** |
| QDS T₂_eff (comparálva) | 89.6 µs | 39.2 µs | **43.7%** |

**Fontos a Kontraszt A-ról:** a Pearson-r **skála- és eltolás-invariáns** — egy kontrasztokban történő driftet **nem tud felfogni**. A Kontraszt A = max⟨ZZ⟩ − min⟨ZZ⟩ viszont **érinti** a driftet: ha a qubit-koherencia romlana, a max-min intervallum összeomlana. Ezért a **két mérőszám együtt** biztosítja a cáfolatot.

## ⚖️ Ítélet

### 🔴 A hipotézis **HAMIS**.

A QDS drift (43,7% rel. szórás) és a wave-quantum ⟨ZZ⟩ stabilitása **nem ugyanazzal a nagyságrenddel** működik. A relatív szórások:

$$\frac{\sigma_{\text{T2eff}}}{\langle \text{T2eff} \rangle} = 43,7\% \quad \text{vs.} \quad \frac{\sigma_r}{\langle r \rangle} = 0,013\% \quad \text{vs.} \quad \frac{\sigma_A}{\langle A \rangle} = 1,5\%$$

Ha a qubit-91 drift architekturális lenne (az egész chipen), a 14-qubit ⟨ZZ⟩ csatorna — amely **tartalmazza** a 91-es qubitet, és ugyanabba az időszakra esik — mindkét mértékon **azonos nagyságrendű** instabilitást mutatna. **Nem teszi:** 0,013% vs 1,5% vs 43,7%.

### Az r és A stabilitása ebben a kontextusban:

- A ⟨ZZ⟩ mérés a **partner qubit marginális** (q₁ = 106) → `⟨Z₁⟩ = cos(2π·k/13)`
- A ⟨ZZ⟩ érték a q₀ (107) és q₁ (106) kooperatív méréséből jön, ahol q₀ a CX célpontja
- **Ha a drift csak a 91-es qubit (q₈ = layout 9.) koherenciáját érinti**, akkor a ⟨ZZ⟩ csatorna — amely a **0. qubiten** (107) és a **1. qubiten** (106) működik — **nem szenved** ettől, mert **a 91-es qubit a spektátor-rezervúumban** (q₂–q₁₃ között) van, és a ⟨ZZ⟩ megfigyelősége a q₀ és q₁ konzorriumára redukálódik.

Ez a **konzisztens** azzal a README.md §2.4. táblázatával és a §4. falszifikációs lánccal, ahol a "kétqubites hullám-korrelációs csatorna" hipotézist az operátor-analízis szerint **cáfolva** (a csatorna valójában `⟨Z₁⟩`-re redukálódik) hagytuk.

### A wave-quantum magas r értéke **NEM fluke**:

- 5 független futás: r = 0.9992–0.9996, A = 1.4814–1.5254
- A QDS drift-időszakok (75 s) során is **stabil marad** mind r, mind A
- A konzisztencia a statisztikai zaj szintjén (0.013%) játszik — a mérés tökéletességének szigorlatja, nem a driftnek

## 🧬 A 91-es qubit drift mechanizmusa (interpretív javaslat)

A drift **qubit-specifikus**, és a következő jelekből áll:

| Jellemző | QDS (q91) | wave-⟨ZZ⟩ (q0/q1 = 107/106) |
|----------|-----------|------------------------------|
| Fázis-koherencia (T₂) drift | ✅ igen (43–141 µs) | ❌ nem (r=0.9994, A=1.5076±0.0226) |
| Relaxáció (T₁) drift | ❌ minimális (1,08 ± 0,14) | n/a |
| Echo vs kontroll | különböztetve (3.18σ) | n/a |

**A drift a 91-es qubit lokális környezetéből adódik** — valószínűleg:
1. A 91-es qubit **közel a chip edge-hez vagy egy zajforráshoz** van (a QDS layout `q₈` pozíció, ami a 14-qubit hálón a rezervúár végén van).
2. **Közvetlen kapcsolat a 91-es qubit T₂-jével** a U-delay-U-dagger visszatérési kar időtartományában, amely a wave-quantum ⟨ZZ⟩-ben **nem részt vesz** (a csatorna q₀/q₁-re épül, a 91-es q₈-ként szerepel).

Ez magyarázza, miért hagyja figyelmen kívül a wave-quantum ⟨ZZ⟩ stabil eredményét, miközben a QDS a 91-es qubitet célozza.

## ✅ A wave-quantum validitása (nehámítás nélküli állítás)

A QDS crosstest **nem csak nem cáfolja** a wave-quantum eredményeit, hanem **fellépíti őket** egy független, drift-ellenálló keretben:

- **Run 7**: r = 0.9973, χ²_red = 4.69, σ_sys = 0.0348 (fez, 2048 shots)
- **Run 7b**: r = 0.9989, χ²_red = 2.58, σ_sys = 0.0231 (azonos layout, közvetlenül utána)
- **Ez a 5 futára kiterjedő repeat**: r = 0.9994 ± 0.0001, A = 1.5076 ± 0.0226

**A wave-quantum ⟨ZZ⟩ Rabi-görbe egy **valódi, stabil fizikai jelenség**, nem a qubit-drift artaktikus torzítása.**

## 📄 Eredeti fájlok

- `results/wave_zz_repeat_run{1..5}.json` — egyéni futások (nyers számláló + sorok + kontraszt A)
- `results/wave_zz_repeat_summary.json` — összefoglaló statisztika + verdict
- `qds_wavezz_repeat.py` — a crosstest futtató szkript (a `wave_quantum_v3.py` `build_v3`-jéből)
- `results/raw_counts_all_runs.json` + `results/multirun_stats.json` — a QDS drift adatok

## 🔧 Módszertani megjegyzés

A `qds_wavezz_repeat.py` szkript két hibát tartalmazott:
1. **Python scope-bug:** `mean` válózó generátor-kifejezésben a definíció előtt (`NameError`). Fix: `mean = sum(rs)/len(rs)` külön sor.
2. **Mérőszámi hiányosság:** csak Pearson r-t számol (ami **nem érzéel** a kontrasztokban driftelést). Javítva: hozzáadtuk a **Kontraszt A** (max−min ⟨ZZ⟩) számítást, ami **érzékeny** a driftre.

Mindkét hiba **csak a statisztikai összesítésben** jelentkezett — a 5 QPU futás **mind megvolt** (nyilvántartva `job_id`-val), és a fixelt változat **újraszámolja** a statisztikát a mentett JSON-ekből. **Nincs újrafuttatva a QPU-n.**

---

🔬 **Ez a dokumentum a QDS × wave-quantum kereszttest eredményét rögzíti. A drift a 91-es qubit-specifikus limitáció, a wave-quantum ⟨ZZ⟩ csatorna stabil (r = 0.9994 ± 0.0001, A = 1.5076 ± 0.0226) — a fizikai jelenség valódi.**
