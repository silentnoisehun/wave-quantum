import json, math, os, sys
sys.path.insert(0, r"D:\codex\wave-quantum")
from _eval_decisive_suite import evaluate_job

# Evaluate marrakesh job:
meta_m = json.load(open(r"D:\codex\wave-quantum\_decisive_marrakesh_job_meta.json"))
# Write a customized eval for marrakesh:
downloads = os.path.join(os.path.expanduser("~"), "Downloads")
with open(os.path.join(downloads, "apikey (1).json"), encoding="utf-8") as fh:
    token = json.load(fh)["apikey"]
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService(channel="ibm_quantum_platform", token=token, instance="auto")
job = service.job(meta_m["job_id"])
res = job.result()
mmap = meta_m["metadata_map"]
shots = meta_m["shots"]

data_entries = []
for entry in mmap:
    idx = entry["index"]
    item = res[idx].data
    counts = None
    for cn in ("c", "meas"):
        if hasattr(item, cn):
            counts = getattr(item, cn).get_counts(); break
    if counts is None:
        counts = getattr(item, list(vars(item).keys())[0]).get_counts()
    
    if entry["type"] == "1q_sweep":
        p0 = counts.get("0", 0) / shots
        p1 = counts.get("1", 0) / shots
        z = p0 - p1
        entry_res = {**entry, "counts": counts, "measured_z": z}
    else:
        p00 = counts.get("00", 0) / shots
        p11 = counts.get("11", 0) / shots
        p01 = counts.get("01", 0) / shots
        p10 = counts.get("10", 0) / shots
        zz = (p00 + p11) - (p01 + p10)
        z0 = (counts.get("00",0) + counts.get("10",0) - counts.get("01",0) - counts.get("11",0)) / shots
        z1 = (counts.get("00",0) + counts.get("01",0) - counts.get("10",0) - counts.get("11",0)) / shots
        entry_res = {**entry, "counts": counts, "measured_zz": zz, "measured_z0": z0, "measured_z1": z1}
    data_entries.append(entry_res)

def analyze_sweep(entries, key="measured_zz"):
    meas = [e[key] for e in entries]
    theo = [e["theory"] for e in entries]
    N = len(meas)
    m_m, m_t = sum(meas)/N, sum(theo)/N
    den = math.sqrt(sum((m-m_m)**2 for m in meas)*sum((t-m_t)**2 for t in theo))
    pearson = sum((m-m_m)*(t-m_t) for m,t in zip(meas,theo)) / den if den > 0 else 0
    A = sum(m*t for m,t in zip(meas,theo)) / sum(t*t for t in theo)
    chi2 = sum(((m - A*t) / math.sqrt(max(1.0 - (A*t)**2, 1e-9)/shots))**2 for m,t in zip(meas,theo))
    chi2_red = chi2 / (N - 1)
    mean_inv_var = sum(1.0/max(1.0-(A*t)**2, 1e-9) for t in theo)/N
    sigma_sys = math.sqrt(max(chi2_red-1.0, 0.0) / (shots * mean_inv_var))
    return {"A": A, "pearson": pearson, "chi2_red": chi2_red, "sigma_sys": sigma_sys, "meas": meas}

sweep_1q = [e for e in data_entries if e["type"] == "1q_sweep"]
sweep_2q = [e for e in data_entries if e["type"] == "2q_sweep"]
sweep_14q = [e for e in data_entries if e["type"] == "14q_sweep"]

res_1q = analyze_sweep(sweep_1q, key="measured_z")
res_2q_zz = analyze_sweep(sweep_2q, key="measured_zz")
res_2q_z1 = analyze_sweep(sweep_2q, key="measured_z1")
res_14q_zz = analyze_sweep(sweep_14q, key="measured_zz")
res_14q_z1 = analyze_sweep(sweep_14q, key="measured_z1")

a_sweep = [e for e in data_entries if e["type"] == "A_sweep"]
phi_sweep = [e for e in data_entries if e["type"] == "phi_sweep"]

print("\n" + "="*75)
print("MARRAKESH DECISIVE EXPERIMENT RESULTS (2048 shots, IBM Heron)")
print("="*75)
print(f"1-qubit (partner q88 only)   : Contrast A = {res_1q['A']:.4f}, Pearson = {res_1q['pearson']:.4f}, chi2_red = {res_1q['chi2_red']:.2f}, sigma_sys = {res_1q['sigma_sys']:.4f}")
print(f"2-qubit <ZZ> (q89, q88)     : Contrast A = {res_2q_zz['A']:.4f}, Pearson = {res_2q_zz['pearson']:.4f}, chi2_red = {res_2q_zz['chi2_red']:.2f}, sigma_sys = {res_2q_zz['sigma_sys']:.4f}")
print(f"2-qubit <Z1> (partner marg) : Contrast A = {res_2q_z1['A']:.4f}, Pearson = {res_2q_z1['pearson']:.4f}, chi2_red = {res_2q_z1['chi2_red']:.2f}, sigma_sys = {res_2q_z1['sigma_sys']:.4f}")
print(f"14-qubit <ZZ>               : Contrast A = {res_14q_zz['A']:.4f}, Pearson = {res_14q_zz['pearson']:.4f}, chi2_red = {res_14q_zz['chi2_red']:.2f}, sigma_sys = {res_14q_zz['sigma_sys']:.4f}")
print(f"14-qubit <Z1> (partner marg): Contrast A = {res_14q_z1['A']:.4f}, Pearson = {res_14q_z1['pearson']:.4f}, chi2_red = {res_14q_z1['chi2_red']:.2f}, sigma_sys = {res_14q_z1['sigma_sys']:.4f}")

print("\nA-SWEEP (14-qubit, fixed band k=2, phi=0.0):")
for e in a_sweep:
    print(f"  A = {e['A']:.1f} -> <ZZ> = {e['measured_zz']:+.4f}, <Z1> = {e['measured_z1']:+.4f}, <Z0> = {e['measured_z0']:+.4f} (theory={e['theory']:+.4f})")

print("\nPHI-SWEEP (14-qubit, fixed band k=2, A=0.5):")
for e in phi_sweep:
    print(f"  phi = {e['phi']:.1f} -> <ZZ> = {e['measured_zz']:+.4f}, <Z1> = {e['measured_z1']:+.4f}, <Z0> = {e['measured_z0']:+.4f} (theory={e['theory']:+.4f})")
print("="*75)

out = {
    "job_id": meta_m["job_id"],
    "backend": "ibm_marrakesh",
    "shots": shots,
    "physical_qubits": meta_m["physical_qubits"],
    "1q_sweep": res_1q,
    "2q_sweep_zz": res_2q_zz,
    "2q_sweep_z1": res_2q_z1,
    "14q_sweep_zz": res_14q_zz,
    "14q_sweep_z1": res_14q_z1,
    "a_sweep": a_sweep,
    "phi_sweep": phi_sweep,
    "raw_entries": data_entries
}
with open(r"D:\codex\wave-quantum\result_decisive_marrakesh.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2)
print("Saved result_decisive_marrakesh.json successfully!")
