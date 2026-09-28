import json, time, sys, numpy as np
sys.path.insert(0,'.')
from adpf.experiments import StudyConfig, build_feeder, link_day, initial_partition, run_session, _jsonable
from adpf.partition import equal_depth_partition, Partition, is_feasible
from adpf.reference import reference_solution
cfg=StudyConfig.load('configs/default.json')
f,_,ov=build_feeder('syn34',cfg)
day=link_day(ov,24,cfg.s3_latency_ms/1000,cfg.s3_loss_pct/100,0.35,0)
P0=initial_partition(f,cfg.P0); Ph=equal_depth_partition(f,len(P0.roots))
print('P0 sizes',{r:len(m) for r,m in P0.members.items()}, 'heur sizes',{r:len(m) for r,m in Ph.members.items()})
Vfn=lambda fi: reference_solution(fi,cfg.reference)
out={'P0':sorted(P0.roots),'heur':sorted(Ph.roots),'runs':[]}
for smax in [int(a) for a in sys.argv[1].split(',')]:
  for Th in (0.0,600.0):
    for m,start in (('M2','P0'),('M3','P0'),('M3','heur')):
      if start=='heur' and Th!=0.0: continue
      Pst=P0 if start=='P0' else Ph
      t=time.time()
      rows=run_session(f,Vfn,m,Pst,day,cfg,0,ctrl_overrides={'delta_J':0.05,'T_h':Th,'max_team_size':smax})
      nch=sum(len(r['changes']) for r in rows)
      rec={'method':m,'start':start,'S_max':smax,'T_h':Th,'n_changes':nch,'conv':sum(r['status']=='converged' for r in rows),
           'mean_TPF':float(np.mean([r['T_PF'] for r in rows])),'mean_Cmsg':float(np.mean([r['C_msg'] for r in rows])),
           'final':rows[-1]['partition'],'n_teams_final':len(rows[-1]['partition']),'rows':rows}
      out['runs'].append(rec)
      print(m,start,smax,Th,nch,rec['conv'],round(rec['mean_TPF'],2),round(rec['mean_Cmsg']),rec['final'],round(time.time()-t,1),'s',flush=True)
json.dump(_jsonable(out),open(f'/home/claude/work/S4_constrained_{sys.argv[1].replace(",","_")}.json','w'))
