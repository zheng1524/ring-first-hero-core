# Reproduce the verified real case

## Fixed identities

- Scientific snapshot: `5636aaebd61a3d53b69f528692c4c7095df46508`.
- Example: first entry in frozen `selection_verified/G01_HERO_PLAN.json`, G01/video004, GEOMETRIC3. Selection preceded the new output; no GT or output quality was used to choose it.
- Target: `G01_v004_raw00341`; supports: `raw00326 / raw00360 / raw00204`, all G01/video004.
- Official used source: verified file-equivalent MVSAnywhere `5bd49bba0992aa56060e1aa3bb40b2150b04726f`.
- Checkpoint SHA256: `00878bab903b1d384cd6bb9ea092e247a9036d429cb8bcc3d6dcbb81f67e556d`.

Obtain the controlled input bundle and pinned official dependencies as described in DATA_ACCESS/ENVIRONMENT. Commands below are run from this checkout in the prepared environment.

```bash
python -m pip install --no-deps --no-build-isolation -e .
python -m ring_first_hero --help
python -m ring_first_hero camera_demo --data .local_data/G01_demo --out outputs/camera
python -m ring_first_hero hero_demo --data .local_data/G01_demo \
  --runtime-config site_config.local.json --out outputs/hero \
  --clean --compare-history --visualize
python -m ring_first_hero visualize --data .local_data/G01_demo \
  --output outputs/hero --gallery visualization
python -m pytest -q
python -m http.server 8765 --bind 127.0.0.1 --directory visualization
```

Open `http://127.0.0.1:8765/`. For the second frozen example: `http://127.0.0.1:8765/?scene=G03_native_sources`.

## Evidence of execution

- `validation/camera_demo.*`: actual target solve. Comparison file: c2w max difference 0, FIT objective difference 0, identical selected candidate source.
- `validation/full_hero_cli.*`: new official CUDA forward, all learned parameters loaded. `optimizer_steps=0`, no cached-depth prediction fallback.
- `validation/HISTORICAL_COMPARISON.json`: new output vs historical native depth/mesh/classification. All 225,280 depth samples and authoritative Raw vertices/faces/Pixel IDs are identical; cleaning state and reason bits are identical.
- `validation/RAW_MESH_GEOMETRY.json`: actual finite data, original depth-jump rule, topology and CAD conflicts. Open geometry and defects are reported rather than repaired.
- `validation/pytest.*`: CPU and actual controlled-data integration checks. Real-data tests are explicitly skipped on a collaborator checkout until the controlled example/output is supplied; that is not a successful inference.
- `validation/BROWSER_SMOKE.json`: actual localhost resource and headless Chrome tests of both separate-source GLBs. Browser screenshots and raw browser profile are local-only.

The historical output is loaded for value comparison **after the new output is written**. Its SHA can be checked beforehand as an input-provenance operation; it is never used by the predictor. No Blender, Body or Dxy truth is read.

## Optional diagnostics

```bash
python -m ring_first_hero camera_demo --data .local_data/G01_demo \
  --out outputs/ring_only --ring-only
```

This deliberately reports unresolved yaw. It is not used to replace the four fixed cameras in the HERO experiment.

`scripts/browser_smoke.py` additionally automates the documented HTTP server and installed Google Chrome in an isolated ignored profile. It starts/stops only its own server, uses local viewer dependencies and does not interact with an existing user browser.

## Maintainer-only migration tools

`scripts/prepare_g01.py --frozen-experiment SOURCE --out NEW_REPO/.local_data/G01_demo` copies the authorized fixed example with file hashes and checks exact frame/cache identity. `scripts/g03_reference_gallery.py --frozen-experiment SOURCE --gallery visualization` reads the first two **video004** entries in the frozen G03 plan and exports independent source layers. These are migration utilities, not runtime dependencies on an old experiment.

The five requested old figures are copied byte-for-byte from the given Git snapshot. Their source paths and SHA256 are in `provenance/HISTORICAL_FIGURES.json`. Renderer reuse preserves the original true-triangle Open3D ray renderer and the same optional per-face colour adapter. No normals-only or display smoothing is claimed as a change to geometry.
