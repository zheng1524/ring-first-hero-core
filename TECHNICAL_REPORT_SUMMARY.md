# Ring-First/HERO collaborator release — execution summary

Date: 2026-11-17. Task: `TASK-RING-FIRST-HERO-COLLAB-RELEASE-001`.

## Delivered scope

An independent Python package/CLI, frozen version lock, real controlled G01 example index, actual new official inference, optional original cleaning, twelve core/original figures, actual separate-source GLBs and an offline HTML viewer. The old research workspaces remain read-only.

The package does not import old experiment modules or include Dxy, Body fitting, experimental BA, SDF, TSDF or Mesh fusion. It declares the reference RGB map and Ceres-derived source-camera ancestry rather than pretending a circular Ring independently resolves a whole camera trajectory.

## Verified results

| Item | Actual result |
| --- | --- |
| Target recovery | Same c2w, selected candidate and FIT objective as frozen original initial camera; differences0 |
| Official parameter loading | All535 learned tensors /201670426 elements, original checkpoint SHA verified |
| New native depth |225280/225280 bitwise equal; every pixel difference0, MAE/P95/max0mm |
| Raw geometry |22733 vertices,43746 faces; authoritative coordinates/faces/Pixel IDs identical |
| Optional017 cleaning |State and reason bits identical; Trusted38815 / Uncertain879 / Rejected0 / Unknown4052 |
| Native geometry round trip |Maximum projection error about1.71e-13 pixels; original depth-jump maximum0.7498398mm |
| Geometry limitations |1106 boundary edges,0 nonmanifold edges,0 degenerate faces,300 unreferenced native vertices;160 faces with signed samples inside CAD |
| Browser |Actual localhost HTTP and headless Chrome load the real GLBs with independent source controls; no CDN dependency |

Execution receipts and test outputs are in `validation/`. Complete geometric truth remains `NOT_EVALUABLE`. A newly generated output is never backfilled from a historical result.

## Version corrections and gaps

The three requested project-script SHA values and checkpoint SHA pass. The given “official”4483e25 commit does **not**: it was the parent local research Git commit. All105 used source/config files instead match official5bd49bba exactly. DINOv2's156 files also match its separately pinned upstream commit. Both the incorrect old claim and its correction are retained in VERSION_LOCK.

The requested module registry/T14–T20 was absent. Actual source functions and frozen SHA receipts are fully listed; no fictitious catalogue was created.

The new environment reuses existing read-only third-party packages. A full fresh CUDA environment install was not performed. Environment setup instructions distinguish executed editable installation/CLI commands from a new-host recipe.

## Real data and publishing

Original videos, original RGB/Mask collections, checkpoint weights, private machine configuration and full external dependency trees are excluded. The prepared real example bundle remains local-only with a real SHA/path index and controlled-access procedure. Curated derived images, known CAD, small actual GLBs and audit materials are suitable for the authorized private collaborator repository.

Final repository URL, complete commit SHA and confirmed visibility are recorded in the release handoff after actual creation/push. They are not asserted merely because a local commit exists.

## Reproduction and review

Run the commands in README/REPRODUCE with authorized data and pinned official dependencies. Important entry points: `camera.py`, `hero.py`, `geometry.py`, `cleaning.py` and `visualization.py`. Exact design/code correspondence is in METHOD_AND_SOURCE_AUDIT, and function identities are in MODULE_MIGRATION.csv.

This completes a minimal real engineering reproduction. It does not resolve multi-source disagreement, certify full camera truth, or promote hidden surfaces to measured anatomy. Further algorithm changes should be separate research tasks.
