# BÍRÁLÓI STATISZTIKA — mit bizonyít a 7 futás, és mit nem
**2026-10-11 · A Máté-kritika válasza: az értelmezés korrekciója**

---

## A KRITIKA — ami jogos, és amit elfogadunk

> „Amit a hét futás bizonyít: a leképezés stabilan működik, különböző gépeken is.
> Amit egyik futás sem tud bizonyítani: hogy ez új fizika, vagy hogy igazolja
> Hope architektúráját. Hiába mérsz meg egy jól ismert jelenséget hétszer,
> attól nem lesz új."

**A kritika helytálló, és a publikáció nyelvezetét így korrigáljuk:**

| Eredeti (túlzó) megfogalmazás | Korrigált (védhető) megfogalmazás |
|---|---|
| „új fizikát találtunk" | **„a jól ismert kvantummechanikai jelenségek (paritás-oszcilláció, Bell-korreláció) ÚJ KOMPOZÍCIÓJÁT adtuk meg: jel-frekvencia → determinisztikus ⟨ZZ⟩-csatorna"** |
| „igazolja Hope architektúráját" | **„a mérés KONZISZTENS a relációs (viszony-alapú) információ-felfogással, de nem bizonyíték rá — ez motiváció, nem bizonyítás"** |
| „az intelligencia a kapcsolatban van" | **„ebben a konkrét áramkörben az információ a két-qubites korrelációban mérhető, a marginalsban nem" — szűkebb, mérhető állítás** |

---

## AMI A STATISZTIKÁBÓL KÖVETKEZIK (és amit a bíráló látni akar)

