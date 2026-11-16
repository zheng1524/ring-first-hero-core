"""CPU geometry controls. Synthetic arrays here are tests, never G01 demo data."""
from pathlib import Path
import ast
import csv
import hashlib
import json
import numpy as np
import pytest
from scipy.spatial.transform import Rotation
from ring_first_hero.geometry import (project,unproject,validate_camera,resize_index_intrinsics,native_rgb_labels,depth_mesh,ring_mesh)
from ring_first_hero.camera import observe,torus_contours

ROOT=Path(__file__).resolve().parents[1]
K=np.array([[490.,0,319.5],[0,490.,179.5],[0,0,1.]])

@pytest.mark.parametrize('rotation',[[0,0,0],[.1,-.2,.3],[.7,.2,-.8]])
def test_c2w_w2c_and_metric_unprojection(rotation):
    C=np.eye(4);C[:3,:3]=Rotation.from_rotvec(rotation).as_matrix();C[:3,3]=[3,-8,25]
    uv=np.array([[0,0],[319.5,179.5],[639,359],[80,250.]])
    z=np.array([10.,20.,31.,40.]);X=unproject(z,C,uv,K)
    p,actual=project(X,C,K)
    np.testing.assert_allclose(p,uv,atol=2e-12);np.testing.assert_allclose(actual,z,atol=1e-12)
    W=np.linalg.inv(C);cam=X@W[:3,:3].T+W[:3,3]
    np.testing.assert_allclose(cam[:,2],z,atol=1e-12)
    Cm=C.copy();Cm[:3,3]/=1000
    np.testing.assert_allclose(unproject(z/1000,Cm,uv,K)*1000,X,atol=1e-11)

def test_wrong_transform_is_not_equivalent():
    C=np.eye(4);C[:3,3]=[1,2,20]
    uv=np.array([[319.,179.]]);X=unproject(np.array([10.]),C,uv,K)
    wrong,_=project(X,np.linalg.inv(C),K)
    assert np.linalg.norm(wrong-uv)>10

def test_reject_improper_camera():
    C=np.eye(4);C[0,0]=-1
    with pytest.raises(ValueError):validate_camera(C,K)

def test_native_K_640x360_to_640x352():
    Kn=resize_index_intrinsics(K)
    assert Kn[0,0]==490
    assert Kn[1,1]==pytest.approx(490*352/360)
    assert Kn[0,2]==319.5
    assert Kn[1,2]==pytest.approx(175.5)
    assert Kn[1,1]!=K[1,1]  # a crop would retain fy; this path is a resize

@pytest.mark.parametrize('uv',[[0.,0.],[319.,175.],[639.,351.]])
def test_half_pixel_corner_index_consistency(uv):
    Kn=resize_index_intrinsics(K);corner=K.copy();corner[:2,2]+=.5;corner[1]*=352/360
    ray_a=np.linalg.inv(Kn)@np.r_[uv,1.]
    ray_b=np.linalg.inv(corner)@np.r_[np.array(uv)+.5,1.]
    np.testing.assert_allclose(ray_a,ray_b,atol=1e-15)

