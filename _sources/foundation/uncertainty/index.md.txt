# Uncertainty

```{admonition} Why should we care?
Some content
```

## Aleatoric vs. epistemic uncertainty

### Aleatoric uncertainty

```{margin}
Aleatoric uncertainty = inherent **noise** in the data
```
Aleatoric uncertainty is an **inherent feature of the data** generating process (DGP).
This type of uncertainty reflects noise in the observations, e.g., measurement errors in the data or sensor noise.
It is independent of the amount of data we collect.
For example, we cannot predict the realization of the measurement error of a thermometer.

The noise in the observations can be either *homoscedastic* or *heteroscedastic*.
Homoscedastic noise is constant for all inputs, in the sense that the variance of the noise-generating random process does not change.
Heteroscedastic noise implies that the variance of the noise differs for inputs.

### Epistemic uncertainty
Epistemic uncertainty or model uncertainty refers to **uncertainty in the model parameters** and is a property of the model [KG17]. I.e., multiple model parameters may "explain" the data obtained so far. Observing further data, then shrinks the set of possible explanations/parameters significantly.
That is, the more data points are available, the lower the uncertainty in the model parameters.
We can *explain away* epistemic uncertainty with data [KG17].

### Example
```{tabbed} Example 1D data
![fishy](img/tikz_alea_epistemic.png)

Regression problem with regions of altering aleatoric uncertainty in the data and areas without data.
```

```{tabbed} GP for various scenarios
![fishy](img/GP_alea_epi.png)

Regressing $f(x) = sin(x)$ with a Gaussian process for different scenarios. In the lower-left, there is low noise in the data. In the lower-right, we do not observe data for a subset of the input range. The upper graphs depict the scenarios as below but with increased noise in the data.
```

```{rubric} References
```
    
[KG17]: Kendall, Alex, and Yarin Gal. "What uncertainties do we need in Bayesian deep learning for computer vision?" *arXiv preprint arXiv:170304977* (2017).
