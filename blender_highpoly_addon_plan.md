# Blender Add-on Plan: High-Poly ZBrush Mesh Repair (Design Only)

## 1) Architecture

### 1.1 Module layout (separation of concerns)
- **UI Layer**
  - Panels in the 3D View sidebar for analysis/fix controls.
  - Read-only summary section with counts, severity, and recommended next step.
- **Operator Layer**
  - Stateless operators for: scan, classify, select, report, and each conservative fix.
  - Operators call service functions and never directly own long-lived analysis state.
- **Analysis Core**
  - Mesh scanners that compute per-vertex/per-edge/per-face diagnostics.
  - Classification engine that labels flagged regions as likely *normals-related* vs *geometry-related*.
- **Fix Core**
  - Conservative, opt-in repair routines with strict safeguards and dry-run support.
- **Data/State Layer**
  - Scene-level properties for user settings.
  - Object-level cache for latest scan results (IDs/index sets + aggregate metrics).
- **Reporting Layer**
  - Human-readable report generation with compact stats and optional CSV/JSON export.

### 1.2 Execution model for dense meshes
- Use **two-phase analysis**:
  1. Fast coarse pass (cheap heuristics) to find suspect zones.
  2. Focused detailed pass only on candidate neighborhoods.
- Use chunked iteration and progress updates to keep UI responsive.
- Cache derived metrics to avoid recomputing unchanged data.
- Re-run only invalidated portions when settings change.

### 1.3 Safety model
- No destructive operation runs by default.
- Every fix supports preview-style counts before apply.
- Deletion-oriented actions are explicitly gated (checkbox + threshold).
- Always preserve undo stack and print exact affected counts.

---

## 2) File Tree

```text
zbrush_highpoly_repair/
  __init__.py
  addon_manifest.py

  ui/
    panel_main.py
    panel_report.py

  operators/
    op_scan_mesh.py
    op_select_issues.py
    op_report_issues.py
    op_fix_recalc_normals.py
    op_fix_clear_custom_normals.py
    op_fix_degenerate_geometry.py
    op_fix_weld_near_duplicates.py
    op_fix_remove_isolated_verts.py

  core/
    analysis/
      scan_coarse.py
      scan_detailed.py
      classify_issues.py
      region_builder.py
      metrics.py
    fixes/
      fix_normals.py
      fix_geometry.py
      fix_safety.py
    reporting/
      report_builder.py
      serializers.py

  data/
    properties.py
    cache_store.py
    issue_types.py

  utils/
    mesh_access.py
    thresholds.py
    logging.py
    timing.py

  tests_manual/
    manual_test_matrix.md
```

---

## 3) Detection Strategy

### 3.1 Principles
- Treat detection as **probabilistic suspicion**, not absolute truth.
- Prefer false positives over false negatives in scan stage, then tighten in classification.
- Work per connected component/region so users can inspect localized damage.

### 3.2 Signals for normals-related anomalies
- Large local shading discontinuity despite smooth topology.
- Sharp divergence between face normal neighborhood and vertex normal direction.
- Presence of custom split normals with outlier vectors.
- Small isolated clusters where normal variance is high but geometry metrics are healthy.

### 3.3 Signals for geometry-related anomalies
- Degenerate faces (zero or near-zero area).
- Extremely short edges relative to local median edge length.
- Near-duplicate vertices within configurable epsilon.
- Isolated vertices or tiny disconnected fragments below user threshold.
- Non-manifold or locally inconsistent topology indicators.

### 3.4 Region scoring and classification
- Build adjacency graph around flagged primitives.
- Compute per-region scores:
  - `S_normals`: normal inconsistency + custom normal outliers.
  - `S_geo`: degeneracy + duplicate/weld cues + isolation cues.
- Label rule:
  - If `S_normals >> S_geo`: **Likely Normals Issue**.
  - If `S_geo >> S_normals`: **Likely Geometry Issue**.
  - Otherwise: **Mixed / Needs Manual Review**.

### 3.5 Dense mesh performance notes
- Use local neighborhood sampling radius in edge-count space (not world units only).
- Avoid global all-pairs duplicate checks; use spatial hashing grid/k-d style buckets.
- Keep threshold math scale-aware (object bounding box and local edge statistics).

---

## 4) Fix Strategy

### 4.1 Order of conservative fixes (recommended pipeline)
1. **Recalculate normals** (safe, reversible).
2. **Clear corrupted custom normals** (only if present/suspect).
3. **Resolve degenerates** (flag + optional cleanup action).
4. **Optional weld near-duplicates** (small epsilon, bounded impact).
5. **Optional isolated-vertex removal** (strictly guarded, tiny-count only).

### 4.2 Fix details
- **Recalculate normals**
  - Apply only to selected issue regions (or whole mesh by explicit option).
  - Re-scan region and compare score deltas.
- **Clear custom normals**
  - Only clears custom split normals layer; does not alter geometry directly.
  - Recommend immediate rescan to verify artifact removal.
- **Degenerate geometry handling**
  - Default action: select/report only.
  - Optional cleanup action: dissolve/remove strictly degenerate elements.
- **Weld near-duplicate vertices**
  - Off by default.
  - Uses epsilon tied to local median edge length.
  - Hard cap on max merged vertices per run to prevent over-collapse.
- **Remove isolated broken vertices**
  - Off by default and requires explicit confirmation toggle.
  - Only vertices with no valid face contribution and below fragment-size threshold.

