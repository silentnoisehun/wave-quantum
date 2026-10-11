"""
wave_quantum_v3.py — Rabi-görbe demonstráció 14-qubit-es routinggal.

FIZIKAI ALAP:
    A mérés a partner qubiton (q1) elforgatott állapot ⟨Z1⟩ Rabi-görbéjét adja:
        ⟨Z1⟩ = cos(2·pi·band/13)
    ahol band = int(f·13).
    A readout qubit (q0) A=0.5, phi=0 esetén a |+> állapotból indul és a mérés
    előtti H kapu után |0> állapotba kerül, így ⟨Z0⟩ = +1.
    Ezért a kétqubites paritás:
        ⟨Z0 · Z1⟩ = (+1) · ⟨Z1⟩ = cos(2·pi·band/13).
"""

import math
import json
import os
import argparse
from typing import Optional, Dict

try:
    from qiskit import QuantumCircuit, transpile
    from qiskit.circuit import Parameter
    from qiskit.quantum_info import Statevector, Pauli
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False


def build_v3(n_qubits: int, readout: int, partner: int, A: float, f: float, phi: float) -> "QuantumCircuit":
    """v3 áramkör: psi-kódolás + Bell-bridge + X-bázisú kiolvasás."""
    qc = QuantumCircuit(n_qubits, 2)
    theta_A = 2.0 * math.asin(math.sqrt(max(0.0, min(1.0, A))))
    qc.ry(theta_A, readout)

    band = int(f * (n_qubits - 1)) % (n_qubits - 1)
    for q in range(1, n_qubits):
        qc.rx(2.0 * math.pi * (band / (n_qubits - 1)), q)

    qc.rz(2.0 * phi, readout)

    # Bell-bridge
    for q in range(1, n_qubits):
        qc.h(q)
        qc.cx(q, readout)

    # X-bázisba fordítás a mérés ELŐTT
    qc.h(readout)
    qc.h(partner)

    qc.measure(readout, 0)
    qc.measure(partner, 1)
    return qc


def run_local_sweep(n_qubits: int = 14) -> dict:
    """Szimulációs sweep kvóta nélkül (Statevector): 13 sáv ellenőrzése."""
    N = n_qubits - 1
    print("\n" + "=" * 68)
    print("SZIMULACIOS SWEEP -- 13 sav Statevector analizissel")
    print("=" * 68)
    print(f"{'band':>5} {'elmelet':>10} {'<ZZ>':>10} {'<Z1> partner':>14} {'<Z0> readout':>14}")
    
    rows = []
    for k in range(N):
        qc = build_v3(n_qubits, 0, 1, 0.5, k / N, 0.0).remove_final_measurements(inplace=False)
        sv = Statevector.from_instruction(qc)
        theory = math.cos(2.0 * math.pi * k / N)
        zz = sv.expectation_value(Pauli("I" * (n_qubits - 2) + "ZZ")).real
        z1 = sv.expectation_value(Pauli("I" * (n_qubits - 2) + "ZI")).real
        z0 = sv.expectation_value(Pauli("I" * (n_qubits - 1) + "Z")).real
        
        print(f"{k:>5} {theory:>+10.4f} {zz:>+10.4f} {z1:>+14.4f} {z0:>+14.4f}")
        rows.append({"band": k, "theory": theory, "zz": zz, "z1": z1, "z0": z0})
        
    print("-" * 68)
    print("Megfigyeles: <ZZ> == <Z1> mind a 13 savon, mert <Z0> == +1.0000.")
    print("A mert korrelacio pontosan a partner qubit egyedi Rabi-gorbeje!")
    print("=" * 68)
    return {"rows": rows}


def resolve_token(token: Optional[str] = None) -> Optional[str]:
    """API token feloldása CLI argból, környezeti változóból vagy helyi fájlból."""
    if token:
        return token
    for env_var in ("IBM_QUANTUM_TOKEN", "QISKIT_IBM_TOKEN"):
        if env_var in os.environ and os.environ[env_var].strip():
            return os.environ[env_var].strip()
    candidate_paths = [
        os.path.join(os.path.expanduser("~"), ".ibm_apikey.json"),
        os.path.join(os.path.expanduser("~"), "Downloads", "apikey (2).json"),
        os.path.join(os.path.expanduser("~"), "Downloads", "apikey.json"),
        r"E:\scs tár\.ibm_apikey.json"
    ]
    for p in candidate_paths:
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as fh:
                    data = json.load(fh)
                    k = data.get("apikey") or data.get("apiKey")
                    if k:
                        return k
            except Exception:
                pass
    return None


