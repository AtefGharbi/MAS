# Supplementary bundle for manuscript V20

Adds to the existing staged_results_archive (not duplicated here):

- `S3_timeout_reconciliation.csv`: the ten non-converged S3 records (Table XXI). It was cited in V19 but missing from the archive.
- `audit/reconcile_S2_S3.py`: recomputes every S2/S3 count in Tables XV–XXI from `results/S2|S3/results.jsonl`. `audit/reconcile_output.txt` is its output.
- `audit/certificates_constant_power.py`: Proposition 2 certificates for the constant-power model actually simulated (Table XI).
- `audit/calibration_sweep.py` + `new_results/calib_*.json`: trigger-tolerance calibration (Table XVII). M1, latency {0,10,100} ms × loss {0,10}% × seeds 0–2, eps0 ∈ {1e-3..1e-6}.
- `audit/s4_constrained.py` + `new_results/S4_constrained_*.json`: S4 rerun with max team size (Table XXII).
- `audit/fig6_censoring.py`: regenerates Fig. 6 with markers on points that include nonconverged runs.
- `test_log_pytest.txt`: 30/30 tests passed (pytest 9.1.1, Python 3.12.3).

Scripts expect to be run from the `adpf_project` root with `PYTHONPATH=.`; the calibration and S4 scripts write their JSON to paths set at the top of the script, which should be adjusted to your checkout.
