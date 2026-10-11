# wave-quantum

**A hullám-kvantum számítás új verziója — Hope saját verziója.**

> psi(t) = A · exp(−γt) · cos(2πft + φ)
> A = amplitúdó (intenzitás) · f = frekvencia (tartalom) · φ = fázis (kontextus) · γ = csillapítás (posztprocessz, NEM kapu)

**Szerző:** Hope (Máté gerincén) · **Dátum:** 2026-10-10 · **Backend:** IBM `ibm_marrakesh` (156Q Heron r2)

## Mi ez

A scs-quantum (hardveresen validált kvantumhíd) + quantum-anchor (Tesseract, negatív eredményekkel) + scs tár (J=0 falszifikációs lecke) tanulságainak **egyesítése**:
minden méréshez **J=0 null-kontroll tartozik**. Ha a null-kontroll ugyanazt adja, a feltevést a Falszifikációs Reflex cáfolja — nem a hope, hanem a mért adat.

## Futtatás

```bash
# Szimuláció (fake backend, gyors ellenőrzés)
python wave_quantum.py --A 0.5 --f 0.25 --phi 0.0

# VALÓDI HARDVER (IBM token kell)
python wave_quantum.py --A 0.5 --f 0.25 --phi 0.0 --real --token <IBMTOKEN>
```

## Evidence-grade rendszer

| Jel | Jelentés |
|---|---|
| 🔬 | Hardveresen mérve |
| ✅ | Szimulációval igazolva |
| ⚠️ | Mérésfüggő / feltevés |
| ❌ | Nem bizonyított |
| 🔴 | Visszavont |

## A J=0 lecke (a scs tárból)

A J=0 konfiguráció (0 kétqubitos gate) hardveren **pontosan ugyanazt** adja, ha a mechanizmus csak klasszikus kódkönyv. A wave-quantum MINDEN mérést ehhez viszonyít: `TVD ≤ 0.05` → FALSIFIED.

## Struktúra

```
wave_quantum.py            — a teljes mérőrendszer (Hope kódja)
_hope_original_output.txt  — a Hope eredeti kimenete (audit)
_hardware_job_id.txt       — futó hardver-job azonosító
```
