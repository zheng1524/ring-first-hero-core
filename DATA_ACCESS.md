# Controlled real example access

The repository is Private. Private visibility alone is not permission to redistribute original data. Original videos, full RGB/Mask collections, personal data and model weights are not committed.

## What the maintainer has prepared

The real example is a local-only bundle, indexed by `examples/G01_demo/DATA_MANIFEST.json` and the release-local bundle receipt. It contains:

- Target `G01_v004_raw00341`.
- Original supports `G01_v004_raw00326`, `G01_v004_raw00360`, `G01_v004_raw00204`.
- Four actual RGB images and original multiclass masks, frozen K/c2w, known Ring CAD.
- A declared real reference-video RGB/SIFT map for the target camera demonstration.
- Native historical HERO depth and Raw Mesh, plus class/face evidence, solely for comparison after the new output is written.

All four frames belong to G01/video004. They are not Blender renders, resized old depth, other-video poses or synthetic HERO proxies. No original video is needed to run this controlled example.

## Collaborator procedure

1. Obtain access to this private code repository from the maintainer.
2. Ask the maintainer for the **G01 Ring-First/HERO v1 controlled example bundle** through an approved institutional/private transfer channel. Repository access does not grant an existing download endpoint.
3. Verify the bundle SHA256 and per-file `DATA_MANIFEST.json` with the receipt supplied for that transfer.
4. Extract it into `.local_data/G01_demo/`; keep it excluded from Git.
5. Acquire official HERO weights separately, subject to the upstream terms. The maintainer does not re-host them in this repository.

No public dataset URL, collaborator account or cloud bucket is invented here. The maintainer's actual local bundle path and SHA are in the delivered local `validation/CONTROLLED_DATA_BUNDLE.json` index. An index is not a claim that the raw bundle was uploaded or backed up remotely.

## Data schema

`DATA_MANIFEST.json` records relative file paths, byte counts, SHA256, one target followed by three support frames, 640×360 K and `c2w_mm`, and conditional camera status. Each frame has `rgb`, `labels`, `K`, `c2w_mm`, `id` and qualification fields. Labels are 0 Background / 1 Polyp / 2 Ring.

The supplied SIFT reference map has `X` in the same Ring world/mm and original 128-dimensional descriptors `des`; its canonical camera ancestry is conditional. It is not a Body surface or HERO/GT point cloud. New videos need an appropriate declared reference map or independently established fixed cameras. This v0.1 release does not silently manufacture one.

## What is safe to browse in Git

The curated derived figures, known R10 CAD, actual derived GLBs, source/hash records and test receipts are included for authorized collaborator review. The GLBs contain no RGB video or complete source-data collection. Actual source identities remain available, and no overlapping meshes are called a fused anatomical surface.
