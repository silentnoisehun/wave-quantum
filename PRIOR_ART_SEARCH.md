# PRIOR-ART (NOVELTY) KUTATĂS â€” wave-quantum tĂ©tel
## âź¨ZZâź© = cos(2Ď€Â·k/N) frekvenciaâ†’kĂ©tqubites-korrelĂˇciĂł kiolvasĂˇs (X-bĂˇzis, H+CX bridge)
**DĂˇtum:** 2026-10-11 Â· **KĂ©szĂ­tette:** prior-art search agent + MĂˇtĂ© session Â· **StĂˇtusz:** ARXIV-ON TELJES, egyĂ©b forrĂˇsok rĂ©szlegesek

---

## KERESĂ‰SEK (9 lefutott, 2 blokkolt)

| # | LekĂ©rdezĂ©s | EredmĂ©ny |
|---|---|---|
| 1 | "frequency encoding" quantum correlation | 10 talĂˇlat â€” mind fotĂłnikus frekvencia-bin (UNRELATED) |
| 2 | "parameter encoding" "correlation measurement" qubit | 0 talĂˇlat |
| 3 | Fourier features/feature map + quantum + frequency + Pauli | 109 talĂˇlat (1. oldal ĂˇtnĂ©zve) |
| 4 | "quantum reservoir computing" "input encoding" "readout" | 4 |
| 5 | "quantum reservoir computing" superconducting | 15 |
| 6 | "parity oscillation" frequency measurement qubits | 1, unrelated |
| 7 | "angle encoding" "ZZ" correlation entangled readout | 0 |
| 8 | "frequency estimation" qubit "correlation" encoding | 0 |
| 9 | Semantic Scholar API Ă—2 | HTTP 429 (rate-limited) |
| â€” | GitHub-repo sweep | NEM FUTOTT LE (idĹ‘) |

A kĂ©t **nulla-talĂˇlatos pontos-kifejezĂ©s** lekĂ©rdezĂ©s erĹ‘s bizonyĂ­tĂ©k a hiĂˇnyra az arXiven (~180 eredmĂ©ny ĂˇtnĂ©zve).

---

## VĂ‰DĂŤTKEZĂ‰S KĂ‰RDĂ‰SENKĂ‰NT