def run_theorem_sweep(token: Optional[str] = None, backend_name: str = "ibm_fez",
                      shots: int = 2048, fixed_layout: bool = True) -> dict:
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

    tok = resolve_token(token)
    service = QiskitRuntimeService(channel="ibm_quantum_platform", token=tok, instance="auto")
    backend = service.backend(backend_name)

    N = 13
    circuits = []
    
    if fixed_layout:
        meta_path = os.path.join(os.path.dirname(__file__), "_run7_meta.json")
        if os.path.exists(meta_path):
            phys14 = json.load(open(meta_path))["physical_qubits"]
        else:
            phys14 = [107, 106, 105, 108, 109, 110, 111, 98, 91, 92, 93, 94, 95, 99]

        band_angles = [Parameter(f"b_{i}") for i in range(1, 14)]
        theta_A = Parameter("A_t")
        theta_phi = Parameter("phi_t")
        qc_param = QuantumCircuit(14, 2)
        qc_param.ry(theta_A, 0)
        for i, q in enumerate(range(1, 14)):
            qc_param.rx(band_angles[i], q)
        qc_param.rz(theta_phi, 0)
        for q in range(1, 14):
            qc_param.h(q)
            qc_param.cx(q, 0)
        qc_param.h(0)
        qc_param.h(1)
        qc_param.measure(0, 0)
        qc_param.measure(1, 1)

        tqc = transpile(qc_param, backend=backend, initial_layout=phys14, optimization_level=3)
        for k in range(N):
            ang = 2.0 * math.pi * k / N
            binds = {theta_A: 2.0 * math.asin(math.sqrt(0.5)), theta_phi: 0.0}
            for p in band_angles:
                binds[p] = ang
            circuits.append(tqc.assign_parameters(binds))
    else:
        for k in range(N):
            circuits.append(transpile(build_v3(14, 0, 1, 0.5, k / N, 0.0), backend=backend, optimization_level=3))

    sampler = Sampler(mode=backend)
    job = sampler.run(circuits, shots=shots)
    print(f"[v3] Job: {job.job_id()} | Backend: {backend_name} | {len(circuits)} circuits, {shots} shots")
    res = job.result()

    rows = []
    for k in range(N):
        item = res[k].data
        counts = None
        for name in ("c", "meas"):
            if hasattr(item, name):
                counts = getattr(item, name).get_counts(); break
        if counts is None:
            counts = getattr(item, list(vars(item).keys())[0]).get_counts()

        p00 = counts.get("00", 0) / shots
        p11 = counts.get("11", 0) / shots
        p01 = counts.get("01", 0) / shots
        p10 = counts.get("10", 0) / shots
        zz = (p00 + p11) - (p01 + p10)
        theory = math.cos(2.0 * math.pi * k / N)
        rows.append({"band": k, "measured_zz": zz, "theory_zz": theory, "counts": counts})

    return {"job_id": job.job_id(), "backend": backend_name, "shots": shots, "rows": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wave-Quantum v3 CLI")
    parser.add_argument("--sweep", action="store_true", help="Futtasson lokális szimulációs sweepet (nem igényel IBM fiókot)")
    parser.add_argument("--backend", default="ibm_fez", help="IBM Quantum backend név")
    parser.add_argument("--shots", type=int, default=2048, help="Mérések száma")
    parser.add_argument("--fixed-layout", action="store_true", dest="fixed_layout", default=True, help="Rögzített fizikai layout használata (alapértelmezett)")
    parser.add_argument("--free-layout", action="store_false", dest="fixed_layout", help="Szabad layout használata (mint a korai Run 1-4 futásoknál)")
    parser.add_argument("--token", default=None, help="IBM Quantum API kulcs")
    parser.add_argument("--output", default="wave_quantum_v3_result.json", help="Kimeneti fájl")
    args = parser.parse_args()

    if args.sweep:
        run_local_sweep()
    else:
        res = run_theorem_sweep(token=args.token, backend_name=args.backend, shots=args.shots, fixed_layout=args.fixed_layout)
        with open(args.output, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=2)
        print(f"Eredmény mentve: {args.output}")
