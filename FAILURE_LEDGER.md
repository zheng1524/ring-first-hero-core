# Failure and limitation ledger

| ID | Stage | Actual issue | Action / final state |
| --- | --- | --- | --- |
| P01 | Version audit | Claimed official MVSAnywhere commit4483e25 was actually the parent local research Git commit; official API returned422 | Preserved false claim as such; all105 used source/config files verified byte-identical to upstream5bd49bba; no algorithm or weight replacement |
| P02 | Registry | REUSABLE_MODULES.md/T14–T20 not present at the required snapshot or inspected source worktree | Marked MISSING; no invented registry entries; actual module/function/hash lineage is supplied |
| E01 | First camera wrapper execution | Bound Python function namespace omitted __builtins__, causing KeyError before solving | Corrected the namespace binding only; subsequent actual target camera and FIT objective exactly match frozen output |
| E02 | Initial G03 reference export | First two general-plan entries included video005; same-video assertion stopped export | Explicitly selected the first two video004 entries, without looking at geometry/output quality; no unverified cross-video transform introduced |
| E03 | Initial gallery resource check | Browser check ran before local viewer dependencies/link relocation finished; a local resource returned404 | Completed local licensed viewer assets and gallery-contained links; rerun checks actual GLB loading and internal resources |
| Q01 | Real Raw geometry | Open boundaries, unreferenced native points and some CAD penetration remain | Preserved original geometry and reported actual counts; no repair/filling/deletion to improve the release |
| Q02 | Camera scope | One support camera includes historical selected-subset Ceres refinement; reference-map ancestry remains conditional | Frozen support camera retained, per-frame provenance recorded; no claim that target-only Ring solve recreated full video BA |
| Q03 | Deployment | Fresh standalone CUDA installation was not built; existing read-only packages were reused | Exact tested components/path-reuse mode recorded. New-host recipe is labelled as a recipe, not falsely reported as executed |
| Q04 | Data access | Real input bundle and checkpoint are not Git assets | Controlled bundle index and genuine local path supplied; no invented public download or claim that weights/data were pushed |

No scientific reconstruction failure is inferred from an engineering wrapper or browser setup issue. Absolute geometric accuracy remains NOT_EVALUABLE. The official source version metadata error is explicitly corrected, not silently marked verified.
