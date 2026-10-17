"""Render typed public specs from generic analytic functions, without private inputs."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
from plot_foundation import (
    AxesSpec, LinePlotSpec, LineSeries, SeriesStyle, RibbonSeries, RibbonStyle,
    ColorMappedLineSeries, ColorMappedLineStyle, HeatmapPlotSpec, HeatmapStyle,
    MultiSurfacePlotSpec, SurfaceLayer, SurfaceStyle, VectorFieldPlotSpec, VectorFieldStyle,
    render_line_plot, render_heatmap, render_multi_surface_3d, render_vector_field,
    render_polarization_ellipses, render_poincare_trajectory, profile_context,
)
from _showcase import COLORS, STYLE, Showcase, plt, tidy3d


def line_panel(ax):
    x=np.linspace(-3,3,241); y=np.exp(-x*x/1.5)*np.cos(2*x)
    spec=LinePlotSpec(series=(
        RibbonSeries(x,y,np.full_like(y,.13),style=RibbonStyle(color=COLORS[0],alpha=.16)),
        LineSeries(x,y,label="analytic signal",style=SeriesStyle(color=COLORS[0],linewidth=1)),
        LineSeries(x[::12],y[::12],label="sampled values",style=SeriesStyle(kind="scatter",color=COLORS[1],scatter_size=11)),
    ), axes=AxesSpec(xlabel="Coordinate t",ylabel="Amplitude",legend=True,legend_fontsize=7))
    result=render_line_plot(spec,ax=ax)
    assert result.axes is ax and result.figure is ax.figure
    return result


def grid_data():
    x,y=np.linspace(-2,2,61),np.linspace(-1,1,35)
    X,Y=np.meshgrid(x,y,indexing="ij")
    z=np.sin(1.6*X)*np.cos(2.3*Y)
    hole=(X-.55)**2+(Y+.15)**2<.29**2
    z[hole]=np.nan
    return x,y,X,Y,z,hole


def heat_panel(fig,ax,cax=None,vector=False):
    x,y,X,Y,z,hole=grid_data()
    result=render_heatmap(HeatmapPlotSpec(x,y,z,axes=AxesSpec(xlabel="x",ylabel="y",aspect="equal"),style=HeatmapStyle(cmap="RdBu_r",vmin=-1,vmax=1)),ax=ax)
    np.testing.assert_allclose(result.artists[0].get_array().filled(np.nan),z.T,equal_nan=True)
    assert np.ma.getmaskarray(result.artists[0].get_array()).sum()==int(hole.sum())
    if vector:
        render_vector_field(VectorFieldPlotSpec(x,y,-Y,X,step=(6,5),axes=AxesSpec(xlabel="x",ylabel="y",aspect="equal"),style=VectorFieldStyle(color="#182331",normalize=True,scale=13,width=.004)),ax=ax)
    if cax is not None:
        cb=fig.colorbar(result.artists[0],cax=cax);cb.set_label("Signed scalar",fontsize=7);cb.ax.tick_params(labelsize=7)
    return result


def surface_panel(ax):
    x,y,X,Y,z,hole=grid_data()
    height=.25*(X*X+.6*Y*Y)
    height[hole]=np.nan
    # Height, color and opacity remain independent channels in the public spec.
    spec=MultiSurfacePlotSpec(x,y,(
        SurfaceLayer(z=height,color_values=z,alpha=1),
        SurfaceLayer(z=height+.85,color_values=-z,alpha=.88)),
        style=SurfaceStyle(cmap="RdBu_r",vmin=-1,vmax=1,rstride=2,cstride=2),
        xlabel="x",ylabel="y",zlabel="Height",elev=23,azim=-59,box_aspect=(1.5,1,1))
    result=render_multi_surface_3d(spec,ax=ax)
    assert len(result.artists)==2
    assert np.isnan(spec.layers[0].z).sum()==hole.sum()
    tidy3d(ax)
    return result


def main(out):
    show=Showcase(out,"Plot Foundation · typed rendering",__file__,
        "All quantities are dimensionless analytic test functions. Grids are x-first with shape (61,35), displayed at the actual 4:2 coordinate aspect. Red/blue represent positive/negative scalar values over [-1,1]; white holes are NaN, not zero. Surface height and color represent different arrays. Stokes components lie on the unit sphere; ellipse color is S3, with no physical propagation convention implied.",
        [{"intrinsic_dimension":"1D","sampling_topology":"uniform path","parameter_space":"generic coordinate","quantity":"analytic amplitude with illustrative interval","compatible_views":["line","scatter","ribbon","color line"],"selected_views":"typed line family","transformation_status":"direct raw analytic samples; interval is illustrative, not statistical uncertainty"},
         {"intrinsic_dimension":"2D","sampling_topology":"non-square regular grid","parameter_space":"generic x,y","quantity":"signed scalar, vectors, surface height and Stokes texture","compatible_views":["heatmap","surface","vectors","ellipses"],"selected_views":"orientation/mask comparison, independent surface channels and polarization","transformation_status":"direct analytic arrays"},
         {"intrinsic_dimension":"1D","sampling_topology":"ordered angular path","parameter_space":"angle","quantity":"unit Stokes vector","compatible_views":["component lines","Poincare trajectory"],"selected_views":"Poincare trajectory","transformation_status":"direct analytic vector samples"}])
    original=plt.rcParams.copy()
    with profile_context("publication_minimal"),plt.rc_context(STYLE):
        fig=plt.figure(figsize=(210/25.4,76/25.4),layout="constrained")
        a=fig.add_subplot(131);b=fig.add_subplot(132);c=fig.add_subplot(133,projection="3d")
        line_panel(a);heat_panel(fig,b);surface_panel(c)
        c.set_zlabel("");c.text2D(.98,.88,"Height",transform=c.transAxes,ha="right",fontsize=8)
        for ax,t in zip((a,b,c),("Typed lines & intervals","x-first scalar grid","Independent surface channels")):ax.set_title(t,loc="left",fontsize=8)
        show.save(fig,"hero","One specification layer, many views","Actual public renderers draw analytic arrays onto caller-owned axes. Each view retains its own data meaning.")
        fig,axs=plt.subplots(2,1,figsize=(105/25.4,100/25.4),layout="constrained")
        line_panel(axs[0])
        t=np.linspace(-3,3,241)
        render_line_plot(LinePlotSpec((ColorMappedLineSeries(t,np.sin(2*t),t,style=ColorMappedLineStyle(cmap="plasma",vmin=-3,vmax=3,linewidth=2)),),axes=AxesSpec(xlabel="Coordinate t",ylabel="sin(2t)")),ax=axs[1])
        axs[1].set_title("Segment color encodes t",loc="left",fontsize=8)
        show.save(fig,"line-family","Lines, scatter, ribbons and color","The shaded interval is ±0.13 around the analytic signal, used to demonstrate ribbon rendering; it is not measured uncertainty.")
        fig=plt.figure(figsize=(105/25.4,65/25.4));ax=fig.add_axes((.14,.20,.70,.70));cax=fig.add_axes((.88,.25,.025,.55))
        heat_panel(fig,ax,cax,True)
        show.save(fig,"grid-orientation","Non-square orientation and a genuine NaN hole","A 61 × 35 x-first scalar grid with a circular missing region and a sampled rotational vector field. Colorbar has its own axes, preserving the data rectangle.")
        fig=plt.figure(figsize=(125/25.4,90/25.4));ax=fig.add_axes((.01,.08,.74,.85),projection="3d");result=surface_panel(ax)
        ax.set_zlabel("");ax.text2D(.96,.88,"Height",transform=ax.transAxes,ha="right",fontsize=8)
        cax=fig.add_axes((.83,.25,.025,.52));cb=fig.colorbar(result.artists[0],cax=cax);cb.set_label("Color scalar",fontsize=7);cb.ax.tick_params(labelsize=7)
        show.save(fig,"surface-channels","Multi-layer surfaces with separate channels","Height is 0.25(x²+0.6y²), with the upper layer shifted by 0.85. Colors encode ±sin(1.6x)cos(2.3y); missing cells remain holes.")
        fig=plt.figure(figsize=(210/25.4,88/25.4),layout="constrained");a=fig.add_subplot(121);b=fig.add_subplot(122,projection="3d")
        x,y=np.linspace(-1,1,25),np.linspace(-1,1,25);X,Y=np.meshgrid(x,y,indexing="ij")
        phi=np.arctan2(Y,X)/2;chi=.45*np.sin(np.pi*X)*np.cos(np.pi*Y)
        s1,s2,s3=np.cos(2*chi)*np.cos(2*phi),np.cos(2*chi)*np.sin(2*phi),np.sin(2*chi)
        np.testing.assert_allclose(s1*s1+s2*s2+s3*s3,1,atol=1e-14)
        glyph=render_polarization_ellipses(x,y,s1,s2,s3,ax=a,step=(2,2),scale=.13,cmap="RdBu_r",linewidth=.6)
        a.set(xlabel="x",ylabel="y",aspect="equal",title="Analytic Stokes texture",xlim=(-1.1,1.1),ylim=(-1.1,1.1))
        t=np.linspace(0,2*np.pi,241);c=.48*np.sin(2*t)
        render_poincare_trajectory(np.cos(c)*np.cos(t),np.cos(c)*np.sin(t),np.sin(c),ax=b,cmap="plasma",linewidth=1.5)
        b.set(xlabel="$S_1$",ylabel="$S_2$",zlabel="$S_3$",title="Unit-sphere trajectory");tidy3d(b);b.view_init(22,-50)
        show.save(fig,"polarization","Polarization ellipses and Poincare path","The left texture is colored by S3; the right path is colored by progression from t=0 to 2π. All three Stokes components are normalized.")
    assert plt.rcParams==original,"Scoped rendering changed global rcParams"
    show.finish({"x_first_shape":[61,35],"renderer_transpose_matches":True,"nan_mask_preserved":True,"caller_axes_reused":True,"two_surface_layers":True,"unit_stokes_norm":True,"global_style_restored":True,"all_assertions_passed":True})


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--out",type=Path,default=Path("docs/assets/showcase"));main(p.parse_args().out)
