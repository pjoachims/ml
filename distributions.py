
from bokeh.layouts import column, row, gridplot
from bokeh.plotting import figure, show, curdoc
from bokeh.models import Slider, RangeSlider, Spinner, Label, Div
from scipy.stats import norm
import numpy as np
from bokeh.io import show
from bokeh.models import Button, CustomJS, Spinner, Select, CheckboxButtonGroup, TextAreaInput


class BokehContDist:
    def __init__(self, sample_func, pdf, cdf, *func_args, x_range=None, name="", **func_kwargs):
        self.sample_func = sample_func
        self.pdf = pdf
        self.cdf = cdf
        self.name = name
        self.func_args = func_args
        self.func_kwargs = func_kwargs
        
        # Handle args and kwargs
        self.sliders = {}
        for param in [*func_args] + [*func_kwargs.values()]:
            if hasattr(param, "on_change"):
                param.on_change("value", self.update)
                self.sliders[param.title] = param
        
        _init_args = [p.value if hasattr(p, "value") else p for p in func_args]
        _init_kwargs = {k: (v.value if hasattr(v, "value") else v) for (k, v) in func_kwargs.items()}
        
        # Make figure
        if x_range is None:
            x_range = (-5, 5)
        plot = figure(
            x_range=x_range, 
            tools='reset,pan,box_zoom, save,zoom_in, zoom_out', 
            background_fill_color="#fafafa", 
            # sizing_mode='scale_both',
            sizing_mode='scale_width',
        )
        plot.title.text_font_size = "3em"
        
        # Init plots
        samples = sample_func(*_init_args, size=1000, **_init_kwargs)
        hist, edges = np.histogram(samples, density=True, bins=50)
        histplot = plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="lightgrey", line_color="white", legend_label="samples")
        x = np.linspace(plot.x_range.start, plot.x_range.end, 100)
        pdfplot = plot.line(x, pdf(x, *_init_args, **_init_kwargs), line_color="#1f77b4", line_width=2, legend_label="PDF")
        cdfplot = plot.line(x, cdf(x, *_init_args, **_init_kwargs), line_color="orange", line_width=2, legend_label="CDF")
        self.plots = {
            "main": plot,
            "hist": histplot,
            "pdf": pdfplot,
            "cdf": cdfplot,
        }
        
        # X_range slider
        range_slider = RangeSlider(
            title=" x-axis range",
            start=x_range[0] - 1,
            end=x_range[1] + 1,
            step=0.1,
            value=(plot.x_range.start, plot.x_range.end),
        )
        range_slider.js_link("value", plot.x_range, "start", attr_selector=0)
        range_slider.js_link("value", plot.x_range, "end", attr_selector=1)
        range_slider.on_change("value", self.update)
        self.sliders["xrange"] = range_slider
        
        # Sampling options
        N_input = Spinner(title="Sample size", value=1000, step=50, low=1)
        N_input.on_change("value", self.update)
        bins_input = Spinner(title="Number of bins", value=50, low=1, step=5)
        bins_input.on_change("value", self.update)
        bins_input.js_on_change(
            "value", 
            CustomJS(
                args=dict(histplot=histplot.glyph),
                code="""histplot.line_width = 1 / cb_obj.value"""
            ),
        )
        
        sampling_checkboxes = CheckboxButtonGroup(labels=["Show", "Autoupdate"], active=[0, 1])
        def sampling_cb_callback(attr, old, new):
            if 0 not in self.inputs["sampling_checkboxes"].active:
                self.plots["hist"].visible = False
            else:
                self.update(None, None, None)
                self.plots["hist"].visible = True
        sampling_checkboxes.on_change("active", sampling_cb_callback)
        
        button_run = Button(label="Sample", button_type="success", align='end')
        def cb(new):
            return self.update(None, None, None, force_sampling=True)
        button_run.on_click(cb)
        
        # Slider adjusting
        select = Select(title="Slider for", value=[*self.sliders.keys()][0], options=[*self.sliders.keys()])
        start_or_end = Select(title="Prop", value="start", options=["start", "end", "step"], align='end')
        new_val = Spinner(title="Value", step=1e-6)
        button_update = Button(label="Update", button_type="success", align='end')
        def cb_update(new): 
            slider = self.sliders[select.value]
            setattr(slider, start_or_end.value, new_val.value)
            if start_or_end.value == "start" and new_val.value > getattr(slider, "value"):
                setattr(slider, "value", new_val.value)
            elif start_or_end.value == "end" and new_val.value < getattr(slider, "value"):
                setattr(slider, "value", new_val.value)
        button_update.on_click(cb_update)
    
        
        self.inputs = {
            "range": range_slider,
            "N": N_input,
            "bins": bins_input,
            "sampling_checkboxes": sampling_checkboxes,
            "button_run": button_run,
            "select": select,
            "mode_to_change": start_or_end,
            "new_val": new_val,
            "button_update": button_update,
        }
        
        self.update(None, None, None)
        
    def sample_data(self, *func_args, **func_kwargs):
        samples = self.sample_func(*func_args, size=self.inputs["N"].value, **func_kwargs)
        hist, edges = np.histogram(samples, density=True, bins=self.inputs["bins"].value)
        self.plots["hist"].data_source.data = {"top": hist, "left": edges[:-1], "right": edges[1:]}
    
    def update_dists(self, *func_args, **func_kwargs):
        x = np.linspace(self.plots["main"].x_range.start, self.plots["main"].x_range.end, 1000)
        self.plots["pdf"].data_source.data = {"x": x, "y": self.pdf(x, *func_args, **func_kwargs)}
        self.plots["cdf"].data_source.data = {"x": x, "y": self.cdf(x, *func_args, **func_kwargs)}
        
    def update(self, attr, old, new, force_sampling: bool = False):
        func_args = [p.value for p in self.func_args]
        func_kw = {k: v.value for (k, v) in self.func_kwargs.items()}
        
        # Sample data
        if (0 in self.inputs["sampling_checkboxes"].active
                and (force_sampling or 1 in self.inputs["sampling_checkboxes"].active)):
            self.sample_data(*func_args, **func_kw)
        
        # Redo pdf/cdf
        self.update_dists(*func_args, **func_kw)
        
    def get_layout(self):
        self.plots["main"].legend.location = "top_left"
                
        layout = column(
            Div(text=f"<h2>{self.name}</h2>"),
            row(
                column(
                    self.plots["main"], 
                    self.inputs["range"],
                ), 
                column(
                    Div(text="Parameters"),
                    *self.func_args,
                    *self.func_kwargs.values(),
                    Div(text=f"<br><em>Sampling</em>"),
                    row(
                        self.inputs["sampling_checkboxes"],
                        self.inputs["button_run"],
                        width=325,
                    ),
                    row(
                        self.inputs["N"],
                        self.inputs["bins"],
                        width=325,
                    ),
                    Div(text=f"<br><em>Adjust sliders</em>"),
                    row(
                        self.inputs["select"],
                        self.inputs["mode_to_change"],
                        self.inputs["new_val"],
                        self.inputs["button_update"],
                        width=325,
                    ),
                ),
            ),
        )
        return layout

