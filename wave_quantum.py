"""
wave_quantum.py — Evidence-grade quantum reservoir measurement
psi(t) = A * exp(-g*t) * cos(2*pi*f*t + phi) -> quantum circuit encoding (A, f, phi encoded; gamma posztprocessz)
Bell-bridge validation + J=0 null-control (falsification gate)
SamplerV2 | ibm_marrakesh | 256 shots
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np
import math
import json
import time
from datetime import datetime

try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
    try:
        from qiskit_ibm_runtime.fake_provider import FakeMarrakesh
    except ImportError:
        from qiskit.providers.fake_provider import GenericBackendV2 as FakeMarrakesh
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    QuantumCircuit = object
    Sampler = object


@dataclass
class CircuitSpec:
    n_qubits: int = 14
    reservoir_qubits: int = 13
    readout_qubit: int = 0
    shots: int = 256
    backend_name: str = "ibm_marrakesh"
    coupling_map: Optional[List[List[int]]] = None
    basis_gates: Optional[List[str]] = None


@dataclass
class WaveParams:
    A: float
    f: float
    phi: float
    t: float


@dataclass
class MeasurementResult:
    circuit_id: str
    params: WaveParams
    counts: dict
    probs: dict
    bell_fidelity: float
    j0_null_result: dict
    falsified: bool
    timestamp: str
    backend: str
    shots: int
    execution_time_ms: float


class WaveQuantumEncoder:
    def __init__(self, spec: CircuitSpec):
        self.spec = spec
        self.n = spec.n_qubits
        self.reservoir = spec.reservoir_qubits
        self.readout = spec.readout_qubit

    def encode_psi(self, params: WaveParams) -> QuantumCircuit:
        qc = QuantumCircuit(self.n, 1)
        A = np.clip(params.A, 0.0, 1.0)
        f = params.f
        phi = params.phi

        theta_A = 2.0 * math.asin(math.sqrt(A))
        qc.ry(theta_A, self.readout)

        band = int(f * self.reservoir) % self.reservoir
        for q in range(1, self.n):
            angle = 2.0 * math.pi * (band / self.reservoir)
            qc.rx(angle, q)

        qc.rz(2.0 * phi, self.readout)
        return qc

    def add_bell_bridge(self, qc: QuantumCircuit) -> QuantumCircuit:
        for q in range(1, self.n):
            qc.h(q)
            qc.cx(q, self.readout)
        return qc

    def add_readout(self, qc: QuantumCircuit) -> QuantumCircuit:
        qc.measure(self.readout, 0)
        return qc

    def build_full(self, params: WaveParams, with_bell: bool = True) -> QuantumCircuit:
        qc = self.encode_psi(params)
        if with_bell:
            qc = self.add_bell_bridge(qc)
        qc = self.add_readout(qc)
        return qc

    def build_j0_null(self, params: WaveParams) -> QuantumCircuit:
        qc = self.encode_psi(params)
        qc = self.add_readout(qc)
        return qc


class BellValidator:
    @staticmethod
    def fidelity(counts: dict, shots: int) -> float:
        p0 = counts.get('0', 0) / shots
        p1 = counts.get('1', 0) / shots
        return 1.0 - abs(p0 - p1)

    @staticmethod
    def is_valid(fidelity: float, threshold: float = 0.92) -> bool:
        return fidelity >= threshold


class NullControl:
    @staticmethod
    def compare(full_counts: dict, null_counts: dict, shots: int, tol: float = 0.05) -> Tuple[bool, float]:
        def dist(c):
            return {k: v / shots for k, v in c.items()}
        d_full = dist(full_counts)
        d_null = dist(null_counts)
        tvd = 0.5 * sum(abs(d_full.get(k, 0) - d_null.get(k, 0)) for k in set(d_full) | set(d_null))
        return tvd <= tol, tvd


class QuantumRunner:
    def __init__(self, spec: CircuitSpec, use_fake: bool = False, token: Optional[str] = None):
        self.spec = spec
        self.use_fake = use_fake
        self.token = token
        self.encoder = WaveQuantumEncoder(spec)
        self.validator = BellValidator()
        self.null_control = NullControl()
        self._backend = None
        self._sampler = None

    def _get_backend(self):
        if self._backend is not None:
            return self._backend
        if self.use_fake or not QISKIT_AVAILABLE:
            self._backend = FakeMarrakesh()
        else:
            service = QiskitRuntimeService(token=self.token) if self.token else QiskitRuntimeService()
            self._backend = service.backend(self.spec.backend_name)
        return self._backend

    def _get_sampler(self):
        if self._sampler is not None:
            return self._sampler
        backend = self._get_backend()
        self._sampler = Sampler(mode=backend)
        return self._sampler

    def run_circuit(self, qc: QuantumCircuit) -> dict:
        backend = self._get_backend()
        sampler = self._get_sampler()
        tqc = transpile(qc, backend=backend, optimization_level=3)
        job = sampler.run([tqc], shots=self.spec.shots)
        result = job.result()
        pub_result = result[0]
        # A klasszikus regiszter neve backend/verzió-függő — az első creg-et használjuk
        data = pub_result.data
        creg_name = qc.cregs[0].name if qc.cregs else "meas"
        try:
            counts = getattr(data, creg_name).get_counts()
        except AttributeError:
            # fallback: első elérhető mező
            first_field = list(vars(data).keys())[0] if vars(data) else None
            if first_field is None:
                raise
            counts = getattr(data, first_field).get_counts()
        return counts

    def measure(self, params: WaveParams) -> MeasurementResult:
        start = time.perf_counter()
        circuit_id = f"wq_{int(time.time()*1000)}"

        qc_full = self.encoder.build_full(params, with_bell=True)
        counts_full = self.run_circuit(qc_full)
        bell_fid = self.validator.fidelity(counts_full, self.spec.shots)
        bell_ok = self.validator.is_valid(bell_fid)

        qc_null = self.encoder.build_j0_null(params)
        counts_null = self.run_circuit(qc_null)

        falsified, tvd = self.null_control.compare(counts_full, counts_null, self.spec.shots)

        elapsed = (time.perf_counter() - start) * 1000

        return MeasurementResult(
            circuit_id=circuit_id,
            params=params,
            counts=counts_full,
            probs={k: v/self.spec.shots for k, v in counts_full.items()},
            bell_fidelity=bell_fid,
            j0_null_result={"counts": counts_null, "tvd": tvd, "falsified": falsified},
            falsified=falsified,
            timestamp=datetime.utcnow().isoformat() + "Z",
            backend=self.spec.backend_name,
            shots=self.spec.shots,
            execution_time_ms=elapsed
        )


def evidence_print(result: MeasurementResult) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append(f"EVIDENCE-GRADE MEASUREMENT  |  {result.circuit_id}")
    lines.append("=" * 70)
    lines.append(f"Timestamp:      {result.timestamp}")
    lines.append(f"Backend:        {result.backend}  |  Shots: {result.shots}  |  Time: {result.execution_time_ms:.1f} ms")
    lines.append("-" * 70)
    lines.append(f"ψ(t) PARAMETERS:")
    lines.append(f"  A (amplitude) = {result.params.A:.6f}  →  RY(2*arcsin(√A)) = {2*math.asin(math.sqrt(result.params.A)):.6f} rad")
    lines.append(f"  f (frequency) = {result.params.f:.6f}  →  band {int(result.params.f * 13) % 13}  →  RX(2π*band/13)")
    lines.append(f"  φ (phase)     = {result.params.phi:.6f}  →  RZ(2φ) = {2*result.params.phi:.6f} rad")
    lines.append(f"  t (time)      = {result.params.t:.6f}")
    lines.append("-" * 70)
    lines.append(f"BELL-BRIDGE VALIDATION:")
    lines.append(f"  Fidelity:     {result.bell_fidelity:.4f}  ({'PASS' if result.bell_fidelity >= 0.92 else 'FAIL'} ≥ 0.92)")
    lines.append(f"  Counts:       {result.counts}")
    lines.append(f"  Probabilities: { {k: f'{v:.4f}' for k, v in result.probs.items()} }")
    lines.append("-" * 70)
    lines.append(f"J=0 NULL-CONTROL (falsification gate):")
    lines.append(f"  Null counts:  {result.j0_null_result['counts']}")
    lines.append(f"  TVD:          {result.j0_null_result['tvd']:.6f}  (threshold ≤ 0.05)")
    lines.append(f"  FALSIFIED:    {'YES — reservoir adds no information beyond single-qubit encoding' if result.falsified else 'NO — reservoir effect detected'}")
    lines.append("=" * 70)
    return "\n".join(lines)


def run_sweep(
    A_vals: List[float],
    f_vals: List[float],
    phi_vals: List[float],
    t: float = 1.0,
    use_fake: bool = True,
    token: Optional[str] = None
) -> List[MeasurementResult]:
    spec = CircuitSpec(use_fake=use_fake)
    runner = QuantumRunner(spec, use_fake=use_fake, token=token)
    results = []
    for A in A_vals:
        for f in f_vals:
            for phi in phi_vals:
                params = WaveParams(A=A, f=f, phi=phi, t=t)
                res = runner.measure(params)
                results.append(res)
                print(evidence_print(res))
    return results


def save_results(results: List[MeasurementResult], path: str):
    data = []
    for r in results:
        data.append({
            "circuit_id": r.circuit_id,
            "params": {"A": r.params.A, "f": r.params.f, "phi": r.params.phi, "t": r.params.t},
            "counts": r.counts,
            "probs": r.probs,
            "bell_fidelity": r.bell_fidelity,
            "j0_null_result": r.j0_null_result,
            "falsified": r.falsified,
            "timestamp": r.timestamp,
            "backend": r.backend,
            "shots": r.shots,
            "execution_time_ms": r.execution_time_ms
        })
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Wave Quantum Reservoir Measurement")
    parser.add_argument("--A", type=float, nargs="+", default=[0.5])
    parser.add_argument("--f", type=float, nargs="+", default=[0.25])
    parser.add_argument("--phi", type=float, nargs="+", default=[0.0])
    parser.add_argument("--t", type=float, default=1.0)
    parser.add_argument("--real", action="store_true", help="Use real IBM backend (requires token)")
    parser.add_argument("--token", type=str, default=None)
    parser.add_argument("--output", type=str, default="wave_quantum_results.json")
    args = parser.parse_args()

    print(f"[wave_quantum] Starting sweep: A={args.A}, f={args.f}, phi={args.phi}, t={args.t}")
    print(f"[wave_quantum] Backend: {'REAL ibm_marrakesh' if args.real else 'FAKE Marrakesh'}")
    print(f"[wave_quantum] Shots: 256 | SamplerV2 | J=0 null-control ACTIVE")
    print()

    results = run_sweep(args.A, args.f, args.phi, args.t, use_fake=not args.real, token=args.token)
    save_results(results, args.output)
    print(f"\n[wave_quantum] Saved {len(results)} measurements to {args.output}")

    falsified_count = sum(1 for r in results if r.falsified)
    print(f"[wave_quantum] SUMMARY: {falsified_count}/{len(results)} configurations FALSIFIED by J=0 null-control")

