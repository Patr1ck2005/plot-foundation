# Phase 1: Independent Plot Foundation

Status: completed on 2026-08-06

Phase 2 style policy work is now implemented as additive API in the same
compatibility line and is recorded below.

Date: 2026-08-06

## Scope

- Correct the earlier single-distribution design.
- Establish `plot-foundation` independently from `eigenmode-analysis`.
- Migrate schema-neutral line/scatter rendering.
- Add robust ribbon and color-mapped line primitives based on mature myPlots
  experience.
- Add scoped style and explicit save contracts.
- Reconnect myPlots and ResearchAgentWorkbench with independent provenance.

## Release gate

- Package tests pass in both consumer analysis environments.
- Both consumer acceptance examples use the independent distribution.
- Existing legacy/shared and Workbench before/after image contracts remain
  unchanged.
- `eigenmode-analysis` contains no plotting or Matplotlib dependency.
- Stable wheels for both shared distributions work without source path injection.

## Evidence

- Plot Foundation: 10 passed in each consumer analysis environment after the
  style/preset additions.
- myPlots: 14 shared adapter tests, including plain-line equivalence, exact
  ribbon vertices, and NaN-safe dynamic color.
- Workbench: 83 passed with both shared source trees; 80 passed and 1 skipped
  without Plot Foundation; 74 passed and 2 skipped without either shared library.
- myPlots legacy/shared plain PNG SHA256 hashes are identical.
- DS-001 produced four nonblank real-data band/Q figures with Plot Foundation
  installed-wheel provenance from Workbench's analysis venv.
- The current compatibility-line wheel is `plot_foundation-0.1.1-py3-none-any.whl`.
- A disposable venv imported Plot Foundation from `site-packages`, classified
  the install as `wheel`, and rendered a nonblank smoke PNG.
- Phase 2 adds scoped paper/preview profiles, semantic figure presets, explicit
  aspect handling, and tests for the A-derived 1.5-inch panel convention.
