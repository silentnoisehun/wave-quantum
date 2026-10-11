"""Referee-grade statisztika minden futáshoz: illesztett kontraszt, chi2, null-kontroll."""
import json, math, os

N = 13
def fit_contrast(rows):
    num = sum(r["measured"] * r["theory"] for r in rows)
    den = sum(r["theory"] ** 2 for r in rows)
    return num / den

def chi2(rows, A, shots):
    s = 0.0
    dof = N - 1
    for r in rows:
        t = r["theory"]
        sigma = math.sqrt(max((1.0 - (A * t) ** 2) / shots, 1e-9))
        s += ((r["measured"] - A * t) / sigma) ** 2
    return s, dof, s / dof

def null_control_p(rows, shots):
    A = fit_contrast(rows)
    den = sum(r["theory"] ** 2 for r in rows)
    sig = sum(math.sqrt(max(1.0 / shots, 1e-9)) for _ in rows) / N
    z = A / (sig / math.sqrt(den))
    from math import erfc, sqrt
    p = erfc(abs(z) / sqrt(2))
    return A, z, p

base_dir = os.path.dirname(os.path.abspath(__file__))
results = {}

for f in sorted(os.listdir(base_dir)):
    if f.startswith("result_run") and f.endswith(".json"):
        name = f[7:-5]
        d = json.load(open(os.path.join(base_dir, f), encoding="utf-8"))
        rows = d.get("rows", [])
        if not rows:
            continue
        shots = d["shots"]
        A = fit_contrast(rows)
        c2, dof, red = chi2(rows, A, shots)
        A0, z, p = null_control_p(rows, shots)
        
        mean_inv_var = sum(1.0 / max(1.0 - (A * r["theory"]) ** 2, 1e-9) for r in rows) / N
        sigma_sys = math.sqrt(max(red - 1.0, 0.0) / (shots * mean_inv_var))
        
        results[name] = {
            "shots": shots,
            "pearson": d.get("pearson", 0.0),
            "A_fit": A,
            "chi2": c2,
            "dof": dof,
            "chi2_red": red,
            "sigma_sys_binomial": sigma_sys,
            "z_vs_null": z,
            "p_null": p,
        }
        print(f"--- {name} ({shots} shots) ---")
        print(f"  illesztett kontraszt A: {A:.4f}  (ideal 1.0)")
        print(f"  chi2 = {c2:.2f} / {dof} dof  ->  chi2_red = {red:.2f}")
        print(f"  sigma_sys (binomial): {sigma_sys:.4f}")
        print(f"  null-kontroll: z = {z:.2f} sigma, p = {p:.2e}")
        print(f"  Pearson: {d.get('pearson', 0.0):.4f}")
        print()

stats_path = os.path.join(base_dir, "referee_stats.json")
with open(stats_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print("Mentve:", stats_path)
