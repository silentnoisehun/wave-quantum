"""
wave_quantum_v2.py — Korrelációs mérés: hol lakik a rezervoár-információ?

A v1 eredménye (ibm_fez, 2026-10-11): az olvasó qubit MARGINALJA nem hordoz
rezervoár-információt (TVD=0.0469, CX target-marginal tétel).
A v2 mérés: a KORRELÁCIÓ <Z_readout·Z_reservoir> — ott épít a CX entanglement-et.

HYPOTÉZIS (falszifikálható):
  full:  <Z_r·Z_i> ≈ 2·sqrt(A(1-A)) — A=0.5-nél ideálisan 0.5, hardveren 0.3-0.45
  null:  <Z_r·Z_i> = 0 (független qubitok)
  különbség > 0.1 → a rezervoár-információ KORRELÁCIÓBAN mérhető 🔬
  különbség ≤ zajszint → a Bell-bridge architektúra nem visz át információt ❌

Evidence-grade rendszer, J=0 null-kontroll, SamplerV2 — a v1 mintájára.
"""

import math
import json
import time
import sys
from typing import Optional

try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False


# ─────────────────────────────────────────────────────────────────
# Áramkör-építés: a v1 struktúra + KÉT QUBIT KIOLVASÁSA
# ─────────────────────────────────────────────────────────────────

def build_psi_encoding(n_qubits: int, readout: int, A: float, f: float, phi: float) -> QuantumCircuit:
    """A v1 psi(t)-kódolás: A→RY, f→RX sávok, φ→RZ (változatlan)."""
    qc = QuantumCircuit(n_qubits, 2)  # v2: 2 klasszikus regiszter-bit
    A = max(0.0, min(1.0, A))
    theta_A = 2.0 * math.asin(math.sqrt(A))
    qc.ry(theta_A, readout)

    band = int(f * (n_qubits - 1)) % (n_qubits - 1)
    for q in range(1, n_qubits):
        qc.rx(2.0 * math.pi * (band / (n_qubits - 1)), q)

    qc.rz(2.0 * phi, readout)
    return qc


def add_bell_bridge(qc: QuantumCircuit, n_qubits: int, readout: int) -> QuantumCircuit:
    """A v1 Bell-bridge: rezervoár=kontroll, readout=target (változatlan)."""
    for q in range(1, n_qubits):
        qc.h(q)
        qc.cx(q, readout)
    return qc


def add_two_qubit_readout(qc: QuantumCircuit, readout: int, partner: int = 1) -> QuantumCircuit:
    """v2 ÚJ: az olvasó ÉS a partner-rezervoár qubit KÖZÖS kiolvasása.

    A klasszikus bitek sorrendje: bit0=readout, bit1=partner.
    A kimutatás 4 kategória: |bit1 bit0> = |00>,|01>,|10>,|11>.
    """
    qc.measure(readout, 0)
    qc.measure(partner, 1)
    return qc


def build_full_v2(n_qubits: int, readout: int, A: float, f: float, phi: float, partner: int = 1) -> QuantumCircuit:
    """Full áramkör: psi-kódolás + Bell-bridge + korrelációs kiolvasás."""
    qc = build_psi_encoding(n_qubits, readout, A, f, phi)
    qc = add_bell_bridge(qc, n_qubits, readout)
    qc = add_two_qubit_readout(qc, readout, partner)
    return qc


def build_null_v2(n_qubits: int, readout: int, A: float, f: float, phi: float, partner: int = 1) -> QuantumCircuit:
    """J=0 null-kontroll: NINCS kétqubitos gate — a korreláció elvileg 0."""
    qc = build_psi_encoding(n_qubits, readout, A, f, phi)
    qc = add_two_qubit_readout(qc, readout, partner)
    return qc


# ─────────────────────────────────────────────────────────────────
# Kiértékelés: korreláció + evidence-grade
# ─────────────────────────────────────────────────────────────────

