"""One-time maintainer extraction from frozen inputs, never an inference dependency.

All source paths are explicit arguments. Writes only to the new repository.
The real example is LOCAL_ONLY; its small source/hash index can be published.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import numpy as np
from PIL import Image

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from ring_first_hero.io import sha256,save_json,read_json

def main():
    p=argparse.ArgumentParser();p.add_argument('--frozen-experiment',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();n=args.frozen_experiment.resolve();out=args.out.resolve();repo=Path(__file__).resolve().parents[1]
    if not out.is_relative_to(repo):raise ValueError('Maintainer extraction writes only to the new repository')
    out.mkdir(parents=True,exist_ok=True)
    plan=read_json(n/'selection_verified/G01_HERO_PLAN.json')[0]  # first preregistered source, no outcome selection
    frames=[plan['target']]+plan['support_views'];manifest=dict(schema='ring-first-hero-example-1',example_id=plan['id'],source_commit='5636aaebd61a3d53b69f528692c4c7095df46508',source_plan='selection_verified/G01_HERO_PLAN.json:first',group='G01',video='004',unit='mm',work_hw=[360,640],native_hw=[352,640],frames=[],files=[])
    for v in frames:
        if v['group']!='G01' or v['video']!='004' or not v['formal'] or v['role']!='FIT':raise ValueError('Unexpected source identity')
        dst=out/'frames'/v['id'];dst.mkdir(parents=True,exist_ok=True)
        data=dict(np.load(n/'local_results/selected_inputs'/(v['id']+'.npz')))
        if sha256(v['RGB_source'])!=v['RGB_SHA256'] or sha256(v['Mask_source'])!=v['Mask_SHA256']:raise ValueError('Original frame SHA mismatch')
        rgb=np.asarray(Image.open(v['RGB_source']).convert('RGB'));lab=np.asarray(Image.open(v['Mask_source']))
        assert np.array_equal(rgb,data['RGB']) and np.array_equal(lab,data['labels'])
        shutil.copyfile(v['RGB_source'],dst/'RGB.png');shutil.copyfile(v['Mask_source'],dst/'labels.png')
        manifest['frames'].append(dict(id=v['id'],rgb=str((dst/'RGB.png').relative_to(out)),labels=str((dst/'labels.png').relative_to(out)),K=v['K'],c2w_mm=v['C'],camera_status=v['status'],candidate_source=v['candidate_source'],calibrated_pose_truth=False))
    target=frames[0];source=n/'hero_fit'/target['id']
    history=out/'historical';history.mkdir(exist_ok=True)
    for f in ['HERO_native.npz','RAW_NATIVE_MESH.npz','Raw_open_mesh.ply','FACE_EVIDENCE.npz','CLEANING.json']:
        shutil.copyfile(source/f,history/f)
    initial=read_json(n/'registration'/target['id']/'INITIAL.json')
    save_json(history/'CAMERA_INITIAL.json',dict(C=initial['C'],candidate_source=initial['candidate_source'],FIT_objective=initial['FIT_objective']))
    rgb_record=read_json(n/'inputs'/target['id']/'RGB_GEOMETRY.json')
    rgbmap=dict(np.load(rgb_record['map_source']['path']))
    np.savez_compressed(out/'REFERENCE_RGB_MAP.npz',X=rgbmap['X'],des=rgbmap['des'])
    save_json(history/'RGB_GEOMETRY.json',dict(C=rgb_record['C'],features_N=rgb_record['features_N'],fit_pnp_inliers=rgb_record['fit_pnp_inliers'],map_ancestry=rgb_record['map_ancestry']))
    np.savez_compressed(history/'RING_OBSERVATION.npz',**dict(np.load(n/'ring_evidence'/(target['id']+'.npz'))))
    conf=next(x for x in read_json(n/'config/FOUR_GROUP_INPUTS.json')if x['group']=='G01')
    if sha256(conf['ring']['path'])!=conf['ring']['sha256']:raise ValueError('CAD input changed')
    cad=dict(np.load(conf['ring']['path']));np.savez_compressed(out/'RING_CAD.npz',V=cad['V'],F=cad['F'])
    (repo/'cad').mkdir(exist_ok=True);shutil.copyfile(out/'RING_CAD.npz',repo/'cad/R10.npz')
    for f in sorted(out.rglob('*')):
        if f.is_file() and f.name!='DATA_MANIFEST.json':manifest['files'].append(dict(path=str(f.relative_to(out)),bytes=f.stat().st_size,sha256=sha256(f)))
    save_json(out/'DATA_MANIFEST.json',manifest)
    d=repo/'examples/G01_demo';d.mkdir(parents=True,exist_ok=True)
    save_json(d/'DATA_MANIFEST.json',manifest)
    save_json(repo/'provenance/DEMO_INPUT_RECEIPT.json',dict(source_commit=manifest['source_commit'],target_id=target['id'],support_ids=[v['id']for v in frames[1:]],selection='first frozen G01 GEOMETRIC3 plan; no result-based selection',RGB_source_files_verified=True,cache_array_identity_verified=True,source_ring_sha256=conf['ring']['sha256'],reference_map_original_sha256=sha256(rgb_record['map_source']['path']),raw_data_uploaded=False))
    print(json.dumps(dict(example=plan['id'],frames=len(frames),files=len(manifest['files']),out=str(out))))

if __name__=='__main__':main()
