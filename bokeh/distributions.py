
from bokeh.layouts import column, row
from bokeh.plotting import figure, show, curdoc
from bokeh.models import Slider, RangeSlider, NumericInput, Label, Div
from scipy.stats import norm
import numpy as np

class BokehContDist:
    def __init__(self, sample_func, pdf, cdf, *func_args, x_range=None):
        self.sample_func = sample_func
        self.pdf = pdf
        self.cdf = cdf
        self.params = {}
        
        # Make figure
        if x_range is None:
            x_range = (-5, 5)
        plot = figure(
            x_range=x_range, 
            tools='reset,pan,wheel_zoom,lasso_select', 
            background_fill_color="#fafafa", 
            width=700,
            height=400,
            # sizing_mode='scale_both',
        )
        plot.title.text_font_size = "3em"
        
        # Default plot
        samples = sample_func(*func_args, size=1000)
        hist, edges = np.histogram(samples, density=True, bins=50)
        histplot = plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="grey", line_color="white", alpha=0.5, legend_label="samples")
        x = np.linspace(plot.x_range.start, plot.x_range.end, 100)
        pdfplot = plot.line(x, pdf(x, *func_args), line_color="#1f77b4", line_width=2, legend_label="PDF")
        cdfplot = plot.line(x, cdf(x, *func_args), line_color="orange", line_width=2, legend_label="CDF")
        
        # Build sliders / inputs
        range_slider = RangeSlider(
            title=" x-axis range",
            start=x_range[0] - 1,
            end=x_range[1] + 1,
            step=1,
            value=(plot.x_range.start, plot.x_range.end),
            # sizing_mode='scale_both',
        )
        range_slider.js_link("value", plot.x_range, "start", attr_selector=0)
        range_slider.js_link("value", plot.x_range, "end", attr_selector=1)
        range_slider.on_change("value", self.update)
        
        N_input = NumericInput(title="Sample size", value=1000, low=1, high=100000)
        bins_input = NumericInput(title="Number of bins", value=50, low=0, high=100)
        N_input.on_change("value", self.update)
        bins_input.on_change("value", self.update)
        self.plots = {
            "main": plot,
            "hist": histplot,
            "pdf": pdfplot,
            "cdf": cdfplot,
        }
        self.inputs = {
            "range": range_slider,
            "N": N_input,
            "bins": bins_input
        }

    def sample_data(self, *func_args, **func_kwargs):
        samples = self.sample_func(*func_args, size=self.inputs["N"].value, **func_kwargs)
        hist, edges = np.histogram(samples, density=True, bins=self.inputs["bins"].value)
        self.plots["hist"].data_source.data = {"top": hist, "left": edges[:-1], "right": edges[1:]}
    
    def update_dists(self, *func_args, **func_kwargs):
        x = np.linspace(self.plots["main"].x_range.start, self.plots["main"].x_range.end, 1000)
        self.plots["pdf"].data_source.data = {"x": x, "y": self.pdf(x, *func_args, **func_kwargs)}
        self.plots["cdf"].data_source.data = {"x": x, "y": self.cdf(x, *func_args, **func_kwargs)}
        
    def add_param_sliders(self, *func_args, **func_kwargs):
        self.func_args = func_args
        self.func_kwargs = func_kwargs
        for slider in func_args:
            slider.on_change("value", self.update)
            
        for slider in func_kwargs.values():
            # TODO: if slider
            slider.on_change("value", self.update)
        
    def update(self, attr, old, new):
        func_args = [p.value for p in self.func_args]
        func_kw = {k: v.value for (k, v) in self.func_kwargs.items()}
        
        # Sample data
        self.sample_data(*func_args, **func_kw)
        
        # Redo pdf/cdf
        self.update_dists(*func_args, **func_kw)
        
    def get_layout(self):
        self.plots["main"].legend.location = "top_left"
        layout = column(
            row(
                column(
                    self.plots["main"], 
                    self.inputs["range"],
                    sizing_mode='scale_both',
                ), 
                column(
                    *self.func_args,
                    *self.func_kwargs.values(),
                    self.inputs["N"],
                    self.inputs["bins"],
                    width=200,
                ),
            )
        )
        return layout

from scipy.stats import norm, beta, gamma

normal = BokehContDist(norm.rvs, norm.pdf, norm.cdf)
normal.add_param_sliders(
    loc=Slider(start=-10, end=10, value=0, step=.5, title="loc", max_width=100),
    scale=Slider(start=0.1, end=10, value=1, step=.1, title="scale", max_width=100)
)
layout = normal.get_layout()
curdoc().add_root(layout)

beta = BokehContDist(beta.rvs, beta.pdf, beta.cdf, 3, 3, x_range=(-1, 1))
beta.add_param_sliders(
    Slider(start=0.1, end=10, value=3, step=.1, title="a"),
    Slider(start=0.1, end=10, value=3, step=.1, title="b"),
    loc=Slider(start=-10, end=10, value=0, step=.5, title="loc", max_width=100),
    scale=Slider(start=0.1, end=10, value=1, step=.1, title="scale", max_width=100)
)
layout = beta.get_layout()
curdoc().add_root(layout)
