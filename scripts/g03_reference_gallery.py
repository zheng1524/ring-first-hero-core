"""Read two actual frozen native HERO sources; no new inference or registration."""
import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from ring_first_hero.io import read_json,save_json,sha256
from ring_first_hero.visualization import render_panel,scene_export

def main():
    p=argparse.ArgumentParser();p.add_argument('--frozen-experiment',type=Path,required=True);p.add_argument('--gallery',type=Path,required=True)
    a=p.parse_args();n=a.frozen_experiment;assets=a.gallery/'assets';sources=[];receipt=[]
    plans=[r for r in read_json(n/'selection_verified/G03_HERO_PLAN.json') if r['target']['video']=='004'][:2]
    for i,r in enumerate(plans):
        if r['target']['video']!='004':raise ValueError('Expected same-video G03 example')
        f=n/'hero_fit'/r['id']/'RAW_NATIVE_MESH.npz';s=dict(np.load(f));color=np.array([[.32,.55,.86],[.9,.52,.24]])[i]
        sources.append((r['id'],s['V'],s['F'],color,'RAW'))
        receipt.append(dict(source_id=r['id'],source_commit='5636aaebd61a3d53b69f528692c4c7095df46508',source_path='hero_fit/'+r['id']+'/RAW_NATIVE_MESH.npz',sha256=sha256(f),native=True,transform_applied_to_geometry=False,body_or_fusion=False,target_video=r['target']['video'],support_ids=[s['id']for s in r['support_views']],support_videos=[s['video']for s in r['support_views']],statistical_independence_claimed=False))
    c=next(c for c in read_json(n/'config/FOUR_GROUP_INPUTS.json')if c['group']=='G03');cad=dict(np.load(c['ring']['path']))
    if sha256(c['ring']['path'])!=c['ring']['sha256']:raise ValueError('CAD input changed')
    bounds=np.r_[cad['V'],*[s[1][np.unique(s[2])]for s in sources]]
    fig,axs=plt.subplots(1,3,figsize=(13,4.5))
    for ax,s in zip(axs[:2],sources):render_panel(ax,s[1],s[2],cad,bounds,s[0]+' / Raw native',(25,-65),color=matplotlib.colors.to_hex(s[3]))
    V=np.concatenate([s[1]for s in sources]);F=np.r_[sources[0][2],sources[1][2]+len(sources[0][1])]
    colors=np.r_[np.tile(sources[0][3],(len(sources[0][2]),1)),np.tile(sources[1][3],(len(sources[1][2]),1))]
    render_panel(axs[2],V,F,cad,bounds,'Independent source overlay / NOT a fused surface',(25,-65),face_colors=colors)
    fig.suptitle('G03 difficulty: source disagreement and limited directions remain; no relocation / filling / Body geometry')
    fig.savefig(assets/'07_G03_Raw_Source_Limitations.png',dpi=145,bbox_inches='tight');plt.close(fig)
    scene_export(assets/'scenes/G03_native_sources.glb',sources,cad)
    save_json(assets/'G03_SOURCE_MANIFEST.json',receipt)

if __name__=='__main__':main()
