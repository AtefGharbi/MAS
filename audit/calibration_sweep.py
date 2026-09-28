import json, sys, time, numpy as np, dataclasses
sys.path.insert(0,'.')
from multiprocessing import Pool
from adpf.experiments import StudyConfig, run_spec
cfg=StudyConfig.load('configs/default.json')
feeders=sys.argv[1].split(',')
specs=[]
for f in feeders:
  for eps0 in (1e-3,1e-4,1e-5,1e-6):
    for lat in (0.0,10.0,100.0):
      for loss in (0.0,10.0):
        for seed in (0,1,2):
          d=dataclasses.asdict(cfg) if dataclasses.is_dataclass(cfg) else dict(cfg.__dict__)
          d=json.loads(json.dumps(d)); d['solver']={'eps0':eps0}
          specs.append(({'scenario':'CAL','feeder':f,'method':'M1','seed':seed,'latency_ms':lat,'loss_pct':loss,'fault':None,'duration_s':None,'route_available':None},d))
def go(a):
  r=run_spec(a); r['eps0']=a[1]['solver']['eps0']; return {k:r.get(k) for k in ('feeder','eps0','latency_ms','loss_pct','seed','status','T_PF','C_msg','E_V_max','RMSE_absV','RMSE_V')}
t=time.time()
with Pool(4) as p: out=p.map(go,specs)
json.dump(out,open(f'/home/claude/work/calib_{"_".join(feeders)}.json','w'))
print(len(out),round(time.time()-t),'s')
