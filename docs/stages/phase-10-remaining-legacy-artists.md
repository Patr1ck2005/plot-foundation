# Phase 10: remaining legacy artists

Release 0.1.9 moved the remaining domain-neutral Matplotlib artist bodies from
myPlots into `plot_foundation.legacy_*` modules. Existing myPlots functions are
imports or thin adapters; figure lifecycle and scientific semantics remain in
the consumer.

The migrated surface covers scatter, contours, path and multiline plots,
simple shapes/annotations, polar lines, and phi/S3 image rendering. All tests
use the Agg backend and close figures.

Verification completed with 29 package tests, the myPlots adapter suite, the
Workbench suite, and stable-wheel provenance in both consumers.