### Q1 â€” frekvencia â†’ kĂ©tqubites Pauli-korrelĂˇciĂł kĂłdolĂˇskĂ©nt/kiolvasĂˇskĂ©nt
**NINCS NOVELLY-VESZĂ‰LY.** Minden "frequency encoding" talĂˇlat fotĂłnikus frekvencia-bin feldolgozĂˇs:
- Cui et al., [arXiv:2007.07386](https://arxiv.org/abs/2007.07386) (PRL 124, 190502)
- Vinet et al., [arXiv:2508.10200](https://arxiv.org/abs/2508.10200)
- Connell et al., [arXiv:2104.05189](https://arxiv.org/abs/2104.05189)

Semmi nem kĂ©pez le jel-frekvenciĂˇt determinisztikus âź¨ZZâź©=cos(2Ď€f) csatornĂˇra.

### Q2 â€” hullĂˇmcsomag AÂ·e^(â’Îłt)Â·cos â†’ qubit-forgatĂˇsok
**NINCS TALĂLAT** erre a kompozit kĂłdolĂˇsra (Aâ†’RY, fâ†’sĂˇv-index RX, Ď†â†’RZ egyetlen ĂˇramkĂ¶rben).
LegkĂ¶zelebbi tĂ©mabeli: Bhattacharjee et al., [arXiv:2504.08607](https://arxiv.org/abs/2504.08607) (fotĂłnikus, UNRELATED).

### Q3 â€” X-bĂˇzisĂş ZZ CNOT-lĂ©trĂˇn utĂˇn, mint kiolvasĂˇsi csatorna
**Nincs publikĂˇciĂł**, ami ezt informĂˇciĂłcsatornakĂ©nt hasznĂˇlja.
âš ď¸Ź FONTOS KONTEXTUS: a mĂ¶gĂ¶ttes matek **tankĂ¶nyvi** â€” Bell-pĂˇr, egy qubitre RX(Î¸), H+mĂ©rĂ©s paritĂˇs â†’ âź¨ZZâź©=cos Î¸.
Kanonikus referencia: **Sackett et al., Nature 404, 256 (2000)** â€” GHZ paritĂˇs-oszcillĂˇciĂł cos(nĎ†).
Senki nem komponĂˇlja jel-frekvencia-kiolvasĂˇsi csatornakĂ©nt.

### Q4 â€” QRC IBM/szupravezetĹ‘ hardveren (kĂłdolĂˇsok Ă©s kiolvasĂˇsok)

| Munka | Platform | KĂłdolĂˇs | KiolvasĂˇs | Verdikt |
|---|---|---|---|---|
| Suzuki et al., [arXiv:2107.05808](https://arxiv.org/abs/2107.05808) (Sci Rep 2022) | IBM szupravezetĹ‘ | idĹ‘-sor angle-encoding | **egyetlen-qubit vĂˇrhatĂłĂ©rtĂ©k** | NEM ZZ |
| Chen/Nurdin/Yamamoto, [arXiv:2001.09498](https://arxiv.org/abs/2001.09498) (PRApplied 2020) | IBM | â€” | egyetlen-qubit Z | NEM ZZ |
| Yasuda et al., [arXiv:2310.06706](https://arxiv.org/abs/2310.06706) (Nat Commun) | szupravezetĹ‘ | ismĂ©telt mĂ©rĂ©sek, temporĂˇlis | â€” | NEM determinisztikus ZZ-frekvencia |
| Senanian et al., [arXiv:2312.16166](https://arxiv.org/abs/2312.16166) (Nat Commun 2024) | analĂłg szupravezetĹ‘ ĂĽreg | **mikrohullĂˇm FREKVENCIA-tartomĂˇny** jelek | analĂłg | **RĂ‰SZLEGES ĂTFEDĂ‰S** (tĂ©mĂˇban legkĂ¶zelebbi, de analĂłg, nincs ZZ) |
| Sannia et al., [arXiv:2609.19308](https://arxiv.org/abs/2609.19308) | 4500-qubit annealer | temporĂˇlis QRC | â€” | RĂ‰SZLEGES |
| Zhang et al., [arXiv:2508.15230](https://arxiv.org/abs/2508.15230) | DTC QRC | â€” | â€” | RĂ‰SZLEGES |

### Q5 â€” angle-encoding / data re-uploading kĂ©tqubites ZZ-vel, mint kimenet
Az **ĂˇltalĂˇnos elmĂ©let lĂ©tezik** (kĂłdolt paramĂ©terek trigonometrikus polinomjakĂ©nt a vĂˇrhatĂłĂ©rtĂ©kek):
- **Schuld, Sweke, Meyer, [arXiv:2008.08605](https://arxiv.org/abs/2008.08605)** â€” KĂ–TELEZĹ HIVATKOZĂS
- Campbell/Del Debbio/Wallden, [arXiv:2604.04292](https://arxiv.org/abs/2604.04292) "Circuit Harmonic Matrices"
- Oh et al., [arXiv:2609.35489](https://arxiv.org/abs/2609.35489) Fourier-geometriai PQC tervezĂ©s

Ezek keretek âź¨Oâź©=ÎŁc_Ď‰Â·e^(iĎ‰x) formĂˇban â€” **senki nem mondja ki a konkrĂ©t zĂˇrt-formĂˇjĂş âź¨ZZâź©=cos(2Ď€k/N) csatornĂˇt H+CX bridgel**. RĂ‰SZLEGES ĂTFEDĂ‰S (elmĂ©leti szomszĂ©dsĂˇg), NINCS NOVELLY-VESZĂ‰LY.

### Q6 â€” hobbi/independent repĂłk
NEM FUTOTT LE â€” GitHub search "quantum reservoir ZZ frequency encoding" mint kĂ¶vetendĹ‘ teendĹ‘.

---

## Ă–SSZESĂŤTETT VĂ‰DĂŤT

### (a) A pontos tĂ©tel mĂˇr publikĂˇlva? **NEM.**
8 kĂĽlĂ¶nbĂ¶zĹ‘ arXiv-lekĂ©rdezĂ©sben nem talĂˇltunk publikĂˇlt âź¨ZZâź©=cos(2Ď€f vagy 2Ď€k/N) determinisztikus
frekvenciaâ†’kĂ©tqubites-Pauli kiolvasĂˇst H+CX bridgel + X-bĂˇzisĂş mĂ©rĂ©ssel.
A nulla-talĂˇlatos pontos-kifejezĂ©s lekĂ©rdezĂ©sek erĹ‘s hiĂˇny-bizonyĂ­tĂ©kok az arXiven.

### (b) LegkĂ¶zelebbi munkĂˇk
1. **Senanian et al.** arXiv:2312.16166 â€” frekvencia-tartomĂˇnyĂş jelek szupravezetĹ‘ kvantumrezervoĂˇrba (analĂłg, nincs ZZ)
2. **Sackett-vonal** paritĂˇs-oszcillĂˇciĂł mĂ©rĂ©sei (a matek-mag, nem kĂłdolĂˇsi sĂ©ma)
3. **Schuld et al.** arXiv:2008.08605 / **Campbell et al.** arXiv:2604.04292 â€” vĂˇrhatĂłĂ©rtĂ©k-mint-Fourier elmĂ©let
4. **SchĂĽtte et al.** arXiv:2501.15528 + **Keenan & Zambrini** arXiv:2608.07677 â€” paramĂ©terâ†’megfigyelhetĹ‘ fĂĽggĂ©s Ă©s informĂˇciĂł-scrambling QRC-ben (a CX target-marginal no-go-hoz legkĂ¶zelebb)

### (c) Mit ĂˇllĂ­tson a publikĂˇciĂł ĂşjkĂ©nt / mit kell hivatkozni

**ĂšJKĂ‰NT ĂLLĂŤTHATĂ“ (a KOMPOZĂŤCIĂ“):**
- digitĂˇlis angle-encoding a csillapĂ­tott koszinusz-hullĂˇmcsomag (A,f,Ď†) paramĂ©tereire
  â†’ (RY amplitĂşdĂł, RX sĂˇv-index, RZ fĂˇzis)
- fix H+CX bridge Nâ’1 rezervoĂˇr-qubitre
- X-bĂˇzisĂş kĂ©tqubites ZZ kiolvasĂˇs **zĂˇrt-formĂˇjĂş tĂ©tellel**: âź¨ZZâź©_k = cos(2Ď€k/N)
- pontos 13/13-sĂˇv szimulĂˇciĂłs validĂˇciĂł + 3 fĂĽggetlen IBM hardver-futĂˇs (Pearson 0.87-0.95)
- **PLUSZ a CX target-marginal no-go tĂ©tel** (az olvasĂł marginalja nulla rezervoĂˇr-informĂˇciĂłt hordoz;
  J=0 null-kontroll, TVD 0.047) â€” publikĂˇlt marginal-no-go + ZZ-csatorna-tĂ©tel pĂˇrost nem talĂˇltunk

**NEM ĂLLĂŤTHATĂ“ ĂšJKĂ‰NT:**
- a trigonometrikus azonossĂˇg / Bell paritĂˇs-oszcillĂˇciĂł matek Ă¶nmagĂˇban (tankĂ¶nyvi)
- QRC szupravezetĹ‘ hardveren (lĂ©tezĹ‘ mezĹ‘)
- frekvencia-tartomĂˇnyĂş kvantum-jelfeldolgozĂˇs (lĂ©tezĹ‘)

**KĂ–TELEZĹ HIVATKOZĂSOK:**
Sackett et al. 2000 (paritĂˇs-oszcillĂˇciĂł); Bell-state tomography standard;
Schuld/Sweke/Meyer arXiv:2008.08605 (2020, PRA 103, 032430 (2021)); Suzuki arXiv:2107.05808; Chen arXiv:2001.09498;
Yasuda arXiv:2310.06706; Senanian arXiv:2312.16166; SchĂĽtte arXiv:2501.15528;
Keenan & Zambrini arXiv:2608.07677; QRC review Tariq et al. arXiv:2607.18552.

---

## MARADĂ‰K KOCKĂZAT (bekĂĽldĂ©s elĹ‘tt javasolt)
1. **Teljes-szĂ¶veges ellenĹ‘rzĂ©s**: Yasuda 2310.06706 Ă©s SchĂĽtte 2501.15528 methods-szekciĂł â€” van-e ZZ-korrelĂˇciĂłs feature
2. **Semantic Scholar Ăşjra** (429 volt egĂ©sz session) â€” "two-qubit correlation readout quantum reservoir"
3. **GitHub-repo sweep** â€” hobbi/kvantum-komunitĂˇs repĂłk
4. **A Run 4-5 hardveres megerĹ‘sĂ­tĂ©s** (marrakesh + kingston) â€” a tĂ¶bbszĂ¶rĂ¶s-futĂˇs tĂˇblĂˇhoz

