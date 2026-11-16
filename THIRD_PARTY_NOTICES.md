# Third-party dependencies and citation

## MVSAnywhere

Official project: https://github.com/nianticlabs/mvsanywhere

MVSAnywhere: Zero Shot Multi-View Stereo, CVPR 2025. Copyright Niantic, Inc.; non-commercial research licence. An unmodified licence copy is preserved at `LICENSES/MVSAnywhere.txt`. Consult the upstream terms for permitted use; this repository grants no additional rights over official code or model weights.

The full official repository and checkpoint are **not redistributed** here. The loader calls an externally installed/obtained, file-verified official implementation. Our project-owned adapter retains the historical loading and input choices. Upstream source URLs, content hashes and the provenance correction are recorded in VERSION_LOCK and `provenance/upstream/`.

Official checkpoint acquisition remains with the collaborator. No download token, mirrored weight file or alternate pretrained model is bundled.

## DINOv2 and other runtime libraries

DINOv2 is obtained separately from https://github.com/facebookresearch/dinov2 at the verified pin, under its upstream Apache-2.0 terms. Its 156 used Python files are checked by hash; the complete source is not bundled.

PyTorch/torchvision, SciPy, NumPy, OpenCV, Open3D, trimesh and matplotlib are external package dependencies governed by their own licences. Existing libraries are reused; their source distributions and environments are not committed.

## Three.js viewer

The browser uses Three.js **0.169.0**, as in the frozen atlas. To make collaborator review work offline, four small browser runtime components are included under `visualization/vendor/`, with their unmodified MIT licence in `LICENSE.three.txt`. This is a licensed runtime subset, not a complete third-party repository. Every URL and SHA256 is in `provenance/VIEWER_DEPENDENCIES.json`.

## Project-owned historical sources

The three requested project scripts are retained as non-executable provenance under `provenance/frozen_sources/`. Only relevant mathematical functions are extracted into the package. No DXY diameter algorithm, Body optimizer, experimental BA route, SDF/TSDF or complete old research repository is included as a runtime dependency.
