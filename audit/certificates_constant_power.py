"""Proposition 2 certificates (Table XI) for the constant-power model used in S1-S7. Run from the adpf_project root."""
from adpf.feeder import get_feeder
from adpf.verification import invariant_ball
for name in ("syn13", "syn34", "syn123"):
    for ls in (1.0, 4.0):
        print(name, ls, invariant_ball(get_feeder(name, p=1, seed=1, load_scale=ls)))
