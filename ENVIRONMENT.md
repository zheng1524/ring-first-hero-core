# Environment and dependency provenance

## Tested environment

Execution receipt: `validation/ENVIRONMENT_ACTUAL.json`; exact observed components: `requirements-verified.txt`.

Python 3.12.13; PyTorch 2.7.1+cu128; torchvision 0.22.1+cu128; NumPy 1.26.4; SciPy 1.15.3; OpenCV-headless 4.11.0.86; Open3D 0.19.0. Actual device: RTX3060 Laptop GPU, approximately 6 GB physical VRAM. HERO's measured peak allocated memory was 1,508,467,712 bytes; this is not total GPU reservation or a minimum-memory guarantee.

The new checkout has its own `.venv` and editable project installation. On this workstation it deliberately reuses already installed dependency packages through a machine-local ignored path file. Those dependency directories were read-only. The Python package itself contains no old workspace paths or imports of old experiment scripts.

This is a verified reused environment, not a claim that a clean CUDA image was built. `site_config.local.json`, `.venv`, dependency source trees and checkpoints are excluded from Git.

## New-host recipe

The following is a setup recipe, not a claim of a full fresh download performed during release. Check CUDA/driver compatibility on the destination host before selecting the PyTorch build.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install 'setuptools==70.3.0' wheel
python -m pip install torch==2.7.1 torchvision==0.22.1 \
  --index-url https://download.pytorch.org/whl/cu128
python -m pip install -c requirements-runtime.txt -e '.[hero,clean,test]'
```

The historical environment supplies `pkg_resources` from setuptools70.3.0 in addition to a newer environment installer. The new-host recipe pins the compatibility version explicitly; blindly using the newest setuptools can break older Lightning/dependency imports. The exact fresh-host combination still needs a destination-host smoke test. Do not change model/loss choices to compensate for environment problems.

Acquire the official dependency checkouts outside the Git-tracked project files:

```bash
git clone https://github.com/nianticlabs/mvsanywhere .dependencies/mvsanywhere
git -C .dependencies/mvsanywhere checkout 5bd49bba0992aa56060e1aa3bb40b2150b04726f
git clone https://github.com/facebookresearch/dinov2 .dependencies/dinov2
git -C .dependencies/dinov2 checkout 7764ea0f912e53c92e82eb78a2a1631e92725fc8
```

Provide the checkpoint separately from its official URL. The loader checks its complete SHA256 before `torch.load`; it also verifies every used MVSAnywhere and DINOv2 source/config file. No auxiliary pretrained backbone download is required because all learned parameters are present in the full HERO checkpoint. Only the three documented pixel-coordinate buffers are regenerated for the native resolution.

The original minimal MVSAnywhere source subset matches all 105 used files in the upstream checkout. A full upstream checkout may contain additional files; those are not executed as replacements or redistributed by this repository.

## Runtime choices kept unchanged

- Exactly three source images, one refinement step, 352×640 model output.
- CUDA FP16 autocast, original official preprocess/forward, `fast_cost_volume=False`.
- Actual camera translation conversion mm→m, output axial Z conversion m→mm.
- No optimizer, training, network update or new architecture.
- CPU Ring solve/SIFT/ray geometry. Open3D is needed for optional cleaning and gallery rendering, not for the basic camera solve.

Historical camera refinement used PyCeres2.6/Ceres2.2. It is not a hidden dependency of the released target RF/RGB solve. Frozen support cameras keep their Ceres provenance and conditional status.
