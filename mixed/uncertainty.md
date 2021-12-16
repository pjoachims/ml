# Uncertainty

## Aleatoric vs. epistemic uncertainty
```{tabbed} Example 1D data
![fishy](img/tikz_alea_epistemic.png)

Regression problem with regions of altering aleatoric uncertainty in the data and areas without data.
```

```{tabbed} Gaussian process for various scenarios
![fishy](img/GP_alea_epi.png)

Regressing sin(x) with a Gaussian process for different scenarios. In the lower-left, there is low noise in the data. In the lower-right, we do not observe data for a subset of the input range. The upper graphs depict the scenarios as below but with increased noise in the data.
```

### Aleatoric uncertainty

Aleatoric uncertainty is an inherent feature of the data generating process (DGP).
This type of uncertainty reflects noise in the observations, e.g., measurement errors in the data or sensor noise.
It is independent of the amount of data we collect.
For example, we cannot predict the realization of the measurement error of a thermometer.
The noise in the observations can be either *homoscedastic* or *heteroscedastic*.
Homoscedastic noise is constant for all inputs, in the sense that the variance of the noise-generating random process does not change, $\epsilon_i \sim N(0, \sigma) \text{ } \forall i$.
Heteroscedastic noise implies that the variance of the noise differs for inputs, $\epsilon_i \sim N(0, \sigma_i)$.

### Epistemic uncertainty

Epistemic uncertainty or model uncertainty refers to uncertainty in the model parameters and is a property of the model \parencite{kendallgal2017}.
To draw an analogy to a certain detective: if there are few data points in a fictitious murder case, multiple explanations (or model parameters) may fit the data obtained so far.
Observing then that the murderer is left-handed and smokes a particular type of tobacco shrinks the set of possible explanations significantly.
That is, the more data points are available, the lower the uncertainty in the model parameters.
We can explain away epistemic uncertainty with data \parencite{kendallgal2017}.

```{rubric} References
```

```{eval-rst}
.. [1] Klimm M, Warode P (2021) Parametric Computation of Minimum Cost
       Flows with Piecewise Quadratic Costs. *Mathematics of Operations
       Research*. Available at https://www3.math.tu-berlin.de/disco/research/publications/pdf/KlimmWarode2021.pdf
```

[1]: http://somewebsite.org
