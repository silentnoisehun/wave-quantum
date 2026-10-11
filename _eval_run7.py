"""A DÖNTŐ KIÉRTÉKELÉS: Run 7 + 7b (rögzített layout) a ZÁRT kritériumok szerint.
Kritérium (3acb8c8, 68% CI, chi2 12 dof):
  (A) ELFOGADJUK layout-magyarázatot ha 1.36*sigma_sys < 0.10 mindkét futásnál
      ELUTASÍTJUK ha 0.72*sigma_sys > 0.15 mindkettőnél
      KÖZTE: NEM DÖNTHETŐ
  (B) drift (külön): |A7 - A7b| < max(2*sigma_A, 0.06)
"""
import json, math, os, argparse
from qiskit_ibm_runtime import QiskitRuntimeService

def evaluate_local(result_file, shots):
    """Evaluate from local result JSON (no API needed)."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    result_path = os.path.join(base_dir, result_file)
    data = json.load(open(result_path, encoding="utf-8"))
    
    rows = []
    for r in data.get("rows", []):
        rows.append({"band": r["band"], "measured": r["measured"], "theory": r["theory"]})
    
    if not rows:
        return None
        
    N = len(rows)
    meas = [r["measured"] for r in rows]; theo = [r["theory"] for r in rows]
    m_m, m_t = sum(meas)/N, sum(theo)/N
    pearson = sum((a-m_m)*(b-m_t) for a,b in zip(meas,theo)) / math.sqrt(sum((a-m_m)**2 for a in meas)*sum((b-m_t)**2 for b in theo))
    A = sum(m*t for m,t in zip(meas,theo)) / sum(t*t for t in theo)
    chi2 = sum(((r["measured"] - A*r["theory"]) / math.sqrt(max(1.0-(A*r["theory"])**2,1e-9)/shots))**2 for r in rows)
    chi2_red = chi2/12
    mean_inv_var = sum(1.0/max(1.0-(A*r["theory"])**2,1e-9) for r in rows)/N
    sigma_sys = math.sqrt(max(chi2_red-1.0,0.0)/(shots*mean_inv_var))
    sig_A = math.sqrt(1.0/shots / sum(t*t for t in theo))
    return A, sig_A, sigma_sys, pearson, chi2_red

def evaluate(svc, jid, name, shots, backend):
    job = svc.job(jid)
    result = job.result()
    rows = []
    for i in range(13):
        data = result[i].data
        counts = None
        for cn in ("c", "meas"):
            if hasattr(data, cn):
                counts = getattr(data, cn).get_counts(); break
        if counts is None:
            counts = getattr(data, list(vars(data).keys())[0]).get_counts()
        zz = (counts.get("00",0)+counts.get("11",0)-counts.get("01",0)-counts.get("10",0))/shots
        rows.append({"band": i, "measured": zz, "theory": math.cos(2.0*math.pi*i/13)})
    meas = [r["measured"] for r in rows]; theo = [r["theory"] for r in rows]
    m_m, m_t = sum(meas)/13, sum(theo)/13
    pearson = sum((a-m_m)*(b-m_t) for a,b in zip(meas,theo)) / math.sqrt(sum((a-m_m)**2 for a in meas)*sum((b-m_t)**2 for b in theo))
    A = sum(m*t for m,t in zip(meas,theo)) / sum(t*t for t in theo)
    chi2 = sum(((r["measured"] - A*r["theory"]) / math.sqrt(max(1.0-(A*r["theory"])**2,1e-9)/shots))**2 for r in rows)
    chi2_red = chi2/12
    mean_inv_var = sum(1.0/max(1.0-(A*r["theory"])**2,1e-9) for r in rows)/13
    sigma_sys = math.sqrt(max(chi2_red-1.0,0.0)/(shots*mean_inv_var))
    sig_A = math.sqrt(1.0/shots / sum(t*t for t in theo))
    print(f"--- {name} ({backend}, {shots} shots) ---")
    print(f"  Pearson: {pearson:.4f} | A: {A:.4f} ± {sig_A:.4f} | chi2_red: {chi2_red:.2f} | sigma_sys: {sigma_sys:.4f}")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, f"result_{name}.json"), "w", encoding="utf-8") as f:
        json.dump({"job_id": jid, "backend": backend, "shots": shots, "pearson": pearson,
                   "A_fit": A, "A_err": sig_A, "chi2_red": chi2_red, "sigma_sys_binomial": sigma_sys,
                   "rows": rows}, f, indent=2)
    return A, sig_A, sigma_sys, pearson, chi2_red

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Run 7 and 7b")
    parser.add_argument("--local", action="store_true", help="Evaluate from local result JSON files (no API)")
    args = parser.parse_args()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    run7  = json.load(open(os.path.join(base_dir, "_run7_meta.json"), encoding="utf-8"))
    run7b = json.load(open(os.path.join(base_dir, "_run7b_meta.json"), encoding="utf-8"))
    
    if args.local:
        print("=" * 64)
        print("RUN 7/7b EVALUATION (LOCAL, NO API)")
        print("=" * 64)
        res7 = evaluate_local("result_run7_fixed_layout.json", run7["shots"])
        res7b = evaluate_local("result_run7b_fixed_layout.json", run7b["shots"])
        
        if res7 is None or res7b is None:
            print("Local result files not found. Run with --local after jobs complete.")
        else:
            A7, sA7, ss7, p7, c7 = res7
            A7b, sA7b, ss7b, p7b, c7b = res7b
    else:
        downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        with open(os.path.join(downloads, "apikey (2).json"), encoding="utf-8") as fh:
            t1 = json.load(fh)["apikey"]
        with open(os.path.join(downloads, "apikey (1).json"), encoding="utf-8") as fh:
            t2 = json.load(fh)["apikey"]
        s1 = QiskitRuntimeService(channel="ibm_quantum_platform", token=t1, instance="auto")
        s2 = QiskitRuntimeService(channel="ibm_quantum_platform", token=t2, instance="auto")
        
        A7, sA7, ss7, p7, c7  = evaluate(s1, run7["job_id"],  "run7_fixed_layout",  2048, "ibm_fez")
        A7b, sA7b, ss7b, p7b, c7b = evaluate(s2, run7b["job_id"], "run7b_fixed_layout", 2048, "ibm_fez")

    print()
    print("=" * 64)
    print("A ZÁRT KRITÉRIUMOK KIÉRTÉKELÉSE (commit 3acb8c8)")
    print("=" * 64)
    # (A) layout-kérdés
    ci7  = (0.72*ss7,  1.36*ss7)
    ci7b = (0.72*ss7b, 1.36*ss7b)
    print(f"(A) layout-kérdés (68% CI):")
    print(f"    run7:  sigma_sys={ss7:.4f} -> CI [{ci7[0]:.4f}, {ci7[1]:.4f}]")
    print(f"    run7b: sigma_sys={ss7b:.4f} -> CI [{ci7b[0]:.4f}, {ci7b[1]:.4f}]")
    accept = ci7[1] < 0.10 and ci7b[1] < 0.10
    reject = ci7[0] > 0.15 and ci7b[0] > 0.15
    if accept:
        print("    ==> ELFOGADVA: a layout magyarázza a futáson-belüli szórást")
    elif reject:
        print("    ==> ELUTASÍTVA: a layout NEM a magyarázat (megmagyarázatlan: crosstalk/readout/leakage/TLS)")
    else:
        print("    ==> NEM DÖNTHETŐ: új futások kell (több shots)")
    print()
    # (B) drift-kérdés
    dA = abs(A7 - A7b)
    tol = max(2.0*max(sA7, sA7b), 0.06)
    print(f"(B) drift-kérdés: |A7-A7b| = {dA:.4f} vs tűrés max(2*sigma_A, 0.06) = {tol:.4f}")
    print(f"    ==> {'STABIL (nincs drift-jezés)' if dA < tol else 'DRIFT-JELZÉS'}")
    print()
    # Összevetés a szabad-layout futásokkal
    print("Összevetés (fez, mind 2048/1024 shots):")
    print(f"  szabad layout (run2): sigma_sys=0.189, A=0.671")
    print(f"  szabad layout (run3): sigma_sys=0.148, A=0.632")
    print(f"  RÖGZÍTETT layout:     sigma_sys={ss7:.3f}/{ss7b:.3f}, A={A7:.3f}/{A7b:.3f}")