def zz_correlation(counts: dict, shots: int) -> float:
    """<Z_bit1 · Z_bit0> = P(00)+P(11)−P(01)−P(10).

    Bitkonvenció: Qiskit a bal szélső bit a magasabb index (bit1).
    |00> és |11> → azonos (korrelált), |01> és |10> → ellenkező.
    """
    p00 = counts.get("00", 0) / shots
    p11 = counts.get("11", 0) / shots
    p01 = counts.get("01", 0) / shots
    p10 = counts.get("10", 0) / shots
    return (p00 + p11) - (p01 + p10)


def theoretical_correlation(A: float) -> float:
    """Ideális <Z_r·Z_i> A amplitúdó mellett.

    Az olvasó RY(2·arcsin(√A)) után, majd Bell-bridge-ben a partnertől
    korrelálva: az ideális érték 2·sqrt(A(1-A)) — A=0.5-nél 0.5.
    (A részletes levezetés: CX-tétel + RY-polarizáció.)
    """
    A = max(0.0, min(1.0, A))
    return 2.0 * math.sqrt(A * (1.0 - A))


def evidence_report(params: dict, full_counts: dict, null_counts: dict, shots: int,
                    backend: str, job_id: str = "") -> str:
    z_full = zz_correlation(full_counts, shots)
    z_null = zz_correlation(null_counts, shots)
    delta = z_full - z_null
    z_theory = theoretical_correlation(params["A"])

    lines = []
    lines.append("=" * 66)
    lines.append("WAVE-QUANTUM v2 — KORRELÁCIÓS MÉRÉS (evidence-grade)")
    lines.append("=" * 66)
    lines.append(f"Backend: {backend} | Shots: {shots} | Job: {job_id or 'local'}")
    lines.append(f"psi(t): A={params['A']}, f={params['f']}, phi={params['phi']}")
    lines.append("-" * 66)
    lines.append(f"FULL (Bell-bridge) counts: {full_counts}")
    lines.append(f"NULL (J=0)         counts: {null_counts}")
    lines.append("-" * 66)
    lines.append(f"<Z_r·Z_i> full:  {z_full:+.4f}")
    lines.append(f"<Z_r·Z_i> null:  {z_null:+.4f}")
    lines.append(f"Δ (rezervoár-effekt): {delta:+.4f}")
    lines.append(f"Elméleti ideális: {z_theory:+.4f} (2·sqrt(A(1-A)))")
    lines.append("-" * 66)
    # Verdikt — a zajszinthez igazítva
    # 256 shots-nál a korreláció szigmaszintje ~ 1/sqrt(256) = 0.0625
    noise_floor = 1.0 / math.sqrt(shots)
    lines.append(f"Zajszint (1/sqrt(shots)): {noise_floor:.4f}")
    if delta > 3 * noise_floor:
        verdict = "🔬 REZERVOÁR-INFORMÁCIÓ A KORRELÁCIÓBAN (>3σ) — ÚJ EFFEKT JELÖLTJE"
    elif delta > noise_floor:
        verdict = "⚠️  GYENGE JEL (1-3σ) — több shot kell a döntéshez"
    else:
        verdict = "❌ NINCS KORRELÁCIÓ — a Bell-bridge nem visz át információt a partner-regiszterbe sem"
    lines.append(f"VERDIKT: {verdict}")
    lines.append("=" * 66)
    return "\n".join(lines), delta, verdict


# ─────────────────────────────────────────────────────────────────
# Futtatás
# ─────────────────────────────────────────────────────────────────