def test_native_label_mapping_is_nearest_only():
    yy,xx=np.mgrid[:360,:640];lab=((yy//15+xx//17)%3).astype(np.uint8)
    rgb=np.repeat(lab[:,:,None],3,axis=2);mapped,labels,Kn=native_rgb_labels(rgb,lab,K)
    assert labels.shape==(352,640) and mapped.shape==(352,640,3)
    assert set(np.unique(labels))=={0,1,2}
    assert np.array_equal(mapped[:,:,0],labels)

def test_raw_native_lattice_and_depth_jump():
    z=np.full((8,9),30.,np.float32);lab=np.ones(z.shape,np.uint8);rgb=np.zeros((*z.shape,3),np.uint8)
    kk=K.copy();C=np.eye(4)
    m,uv,pix=depth_mesh(z,lab,C,kk,rgb)
    assert len(m.faces)==2*7*8
    assert np.array_equal(pix,uv[:,1]*9+uv[:,0])
    pred,depth=project(m.vertices,C,kk);np.testing.assert_allclose(pred,uv,atol=2e-13)
    np.testing.assert_allclose(depth,30)
    z[:,4:]=31.;before=z.copy();m,uv,pix=depth_mesh(z,lab,C,kk,rgb)
    assert np.ptp(z[uv[:,1],uv[:,0]][m.faces],axis=1).max()<=.75
    assert len(m.faces)<2*7*8
    np.testing.assert_array_equal(z,before)

def test_missing_depth_never_filled():
    z=np.full((5,6),30.,np.float32);z[2,2]=np.nan
    m,uv,pix=depth_mesh(z,np.ones(z.shape,np.uint8),np.eye(4),K,np.zeros((5,6,3),np.uint8))
    assert 2*6+2 not in pix and len(m.vertices)==29
    assert np.isnan(z[2,2])

def test_R10_known_CAD():
    m=ring_mesh();rho=np.linalg.norm(m.vertices[:,:2],axis=1)
    assert m.is_watertight
    assert 2*rho.min()==pytest.approx(10.,abs=1e-12)
    assert 2*rho.max()==pytest.approx(12.4,abs=1e-12)
    np.testing.assert_allclose(np.hypot(rho-5.6,m.vertices[:,2]),.6,atol=2e-15)

def test_projection_of_true_torus_tangency():
    # Controlled camera, not claimed to be a real input frame.
    C=np.eye(4);C[:3,:3]=np.diag([1,-1,-1]);C[:3,3]=[0,-3,30]
    curves=torus_contours(C,K,256)
    assert curves.shape==(2,256,2) and np.isfinite(curves).all()
    assert (curves[:,:,0]>0).all() and (curves[:,:,0]<640).all()

def test_polyp_adjacent_ring_boundaries_remain_unknown():
    lab=np.zeros((360,640),np.uint8);lab[100:130,240:400]=2;lab[130:160,250:390]=1
    ob=observe(lab)
    assert len(ob['unknown_boundary'])>0 and len(ob['q_train'])>0
    assert len(ob['p_train'])<=192 and len(ob['b_train'])<=192

def test_exact_frozen_functions():
    rows=list(csv.DictReader((ROOT/'provenance/MODULE_MIGRATION.csv').open()))
    for file in ['_kernels.py','_clean_kernels.py']:
        text=(ROOT/'src/ring_first_hero'/file).read_text()
        functions={n.name:ast.get_source_segment(text,n)for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)}
        for row in rows:
            if row['destination'].endswith('/'+file):assert hashlib.sha256(functions[row['function']].encode()).hexdigest()==row['function_sha256']

def test_three_requested_source_hashes():
    expected={'cameras.py':'ba95a389fc6722841491c3f876906e0014262c8baa055637a648bc66378db95f','torus.py':'904d9cae48c1cc9317454c2feb80a331908009e095683851c8e8e3c80625191d','infer.py':'c48926cb8ede2792a903436c6478f4fd44f00a8e261c9408521165db738c7049'}
    for f,h in expected.items():assert hashlib.sha256((ROOT/'provenance/frozen_sources'/f).read_bytes()).hexdigest()==h

def test_no_old_workspace_runtime_imports():
    for p in (ROOT/'src/ring_first_hero').glob('*.py'):
        text=p.read_text();assert '/home/liu/'not in text
        assert 'from context import'not in text and 'from ucommon import'not in text

def test_upstream_lock_checks_content_not_parent_git():
    d=json.loads((ROOT/'src/ring_first_hero/upstream_source_lock.json').read_text())
    assert len(d['matched'])==105 and d['different']==[]
    assert len(d['dinov2']['matched'])==156 and d['dinov2']['different']==[]
    assert d['dinov2']['upstream_commit']