### 4.3 Post-fix validation
- Mandatory mini re-scan of touched regions.
- Report before/after counts and confidence trend.
- If worsening detected, recommend undo and lower aggressiveness.

---

## 5) Risk Analysis

### 5.1 False classification risk
- **Risk**: Mixed artifacts may be mislabeled as normals-only.
- **Mitigation**: Mixed category + confidence score + manual inspection selection.

### 5.2 Over-fixing risk
- **Risk**: Welding/deletion can alter sculpt detail.
- **Mitigation**: Off-by-default, tight thresholds, per-run caps, dry-run preview.

### 5.3 Scale sensitivity risk
- **Risk**: Absolute epsilon fails on very large/small meshes.
- **Mitigation**: Relative thresholds from bbox and local edge statistics.

### 5.4 Performance risk on dense meshes
- **Risk**: Full scans stall UI.
- **Mitigation**: Coarse-to-fine scanning, chunking, cache reuse, region-only rescans.

### 5.5 User trust risk
- **Risk**: Automatic destructive behavior reduces reliability.
- **Mitigation**: Conservative defaults, explicit confirmations, transparent reports.

---

## 6) Operator List

- `HPMESH_OT_scan_issues`
  - Scan active mesh and populate issue cache.
- `HPMESH_OT_select_region`
  - Select next/previous issue region by severity.
- `HPMESH_OT_select_by_type`
  - Select issues by label: normals / geometry / mixed.
- `HPMESH_OT_report_issues`
  - Generate textual report (optionally export JSON/CSV).
- `HPMESH_OT_fix_recalc_normals`
  - Recalculate normals in safe scope.
- `HPMESH_OT_fix_clear_custom_normals`
  - Clear custom normals data layer.
- `HPMESH_OT_fix_degenerate_geometry`
  - Select or optionally clean strict degenerates.
- `HPMESH_OT_fix_weld_near_duplicates`
  - Optional controlled weld of near-duplicates.
- `HPMESH_OT_fix_remove_isolated_vertices`
  - Optional guarded deletion of truly isolated broken vertices.
- `HPMESH_OT_rescan_touched_regions`
  - Validate and update issue scores after fixes.

---

## 7) Property List

### 7.1 Scan properties
- `scan_scope` (ENUM): active selection / visible / full object.
- `coarse_only` (BOOL): fast first pass only.
- `max_regions` (INT): cap number of reported regions.
- `normal_outlier_angle_deg` (FLOAT): normal deviation threshold.
- `degenerate_area_epsilon` (FLOAT): near-zero face area threshold.
- `short_edge_ratio` (FLOAT): edge anomaly threshold vs local median.
- `duplicate_vertex_epsilon` (FLOAT): near-duplicate vertex merge distance.
- `island_min_size` (INT): tiny fragment threshold.

### 7.2 Fix safety properties
- `fix_scope` (ENUM): selected regions / all flagged / whole mesh.
- `dry_run` (BOOL): show impact counts without applying.
- `require_confirm_destructive` (BOOL): must be true to allow deletion-type operations.
- `max_elements_to_modify` (INT): hard cap for one operation.
- `abort_on_worsen` (BOOL): rollback recommendation when re-scan score worsens.

### 7.3 Reporting properties
- `show_confidence` (BOOL): include confidence per region.
- `report_format` (ENUM): text / JSON / CSV.
- `include_thresholds` (BOOL): embed effective thresholds in report.

---

## 8) Manual Test Plan

### 8.1 Test assets
- Dense ZBrush import with known shading pin artifacts.
- Dense clean control mesh.
- Mesh with synthetic degenerates (zero-area faces, loose verts).
- Mesh with duplicated vertices in small regions.
- Mixed-case mesh (both normals and topology issues).

### 8.2 Functional tests
1. **Baseline scan**
   - Run scan on each asset.
   - Verify issues found where expected and none/minimal on clean control.
2. **Classification check**
   - Confirm normals-only case labels as normals.
   - Confirm degenerate case labels as geometry.
   - Confirm mixed case produces mixed/manual review zones.
3. **Selection and reporting**
   - Step through regions by severity.
   - Export report and verify counts/types match viewport selection.

### 8.3 Fix validation tests
4. **Normals recalc safety**
   - Apply recalc on flagged regions only.
   - Confirm no unexpected global geometry change.
5. **Clear custom normals**
   - On mesh with custom split normals, clear and rescan.
   - Verify artifact reduction where corruption was due to custom normals.
6. **Degenerate handling**
   - With cleanup disabled, confirm only select/report.
   - With cleanup enabled, confirm only strict degenerates affected.
7. **Weld near-duplicates**
   - Run with tiny epsilon and cap.
   - Verify local cleanup without broad detail loss.
8. **Isolated vertices removal**
   - Ensure operation is blocked unless destructive confirm is enabled.
   - Verify only truly isolated/broken vertices removed.

### 8.4 Robustness/performance tests
9. **Dense mesh stress**
   - Run scan/fixes on high poly mesh (>5M verts if available).
   - Confirm tool remains responsive and completes with progress feedback.
10. **Undo/redo integrity**
    - Validate each fix is a clean undo step.
11. **Threshold sensitivity sweep**
    - Test low/medium/high strictness presets.
    - Confirm predictable shift in flagged counts.

### 8.5 Acceptance criteria
- No destructive changes occur with default settings.
- Problem regions are selectable and clearly reported.
- Normals-vs-geometry classification is explainable and mostly correct.
- Optional destructive operations require explicit user intent.
- Dense meshes can be processed in practical time with no crashes.
