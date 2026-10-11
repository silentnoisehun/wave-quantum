# AZ ELSŐSÉG ÉS TARTALOM PONTOSÍTÁSA (2026-10-11)

## 1. A korábbi állítás felülvizsgálata

A korábbi tervezet azt állította: „bizonyítottan elsők vagyunk abban, hogy egy hullám frekvenciáját kétqubites korrelációvá képeztük zárt tétellel, és ezt hardveren visszaolvastuk”.

**Ez az állítás nem áll meg.**

Az analitikus levezetés és a szimuláció egyértelműen bizonyítja:
1. A mért `⟨Z_readout · Z_partner⟩` paritás az áramkör szimmetriája miatt analitikusan megegyezik a partner qubit saját `⟨Z_partner⟩` várható értékével:
   ```
   ⟨Z₀ · Z₁⟩ = ⟨Z₁⟩ = cos(2π·k/N)
   ```
2. Ez pontosan egyetlen qubit **Rabi-görbéje** az `RX(2πk/N)` forgatás után.
3. A readout qubit (`q₀`) és a 12 további rezervoár-qubit kiesik a megfigyelhetőből: nem hordoznak információt a mérésben, csak kapuhubát és dekoherenciát adnak hozzá.
4. A korábban „no-go tételként” hirdetett állítás (a readout qubit marginálisa nem hordoz frekvencia-információt) triviális: `A=0.5`-nél a readout qubit `|+⟩` állapotban van, a mérés előtti Hadamard után pedig `|0⟩` állapotba esik (`⟨Z₀⟩ = +1`). A partner qubit saját marginálisa viszont **pontosan hordozza** a cos(2πk/N) jelet!

---

## 2. Mi a munka valódi, védhető eredménye?

A munka nem új fizikát és nem új elméleti csatornát mutat be, hanem egy **kísérleti módszertani tanulságot**:

1. **Egy ismert Rabi-görbe demonstrációja 14-qubites transpilált környezetben** — 3 különböző szupravezető Heron QPU-n (`ibm_fez`, `ibm_marrakesh`, `ibm_kingston`), 7 futásban, stabil Pearson korrelációval (0.87–0.999) és kontraszttal (A ≈ 0.50–0.76).
2. **Kísérlettervezési zavaró tényező kimutatása és felszámolása** — a szabad layout esetén a transpiler sávonként más-más fizikai láncot választott (2–4 lánc futásonként), ami szisztematikus szórást okozott (`σ_sys ≈ 0.15–0.19`, `χ²_red ≈ 24–100`). A rögzített layout alkalmazása ezt a szórást ~5-szörösére csökkentette (`σ_sys ≈ 0.023–0.035`, `χ²_red ≈ 2.58–4.69`).
3. **A Falszifikációs Reflex demonstrációja** — a kutatás nyíltan dokumentálja saját tévedéseit (a marginals-hipotézis elbukása, a Z-korreláció elbukása, és végül az a felismerés, hogy a kétqubites tétel valójában egyetlen qubit Rabi-forgatása volt 14-qubites környezetbe ágyazva).

---

## 3. A publikáció tisztességes mondata

> „Demonstráljuk az egyqubites Rabi-oszcilláció viselkedését egy 14-qubites rezervoár-hálózatba transpilálva valós IBM szupravezető processzorokon. Megmutatjuk, hogy a korábban feltételezett kétqubites korrelációs csatorna analitikusan egybeesik a partner qubit marginálisával (`⟨Z₀Z₁⟩ = ⟨Z₁⟩ = cos(2πk/N)`), és a spektátor qubitek kizárólag dekoherenciát és zajt adnak a méréshez. Kimutatjuk a sávonkénti transpiler-layout ingadozás szisztematikus hatását, és rögzített lánccal 5-szörösére csökkentjük a szisztematikus szórást.”
