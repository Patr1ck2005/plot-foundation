# Phase 09: Legacy Line and Heatmap Ownership

Release `0.1.8` moves the mature myPlots `plot_line_advanced` and
`plot_2d_heatmap` implementations into Plot Foundation. This includes the
gradient-fill `imshow` path, dynamic color line path, ribbon path, and the
historical x-first complex heatmap policy.

myPlots retains `advance_plot_styles.line_plot.plot_line_advanced` and
`core.plot_3D_params_space_plt.plot_2d_heatmap` as compatibility exports. No
Visualizer call sites need to change, and no renderer creates, saves, shows, or
closes figures outside the caller's explicit request.