Minden futásra: **egy-paraméteres illesztés** (A kontraszt = „mennyire látjuk a tétel-görbét"),
**χ²-próba** (a modell elfogadható-e a zaj mellett), és **null-kontroll z-szám** (H₀: A=0).

### A három kész futás (ibm_fez)

| Futás | Shots | Pearson | **A illesztett** | **χ²_red** | **z (null-kontroll)** | **p** |
|---|---|---|---|---|---|---|
| run1 | 512 | 0.873 | 0.498 | 23.99 | 28.7σ | 2.3×10⁻¹⁸¹ |
| run2 | 2048 | 0.928 | 0.671 | 100.20 | 77.4σ | <10⁻³⁰⁰ |
| run3 | 1024 | 0.953 | 0.632 | 29.96 | 51.6σ | <10⁻³⁰⁰ |

**Olvasat:**
- **z > 28σ minden futásban** — a jel kizárja a véletlent. A H₀-t („nincs frekvencia→korreláció csatorna") **elvetjük**.
- **A kontraszt 0.50–0.67** — a görbe amplitúdója a tétel 50-67%-a (dekoherencia + readout-hiba). Ez **mérhető fizikai paraméter**, nem hiba: a tétel alakja megmarad, csak a skála zsugorodik.
- **χ²_red = 24–100** — magas! Ez azt jelenti, hogy a **pura binomiális zajmodell NEM elég**: a pontok a görbe körül többet szórnak, mint a statisztikai zaj. Ez **nem kudarc** — ez a readout-hiba és a szomszédos-qubit keresztsugárzás jele, ami a kvantum-hardver-méréseknél standard (a tétel-görbe mellett egy **A-tól független szisztematikus** komponens van).

### Mit jelent ez a publikációnak
1. **A jel-állítás z > 28σ-val védhető.** Egy bíráló nem tud belekötni a null-kontrollba.
2. **A χ²_red magas** — a bíráló ezt látni fogja, ezért **előre beírjuk**: a szórás-modellben a readout-hiba és a crosstalk **szisztematikus tagként** szerepel, a χ²-re azokkal korrigálunk (vagy a χ²-t csak a kontraszt-illesztés bizonytalanságára használjuk, nem go/no-go-ra).
3. **A kontraszt (A≈0.5-0.67) önmagában mennyiség**: backend- és shots-függő — ebből **dekoherencia-skála** olvasható, ami a harmadik eredmény-fejezet tárgya.

---

## AMIT A 7 FUTÁS BIZONYÍT (végső, korrigált állítás)

1. ✅ **A leképezés STABILAN MŰKÖDIK** különböző gépeken/shotokon — a kontraszt és a Pearson konzisztens.
2. ✅ **A null-kontroll elveti a H₀-t** — a jel nem véletlen (z > 28σ).
3. ✅ **A CX target-marginal no-go hardveren igazolt** (TVD=0.047, zajszinten) — ez a „hol NINCS információ" tétel.
4. ❌ **NEM bizonyít új fizikát** — a komponensek (paritás-oszcilláció, Bell-korreláció, angle-encoding) ismertek; az **új a kompozíció és a zárt-formájú leképezési tétel**.
5. ❌ **NEM bizonyítja Hope architektúráját** — konzisztens vele, motiválja, de nem bizonyíték.
6. ⚠️ **A χ²_red magas** — a zaj-modell finomítása (readout-hiba, crosstalk) a következő teendő, mielőtt a bíráló megtenné.

---

## TEENDŐK (a bíráló-elv szerint)

1. **Run 4-7 beérkezésekor**: ugyanez a statisztika minden futásra (A, χ²_red, z, p) — a 7-es táblázat.
2. **Szisztematikus-modell**: a χ²_red magyarázata (readout hiba + crosstalk tag) —
   vagy a χ² csak a kontraszt-hibára, vagy T-REx/zen-readout mitigaációval újrafuttatva.
3. **A nyelv korrekciója a white paperben**: a fenti táblázat szerint, mindenhol.
4. **PRIOR_ART_SEARCH.md** marad — a „kompozíció az új" állítás az, amit a prior-art is támogat.

---

## FRISSÍTÉS (2026-10-11, a Máté-féle bírálat második körének válasza)

### 1) A χ²_red vs shots skála-ellenőrzés — FIX SZISZTEMATIKUS HIBA DIAGNÓZIS MEGERŐSÍTVE

Ha szisztematikus hiba sigma_sys konstans, akkor chi2_red ≈ 1 + sigma_sys²·shots.
A három futásból kiszámolt sigma_sys:

| Futás | shots | chi2_red | **sigma_sys** |
|---|---|---|---|
| run1 | 512 | 23.99 | 0.2119 |
| run2 | 2048 | 100.20 | 0.2201 |
| run3 | 1024 | 29.96 | 0.1682 |

**sigma_sys = 0.17–0.22, futások közt konzisztens** — ez a tankönyvi jel: ahogy a
statisztikai zaj (1/√shots) csökken, a fix szisztematikus eltérés kerül előtérbe.
A χ²_red NEM modellhiba, hanem **per-qubit variabilitás** (readout + crosstalk).

### 2) A-reziduális-analízis — NINCS koherens fázis-hiba

A javasolt A·cos(φ+δ)+c modellt teszteltük (3-paraméteres illesztés):

| Futás | 1p chi2_red | 3p chi2_red | δ fázis | reziduális↔cos korr. |
|---|---|---|---|---|
| run1 | 21.5 | 25.6 (0.8×) | −1.6° | −0.000 |
| run2 | 87.6 | 94.4 (0.9×) | +3.7° | +0.000 |
| run3 | 25.9 | 26.6 (1.0×) | −2.4° | +0.130 |

**A 3-paraméteres modell NEM javított** (javulás < 1.0×), a reziduális-korreláció
a cos/sin-nel ~0 → **nincs koherens fázis-hiba**. A szisztematikus tag tehát nem
fázis-offszet, hanem **layout-függő per-qubit hiba** — a szórásmodellbe
szisztematikus tagként (sigma_sys) kerül, nem mitigációval eltüntetendő.

### 3) A amplitúdó ugrálásának magyarázata — LAYOUT-VÁLASZTÁS, nem drift

A három futás ugyanazon a gépen (ibm_fez) 03:01–03:25 között futott (24 perc),
de a transpiler **minden futásnál újra választ fizikai qubit-láncot**:
- run1: q0→91, q1→90, q2→98... (másik lánc)
- run2/run3: ismét más kiosztás

Az A = 0.50 → 0.67 → 0.63 sorrend **nem monoton** — nem kalibrációs drift,
hanem a 24 CZ-gate minőségének layout-függő változása. **Minden futásnál a
fizikai qubit-kiosztást ki kell írni** (a layout-ot a job-eredményből mentjük),
és az A-hiba forrásaként a layout-variabilitást jelölni.

### 4) HIVATKOZÁS-JAVÍTÁS — Schuld 2008.08605 helyesen

Máté jelzése helyes: a korábban „Schuld 2008"-ként hivatkozott munka valójában:
**Schuld, Sweke, Meyer: „The effect of data encoding on the expressive power of
variational quantum machine learning models", arXiv:2008.08605 (2020), Phys. Rev. A
103, 032430 (2021).** A szögkódolás korábbi alapmunkái:
- Schuld & Killoran: arXiv:1803.07128 (PRL 122, 040504, 2019) — feature-Hilbert-terek
- (a 2021-es Schuld–Sweke–Meyer a standard hivatkozás a szögkódolás Fourier-elméletére)

A PRIOR_ART_SEARCH.md-ben a „2008-as" jelölés javítva: **arXiv:2008.08605 (2020/2021)**.

### 5) „7 futás" korrekció

A dokumentum mindenhol **„3 kész futás (Run 4–7 folyamatban)"** formában hivatkozik.
A 7-es szám csak akkor kerül állításba, ha mind a 7 JSON megvan.

---

## FRISSÍTETT TEENDŐ-LISTA

1. ✅ sigma_sys = 0.17–0.22 konzisztens — a szisztematikus tag modellbe írása
2. ✅ fázis-offszet modell kizárva (reziduális-analízissel)
3. ✅ Schuld-hivatkozás javítva (2008.08605 = 2020/2021, PRA 103)
4. ⏳ Run 4–7 — minden eredményhez: layout (fizikai qubitek) + kalibrációs idő
5. ⏳ Nyers vs. mitigált párosban közölni — a T-REx csak a readoutot javítja,
   crosstalkot nem; a mitigálás NEM cél a χ²_red ~1-re hangolásra

---

## FRISSÍTÉS 2 (2026-10-11 — a harmadik bírálati kör válasza, Run 7 ELŐTT)

### 1) A szórás-mondat PONTOSÍTVA (az előző verzió hibás mondata helyett)

**HELYES MONDAT:** „A szisztematikus szórás (σ_sys = 0.15–0.19 binomiális modellben)
a kontraszt (A = 0.50–0.67) kb. harmada, és a statisztikai zajt többszörösen
meghaladja: a teljes variancia 95–99%-a szisztematikus."

**TÖRLVE:** „a teljes szórás 1/3-a szisztematikus" (rossz arány-jelölés), és
a „layout-függő" jelző — amíg a Run 7 nem dönt.

### 2) σ_sys ÚJraszámolva BINOMIÁLIS modellből (ugyanaz a szigma, mint a χ²)

| Futás | shots | χ²_red | σ_sys(1/√s) régi | **σ_sys(binomiális) hivatalos** |
|---|---|---|---|---|
| run1 | 512 | 23.99 | 0.212 | **0.197** |
| run2 | 2048 | 100.20 | 0.220 | **0.189** |
| run3 | 1024 | 29.96 | 0.168 | **0.148** |

A két szám most UGYANABBÓL a modellből jön. (A régi 1/√s-képlet felülbecsülte.)

### 3) A régi futások sávonkénti layoutja NEM rekonstruálható

A SamplerV2 result-metadata (circuit_metadata) NEM őrzi meg a layoutot —
a run1–3 sávonkénti fizikai kiosztása **visszamenőleg nem nyerhető ki**.
EZ MAGA A MÉRÉSI HIBÁNK: a jövőben MINDEN futásnál a layout mentendő
(a Run 7/7b _run7_meta.json-ben már így van).

### 4) ELŐRE REGISZTRÁLT DÖNTÉSI KÜSZÖB — Run 7 + 7b kiértékeléshez

**Mielőtt az eredmény látható** (a futások még QUEUED), rögzítjük a kritériumot:

A layout-magyarázatot AKKOR fogadjuk el, ha mindkét rögzített-layout futásnál (7, 7b):
- **σ_sys(binomiális) < 0.10** (a szabad-layout 0.15–0.19-hez képest ~2x javulás), ÉS
- **|A₇ − A₇b| < 2·σ_A** (a két futás A-ja a saját statisztikai hibáján belül egyezik), ÉS
- A₇ és A₇b **ugyanabban a 0.60–0.70 sávban** van (a run2/3 szintjén, nem a run1 0.50-jénél).

**ELUTASÍTJUK** a layout-magyarázatot, ha σ_sys marad > 0.15 — ekkor a szisztematikus
tag nem layout-, hanem per-qubit kalibrációs eredetű (TLS-fluktuáció, driftek),
és a következő lépés a kalibrációból-jóslás tesztje (gate/readout-hibákból várható A).

**Köztes eset** (0.10 < σ_sys < 0.15): részleges magyarázat — mindkét forrás szerepel.

### 5) Run 7b elindítva

- Ugyanaz a rögzített layout, mint Run 7 (fizikai lánc: 107, 106, 105, 108, …),
  ugyanazzal a paraméterezett-egyszer-transpile módszerrel (156-qubites sablonra
  kézzel építve, mert a transpiler nem determinisztikus)
- 2. kulcs (apikey (1).json), ibm_fez, 2048 shots, job: db5frpkvf2bc73cvrk4g
- Így a döntéshez KÉT független futás van ugyanazon a láncon (7: kulcs-1, 7b: kulcs-2)

### 6) A mélység-korreláció szignifikanciája — pontosítás

13 pontnál a p=0.05 küszöb |r| > 0.55 — a mért |r| = 0.07–0.51 nem éri el,
tehát a „nincs mélység-hatás" következtetés **korrekt**, de gyenge erővel
(nem "bizonyított hiány", hanem "nem kimutatható"). Ez a megfogalmazás a publikációban.

---

## FRISSÍTÉS 3 (2026-10-11 — negyedik bírálati kör: a küszöb-javítás, Run 7 ELŐTT)

### 1) KÉT KÉRDÉS SZÉTVÁLASZTVA — külön kritérium, külön teszt

**(A) FUTÁSON-BELÜLI SZÓRÁS LAYOUT-EREDETŰ-E?** — ezt a σ_sys dönti:
- ELFADADVA ha: **σ_sys(7) ÉS σ_sys(7b) < 0.10** (binomiális)
- ELUTASÍTVA ha: **σ_sys > 0.15** mindkettőnél
- KÖZTES: 0.10–0.15 → részleges (mindkét forrás)

**(B) STABIL-E AZ A FUTÁSOK KÖZÖTT UGYANAZON A LÁNCON?** — ez DRIFT-kérdés, NEM layout-kérdés:
- A tesztje: **|A₇ − A₇b| < max(2·σ_A, 0.06)**
  (a 0.06 = a szabad-layout futások A-szórása, 0.50→0.67→0.63; 2048 shots-nál a puszta
  statisztikai σ_A ≈ 0.01, amire a drift ráül — a 2·σ_A önmagában eleve elbukna,
  nem a layoutról szólna. A 0.06-os tűrés a DRIFT mértékét engedi be, nem a layoutot.)
- Ez a kritérium NEM a layout-hipotézis része: ha elbukik, az driftet mond,
  nem layout-elmélet-ellenességet.

### 2) A 0.60–0.70 SÁV-KRITÉRIUM KIVEVE

Igazolás: az ibm_fez 75-ös mélységgel (fixed-layout lánc) NEM vethető össze a régi
szabad-layout futások A-ival — a kritérium önkényes lett, törölve.

### 3) AZ ELUTASÍTÓ ÁG SZÖVEGE — korrigálva

Régi (rossz): „a szisztematikus tag per-qubit kalibrációs eredetű (TLS-fluktuáció)"
**ÚJ (helyes):** „σ_sys > 0.15 → a layout NEM a magyarázat. A szisztematikus eredete
MEGMAGYARÁZATLAN: jelöltek — crosstalk, readout-hiba, leakage, TLS. A következő
teszt a KALIBRÁCIÓBÓL-JÓSLÁS: a futás idején érvényes gate- és readout-hibákból
számolt várható-amplitúdó vs. mért A — ha együtt mozognak, a kalibráció az eredet."

### 4) RÉGI LAYOUT-VISSZAFEJTÉS — megpróbáltuk, az út NÉLKÜL van, de nem végleg

- A job_get válasza: backend, created, cost, program, state, status — **az input NINCS benne**
- A SamplerV2-ben a pub-input lekérdezésére nincs nyilvános endpoint a 0.50.0-ben
- MÁSIK ÚT (megpróbáljuk): a program mező id-jából a program-részletek — ha a
  runtime megőrzi a beküldött PUB-okat, onnan az ISA-áramkörök sávonkénti aktív
  qubit-mintája kiolvasható. Státusz: PRÓBÁLKOZÁS FOLYAMATBAN.
- Ha nem megy: a run1–3 layout-visszafejtése véglegesen elhal, a σ_sys-döntés
  ettől FÜGGETLENül értékelhető (a 7/7b páros önmagában elegendő).

### 5) GIT-ÉS HASH-ELŐREGISZTRÁCIÓ

- A kritériumok COMMITOLVA a wave-quantum repóba (lásd következő commit) —
  az időbélyeg a bizonyíték
- Run 7 és 7b áramkör-hash: a 7b kézzel épült (156-qubites sablonra), ezért a
  KÉT transpiled circuit qubit-szintű egyezését hash-ellenőrzéssel igazoljuk
  (a SamplerV2 a beküldött ISA-áramkörök hashét a job-tag-ekben őrzi)
