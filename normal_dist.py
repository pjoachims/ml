# normal_dist.py

from bokeh.layouts import column, row
from bokeh.plotting import figure, show, curdoc
from bokeh.models import Slider, RangeSlider, NumericInput, Label
from scipy.stats import norm
import numpy as np

# Make figure
plot = figure(
    x_range=(-5, 5), 
    tools='reset,pan,wheel_zoom,lasso_select', 
    background_fill_color="#fafafa", 
    width=700,
    height=400,
    # sizing_mode='scale_both',
)
plot.title.text_font_size = "3em"

# Default plot
samples = norm.rvs(size=1000)
hist, edges = np.histogram(samples, density=True, bins=50)
histplot = plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="grey", line_color="white", alpha=0.5, legend_label="samples")
x = np.linspace(plot.x_range.start, plot.x_range.end, 100)
pdfplot = plot.line(x, norm.pdf(x), line_color="#1f77b4", line_width=2, legend_label="PDF")
cdfplot = plot.line(x, norm.cdf(x), line_color="orange", line_width=2, legend_label="CDF")

# Build sliders / inputs
range_slider = RangeSlider(
    title=" x-axis range",
    start=-20,
    end=20,
    step=1,
    value=(plot.x_range.start, plot.x_range.end),
    # sizing_mode='scale_both',
)
range_slider.js_link("value", plot.x_range, "start", attr_selector=0)
range_slider.js_link("value", plot.x_range, "end", attr_selector=1)

N_input = NumericInput(title="Sample size", value=1000, low=1, high=100000, max_width=100)
bins_input = NumericInput(title="Number of bins", value=50, low=0, high=100, max_width=100)
loc_slider = Slider(start=-10, end=10, value=0, step=.5, title="loc", max_width=100)
scale_slider = Slider(start=0.1, end=10, value=1, step=.1, title="scale", max_width=100)

# Connect to callback
def update(attr, old, new): 
    N = N_input.value
    loc = loc_slider.value
    scale = scale_slider.value
    samples = norm.rvs(loc=loc, scale=scale, size=N_input.value)
    hist, edges = np.histogram(samples, density=True, bins=bins_input.value)
    histplot.data_source.data = {"top": hist, "left": edges[:-1], "right": edges[1:]}
    x = np.linspace(plot.x_range.start, plot.x_range.end, 100)
    pdfplot.data_source.data = {"x": x, "y": norm.pdf(x, loc=loc, scale=scale)}
    cdfplot.data_source.data = {"x": x, "y": norm.cdf(x, loc=loc, scale=scale)}

N_input.on_change("value", update)
bins_input.on_change("value", update)
range_slider.on_change("value", update)
loc_slider.on_change("value", update)
scale_slider.on_change("value", update)

# Styling
plot.legend.location = "top_left"
plot.grid.grid_line_color="white"

# Set layout
layout = row(
    column(
        plot, 
        range_slider,
        sizing_mode='scale_both',
    ), 
    column(
        loc_slider, 
        scale_slider, 
        N_input, 
        bins_input,
        width=100,
    ),
)
curdoc().add_root(column(layout))
curdoc().title = "wabbadabba"
