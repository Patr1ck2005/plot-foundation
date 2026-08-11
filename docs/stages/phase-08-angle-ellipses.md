# Phase 08: Angle-Form Polarization Ellipses

Release 0.1.7 moves myPlots' remaining general `(phi, chi)` ellipse renderer
into Plot Foundation. The shared renderer preserves sampling, scale, color-by
chi/phi policy, color limits, linewidth, alpha, and equal-aspect behavior.

myPlots retains its historical function name in
`core.data_postprocess.momentum_space_toolkits`; the wrapper returns the
Matplotlib `PatchCollection` exactly as before. Plot Foundation owns no field
names, DataFrame schema, or figure-saving policy.
