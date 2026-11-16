"""Executed locally on the controlled real G01 example; skipped if not supplied."""
from pathlib import Path
import json
import numpy as np
import pytest
import trimesh
from scipy.spatial import cKDTree
from ring_first_hero.io import read_json,check_assets
from ring_first_hero.geometry import project

ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'.local_data/G01_demo';OUT=ROOT/'outputs/hero'
pytestmark=pytest.mark.skipif(not (DATA/'DATA_MANIFEST.json').exists(),reason='Controlled G01 data is not redistributed; see DATA_ACCESS.md')

def test_real_four_frame_identity_and_pose_contract():
    d=read_json(DATA/'DATA_MANIFEST.json');check_assets(DATA,d)
    assert len(d['frames'])==4 and d['group']=='G01' and d['video']=='004'
    assert len({r['id']for r in d['frames']})==4
    rec=read_json(ROOT/'outputs/camera/HISTORICAL_CAMERA_COMPARISON.json')
    assert rec['c2w_max_abs']<1e-10 and rec['candidate_source_equal']

def test_fresh_official_inference_and_raw_geometry():
    run=read_json(OUT/'INFERENCE.json');receipt=read_json(OUT/'MODEL_RECEIPT.json');rec=read_json(OUT/'HISTORICAL_COMPARISON.json')
    assert run['inference_executed'] and not run['reused_historical_depth'] and run['optimizer_steps']==0
    assert receipt['all_learned_parameters_loaded']==535
    assert rec['depth_bitwise_equal'] and rec['raw_faces_equal'] and rec['raw_pixel_ids_equal']
    assert rec['raw_vertex_max_mm']==0
    m=dict(np.load(OUT/'RAW_NATIVE_MESH.npz'));uv,z=project(m['V'],m['T'],m['K'])
    np.testing.assert_allclose(uv,m['uv'],atol=2e-12)
    assert np.isfinite(m['V']).all() and (m['F']>=0).all() and m['F'].max()<len(m['V'])

def test_optional_cleaning_is_exact_and_reversible():
    rec=read_json(OUT/'HISTORICAL_COMPARISON.json');assert rec['cleaning_state_equal'] and rec['cleaning_reason_bits_equal']
    f=dict(np.load(OUT/'FACE_EVIDENCE.npz'));raw=dict(np.load(OUT/'RAW_NATIVE_MESH.npz'))
    np.testing.assert_array_equal(f['V'],raw['V']);np.testing.assert_array_equal(f['F'],raw['F'])
    assert set(np.unique(f['state']))<=set([0,1,2,3])

def test_layered_GLB_uses_metres_once():
    scene=trimesh.load(ROOT/'visualization/assets/scenes/G01_core.glb',force='scene',process=False)
    assert any('Ring_R10' in n for n in scene.geometry)
    assert sum('__RAW'in n for n in scene.geometry)==1
    raw=dict(np.load(OUT/'RAW_NATIVE_MESH.npz'))
    g=next(g for n,g in scene.geometry.items()if '__RAW'in n)
    distances=cKDTree(raw['V']).query(np.asarray(g.vertices)*1000)[0]
    assert distances.max()<5e-6  # only GLB float32 encoding; no scale fitting
    cad=next(g for n,g in scene.geometry.items()if 'Ring_R10'in n)
    assert 2*np.linalg.norm(cad.vertices[:,:2],axis=1).min()*1000==pytest.approx(10,abs=1e-5)

def test_G03_GLBS_keep_sources_separate():
    p=ROOT/'visualization/assets/scenes/G03_native_sources.glb'
    if not p.exists():pytest.skip('G03 reference export not supplied')
    scene=trimesh.load(p,force='scene',process=False)
    assert sum('__RAW'in n for n in scene.geometry)==2
    assert not any('Body'in n or 'BODY'in n for n in scene.geometry)