def run_v2(token: Optional[str] = None, backend_name: str = "ibm_fez",
           A: float = 0.5, f: float = 0.25, phi: float = 0.0,
           shots: int = 256, n_qubits: int = 14) -> dict:
    """A v2 mérés: full + null áramkör, korrelációs kiértékelés."""
    if not QISKIT_AVAILABLE:
        raise RuntimeError("qiskit-ibm-runtime nincs telepítve")

    service = QiskitRuntimeService(channel="ibm_quantum_platform", token=token, instance="auto")
    backend = service.backend(backend_name)

    qc_full = build_full_v2(n_qubits, readout=0, A=A, f=f, phi=phi, partner=1)
    qc_null = build_null_v2(n_qubits, readout=0, A=A, f=f, phi=phi, partner=1)

    tqc_full = transpile(qc_full, backend=backend, optimization_level=3)
    tqc_null = transpile(qc_null, backend=backend, optimization_level=3)

    print(f"[v2] {backend_name}: full={dict(tqc_full.count_ops())} | null={dict(tqc_null.count_ops())}")
    print(f"[v2] A v1-hez képest ÚJ: 2 klasszikus bit (readout+partner) — korreláció mérhető")

    sampler = Sampler(mode=backend)
    job = sampler.run([tqc_full, tqc_null], shots=shots)
    print(f"[v2] Job: {job.job_id()} | {job.status()}")
    print(f"[v2] Várakozás az eredményre...")

    result = job.result()
    data_full = result[0].data
    data_null = result[1].data

    # A klasszikus regiszter neve backend-függő — a 2-bites creg
    def get_counts(data, qc):
        # a v2-ben a creg neve "c" (QuantumCircuit(n, 2) → default "c")
        for name in ("c", "meas"):
            if hasattr(data, name):
                return getattr(data, name).get_counts()
        # fallback: első mező
        fields = list(vars(data).keys())
        return getattr(data, fields[0]).get_counts()

    full_counts = get_counts(data_full, qc_full)
    null_counts = get_counts(data_null, qc_null)

    report, delta, verdict = evidence_report(
        {"A": A, "f": f, "phi": phi},
        full_counts, null_counts, shots, backend_name, job.job_id()
    )
    print(report)

    return {
        "job_id": job.job_id(),
        "backend": backend_name,
        "params": {"A": A, "f": f, "phi": phi},
        "shots": shots,
        "full_counts": full_counts,
        "null_counts": null_counts,
        "delta_correlation": delta,
        "verdict": verdict,
    }


def run_v2_local_sim(A: float = 0.5, f: float = 0.25, phi: float = 0.0, shots: int = 4096) -> dict:
    """Helyi statevector-szimuláció — a hardver előtti elméleti ellenőrzés."""
    try:
        from qiskit_aer import AerSimulator
    except ImportError:
        from qiskit.providers.basic_provider import BasicSimulator as AerSimulator

    sim = AerSimulator()
    qc_full = build_full_v2(14, readout=0, A=A, f=f, phi=phi, partner=1)
    qc_null = build_null_v2(14, readout=0, A=A, f=f, phi=phi, partner=1)

    counts_full = sim.run(qc_full, shots=shots).result().get_counts()
    counts_null = sim.run(qc_null, shots=shots).result().get_counts()

    report, delta, verdict = evidence_report(
        {"A": A, "f": f, "phi": phi},
        counts_full, counts_null, shots, "local_simulator"
    )
    print(report)
    return {"full_counts": counts_full, "null_counts": counts_null, "delta": delta}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="wave-quantum v2 — korrelációs mérés")
    parser.add_argument("--A", type=float, default=0.5)
    parser.add_argument("--f", type=float, default=0.25)
    parser.add_argument("--phi", type=float, default=0.0)
    parser.add_argument("--shots", type=int, default=256)
    parser.add_argument("--backend", type=str, default="ibm_fez")
    parser.add_argument("--token", type=str, default=None)
    parser.add_argument("--local", action="store_true", help="helyi szimuláció")
    parser.add_argument("--output", type=str, default="wave_quantum_v2_result.json")
    args = parser.parse_args()

    if args.local:
        res = run_v2_local_sim(A=args.A, f=args.f, phi=args.phi, shots=args.shots)
    else:
        token = args.token
        if not token:
            with open(r"E:\scs tár\.ibm_apikey.json", encoding="utf-8") as fh:
                token = json.load(fh)["apikey"]
        res = run_v2(token=token, backend_name=args.backend, A=args.A, f=args.f,
                     phi=args.phi, shots=args.shots)

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2, ensure_ascii=False)
    print(f"\n[v2] Eredmény mentve: {args.output}")