from scipy.stats import norm, beta, gamma

normal = BokehContDist(
    norm.rvs, 
    norm.pdf, 
    norm.cdf, 
    name="Normal Distribution",
    loc=Slider(start=-10, end=10, value=0, step=.5, title="loc"),
    scale=Slider(start=0.1, end=10, value=1, step=.1, title="scale"),
)
# normal.add_param_sliders(
#     loc=Slider(start=-10, end=10, value=0, step=.5, title="loc"),
#     scale=Slider(start=0.1, end=10, value=1, step=.1, title="scale")
# )

beta = BokehContDist(
    beta.rvs, 
    beta.pdf, 
    beta.cdf, 
    Slider(start=0.1, end=10, value=3, step=.1, title="a"),
    Slider(start=0.1, end=10, value=3, step=.1, title="b"),
    x_range=(0, 1),
    name="Beta Distribution",
    loc=Slider(start=-10, end=10, value=0, step=.5, title="loc"),
    scale=Slider(start=0.1, end=10, value=1, step=.1, title="scale")
)

# layout = gridplot(
#     [
#         normal.get_layout(), 
#         beta.get_layout()
#     ],
#     ncols=2,
#     width=500,
# )
# curdoc().add_root(normal.get_layout())
curdoc().add_root(beta.get_layout())
