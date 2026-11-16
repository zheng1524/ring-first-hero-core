import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

const host=document.querySelector('#viewer'),status=document.querySelector('#viewer-status');
const requestedScene=new URLSearchParams(location.search).get('scene');
if([...document.querySelector('#scene-choice').options].some(o=>o.value===requestedScene))document.querySelector('#scene-choice').value=requestedScene;
const scene=new THREE.Scene();scene.background=new THREE.Color('#eff2ed');
const camera=new THREE.PerspectiveCamera(42,1,.00001,10);camera.up.set(0,0,1);
const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.outputColorSpace=THREE.SRGBColorSpace;host.appendChild(renderer.domElement);
const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;
scene.add(new THREE.AmbientLight(0xffffff,2.1));const light=new THREE.DirectionalLight(0xffffff,2.1);light.position.set(.06,-.04,.09);scene.add(light);
let model=null;const sources=new Set(),nodes=[];
function resize(){renderer.setSize(host.clientWidth,host.clientHeight);camera.aspect=host.clientWidth/host.clientHeight;camera.updateProjectionMatrix();}
new ResizeObserver(resize).observe(host);resize();
function kind(node){return node.name.includes('__')?node.name.split('__').at(-1):'';}
function apply(){
 const mode=document.querySelector('#surface-choice').value,availableTrusted=nodes.some(n=>kind(n)==='TRUSTED');
 for(const n of nodes){
  if(n.name.startsWith('Ring_'))n.visible=document.querySelector('#ring-toggle').checked;
  else if(n.name.startsWith('CAMERA__'))n.visible=document.querySelector('#camera-toggle').checked;
  else{const k=kind(n),id=n.name.slice(0,n.name.lastIndexOf('__'));n.visible=sources.has(id)&&(k===(mode==='TRUSTED'&&availableTrusted?'TRUSTED':'RAW'));}
 }
}
function reset(){
 const box=new THREE.Box3();
 for(const n of nodes)if(n.visible&&!n.name.startsWith('CAMERA__'))box.union(new THREE.Box3().setFromObject(n));
 if(box.isEmpty())return;
 const center=box.getCenter(new THREE.Vector3()),size=box.getSize(new THREE.Vector3());
 const radius=size.length()*.75;controls.target.copy(center);camera.position.copy(center).add(new THREE.Vector3(radius*1.3,-radius*1.8,radius*.9));camera.lookAt(center);controls.update();
 document.querySelector('#scale').textContent=`Visible bounds: ${(size.x*1000).toFixed(2)} × ${(size.y*1000).toFixed(2)} × ${(size.z*1000).toFixed(2)} mm`;
}
async function load(){
 status.dataset.loadStatus='loading';status.textContent='Loading actual GLB…';
 const name=document.querySelector('#scene-choice').value;document.querySelector('#download').href=`assets/scenes/${name}.glb`;
 try{
  const gltf=await new GLTFLoader().loadAsync(`assets/scenes/${name}.glb`);
  if(model){scene.remove(model);model.traverse(n=>{if(n.geometry)n.geometry.dispose();});}
  model=gltf.scene;scene.add(model);nodes.length=0;sources.clear();
  model.traverse(n=>{if(n.isMesh){nodes.push(n);if(n.material){n.material.side=THREE.DoubleSide;n.material.needsUpdate=true;}if(kind(n)==='RAW')sources.add(n.name.slice(0,n.name.lastIndexOf('__')));}});
  const trustedOption=document.querySelector('#surface-choice option[value="TRUSTED"]');
  trustedOption.disabled=!nodes.some(n=>kind(n)==='TRUSTED');
  if(trustedOption.disabled)document.querySelector('#surface-choice').value='RAW';
  const list=document.querySelector('#sources');list.replaceChildren();
  for(const id of sources){const label=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.checked=true;input.dataset.source=id;input.addEventListener('change',()=>{if(input.checked)sources.add(id);else sources.delete(id);apply();});label.append(input,document.createTextNode(' '+id));list.append(label);}
  apply();reset();status.dataset.loadStatus='ready';status.dataset.meshCount=String(nodes.length);status.textContent=`Loaded ${nodes.length} separate Mesh objects. Original source identities preserved. Display dimensions are in mm.`;
 }catch(error){status.dataset.loadStatus='error';status.textContent='3D load failed: '+error.message;console.error(error);}
}
document.querySelector('#scene-choice').addEventListener('change',load);
for(const id of ['surface-choice','ring-toggle','camera-toggle'])document.querySelector('#'+id).addEventListener('change',apply);
document.querySelector('#reset').addEventListener('click',reset);
renderer.setAnimationLoop(()=>{controls.update();renderer.render(scene,camera);});
load();
