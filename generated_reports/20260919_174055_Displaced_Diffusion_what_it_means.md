# 1. Executive Summary & Theoretical Intuition

The **Displaced Diffusion** model, originally introduced by Mark Rubinstein (1983) in the context of option pricing and binomial trees, is a continuous-time stochastic volatility model designed to capture empirical deviations from the classic geometric Brownian motion assumed by the Black-Scholes-Merton (BSM) framework. 

Under the standard BSM model, asset returns are assumed to be normally distributed with constant percentage volatility ($\sigma$), leading to a flat implied volatility smile across strikes. In reality, equity markets exhibit a pronounced "volatility smirk" or "skew"—where out-of-the-money puts trade at significantly higher implied volatilities than out-of-the-money calls. Conversely, fixed-income and foreign exchange markets often encounter environments where rates or spreads can drop below zero, a domain where standard log-normal models fail because they cannot accommodate non-positive asset prices.

The displaced diffusion model solves these structural limitations by introducing a positive constant shift parameter, $d > 0$, to the underlying asset price. By defining the shifted process as $\tilde{S}_t = S_t + d$, the model interpolates between a purely additive normal model (when the displacement is large relative to the spot) and a standard log-normal model (when $d \to 0$). This parameterization allows quantitative analysts to flexibly fit the volatility skew, generate realistic probability density functions with heavy left tails, and ensure mathematical tractability under negative interest rate regimes without resorting to fully intractable non-linear local volatility surfaces.

---

# 2. Mathematical Framework & Underlying Assumptions

To formalize the displaced diffusion process, we establish the underlying probability space $(\Omega, \mathcal{F}, \{\mathcal{F}_t\}_{t \ge 0}, \mathbb{Q})$, where $\mathbb{Q}$ is the risk-neutral pricing measure. Under $\mathbb{Q}$, discounted asset prices are martingales (Björk, *Arbitrage Theory in Continuous Time*, p. 129).

### Standard BSM Dynamics (Reference)
In the standard Black-Scholes model, the spot price $S_t$ follows a geometric Brownian motion:
$$dS_t = r S_t dt + \sigma S_t dW_t$$

### Displaced Diffusion SDE
The displaced diffusion model modifies the diffusion (volatility) coefficient by shifting the asset price argument. The risk-neutral stochastic differential equation (SDE) governing the spot price $S_t$ is defined as:
$$dS_t = r S_t dt + \sigma (S_t + d) dW_t$$

### Underlying Assumptions
1. **Constant Interest Rates:** The risk-free rate $r$ is deterministic and constant over the life of the option (Fabozzi et al., *The Mathematics of Financial Modelling*, p. 284).
2. **Shift Parameter:** The displacement parameter $d > 0$ is a strictly positive constant known a priori.
3. **Brownian Motion:** $W_t$ is a standard 1-dimensional Brownian motion under the risk-neutral measure $\mathbb{Q}$ (Gregoriou & Pascalau, *Financial Econometrics Modeling*, p. 188).
4. **Modified Volatility:** The parameter $\sigma > 0$ represents the volatility coefficient of the displaced process.

---

# 3. Step-by-Step Derivation & Formula Mechanics

### Step 1: Definition of the Shifted Process
We define a new state variable, the displaced asset price $\tilde{S}_t$, via the linear transformation:
$$\tilde{S}_t = S_t + d$$

### Step 2: Deriving the SDE for the Shifted Process
To find the differential $d\tilde{S}_t$, we apply the differential operator to our transformation. Since $d$ is a deterministic constant, its differential $dd = 0$. 
$$d\tilde{S}_t = d(S_t + d) = dS_t$$

Substituting the displaced diffusion SDE for $dS_t$:
$$d\tilde{S}_t = r S_t dt + \sigma (S_t + d) dW_t$$

We now express $S_t$ in terms of $\tilde{S}_t$ by inverting our transformation ($S_t = \tilde{S}_t - d$):
$$d\tilde{S}_t = r (\tilde{S}_t - d) dt + \sigma \tilde{S}_t dW_t$$

Expanding this expression yields:
$$d\tilde{S}_t = \left( r \tilde{S}_t - rd \right) dt + \sigma \tilde{S}_t dW_t$$

This formulation demonstrates that $\tilde{S}_t$ no longer follows a pure geometric Brownian motion due to the deterministic drift adjustment $-rd \, dt$. However, the stochastic term $\sigma \tilde{S}_t dW_t$ scales directly with $\tilde{S}_t$, allowing us to leverage log-normal pricing techniques.

### Step 3: Deriving the European Call Option Pricing Formula
Consider a European call option with strike price $K$ and maturity $T$. The payoff at maturity $T$ is given by $\max(S_T - K, 0)$. 

We can rewrite the payoff in terms of the displaced variables by adding and subtracting $d$:
$$\max(S_T - K, 0) = \max\left((S_T + d) - (K + d), 0\right) = \max\left(\tilde{S}_T - \tilde{K}, 0\right)$$
where $\tilde{K} = K + d$ represents the adjusted strike price.

Under the risk-neutral pricing framework, the price of the European call option at time $t=0$, denoted as $C(0, S_0)$, is the expected discounted payoff under measure $\mathbb{Q}$:
$$C(0, S_0) = e^{-rT} \mathbb{E}^{\mathbb{Q}} \left[ \max(\tilde{S}_T - \tilde{K}, 0) \right]$$

Because the process $\tilde{S}_t$ satisfies a log-normal diffusion (with a shifted drift), its terminal distribution $\tilde{S}_T$ conditional on $\tilde{S}_0 = S_0 + d$ is log-normal. Consequently, the expectation can be evaluated analytically using the Black-Scholes pricing formula structure, substituting the initial spot $S_0$ with $\tilde{S}_0 = S_0 + d$ and the strike $K$ with $\tilde{K} = K + d$:

$$C(0, S_0) = \tilde{S}_0 \Phi(d_1) - e^{-rT} \tilde{K} \Phi(d_2)$$

where the auxiliary parameters $d_1$ and $d_2$ are defined as:
$$d_1 = \frac{\ln\left(\frac{\tilde{S}_0}{\tilde{K}}\right) + \left(r + \frac{1}{2}\sigma^2\right)T}{\sigma \sqrt{T}} = \frac{\ln\left(\frac{S_0 + d}{K + d}\right) + \left(r + \frac{1}{2}\sigma^2\right)T}{\sigma \sqrt{T}}$$

$$d_2 = d_1 - \sigma \sqrt{T}$$

---

# 4. Comprehensive Variable Dictionary (All Symbols & Full Names)

| Symbol | Full Name / Description | Physical / Financial Meaning | Typical Units / Domain |
| :--- | :--- | :--- | :--- |
| $t$ | Current Time | Elapsed time from the inception of the contract | Years ($0 \le t \le T$) |
| $T$ | Maturity Time | Expiration time of the derivative contract | Years ($T > 0$) |
| $S_t$ | Spot Price | Market price of the underlying asset at time $t$ | Currency units ($S_t > -d$) |
| $\tilde{S}_t$ | Displaced Asset Price | Shifted underlying asset process ($\tilde{S}_t = S_t + d$) | Currency units ($\tilde{S}_t > 0$) |
| $d$ | Displacement Parameter | Constant positive shift applied to the underlying asset | Currency units ($d > 0$) |
| $r$ | Risk-Free Rate | Continuously compounded risk-free interest rate | Dimensionless fraction per annum ($r \in \mathbb{R}$) |
| $\sigma$ | Volatility Parameter | Volatility coefficient of the displaced diffusion process | Dimensionless fraction per annum ($\sigma > 0$) |
| $W_t$ | Standard Brownian Motion | Wiener process driving stochastic shocks under measure $\mathbb{Q}$ | $\sqrt{\text{Years}}$ |
| $\mathbb{Q}$ | Risk-Neutral Measure | Martingale pricing measure equivalent to the objective measure | Probability measure |
| $F(t, S_t)$ | Derivative Price | Value of a contingent claim at time $t$ | Currency units |
| $K$ | Strike Price | Exercise price of the European option contract | Currency units ($K > 0$) |
| $\tilde{K}$ | Adjusted Strike Price | Displaced strike price ($\tilde{K} = K + d$) | Currency units ($\tilde{K} > 0$) |
| $\Phi(\cdot)$ | Cumulative Normal Distribution | Integral of the standard normal probability density function | Probability ($[0, 1]$) |
| $d_1, d_2$ | Black-Scholes Auxiliary Variables | Intermediate standardized moneyness parameters | Dimensionless |

---

# 5. Worked Numerical Financial Example (Step-by-Step)

### Problem Setup
Consider a European call option on an equity index with the following parameters:
*   Current spot price ($S_0$): $\$100.00$
*   Strike price ($K$): $\$100.00$ (At-the-money)
*   Displacement parameter ($d$): $\$20.00$
*   Risk-free interest rate ($r$): $5\%$ per annum ($0.05$)
*   Volatility parameter ($\sigma$): $20\%$ per annum ($0.20$)
*   Time to maturity ($T$): $1.0$ year

### Step 1: Calculate Displaced Initial Spot and Strike
$$\tilde{S}_0 = S_0 + d = 100.00 + 20.00 = 120.00$$
$$\tilde{K} = K + d = 100.00 + 20.00 = 120.00$$

### Step 2: Compute Auxiliary Parameters $d_1$ and $d_2$
First, calculate the log-moneyness ratio:
$$\frac{\tilde{S}_0}{\tilde{K}} = \frac{120.00}{120.00} = 1.00 \implies \ln(1.00) = 0.00$$

Next, calculate the numerator for $d_1$:
$$\text{Numerator} = 0.00 + \left(0.05 + \frac{1}{2}(0.20)^2\right)(1.0) = 0.05 + \frac{1}{2}(0.04)(1.0) = 0.05 + 0.02 = 0.07$$

Calculate the denominator for $d_1$:
$$\text{Denominator} = \sigma \sqrt{T} = 0.20 \times \sqrt{1.0} = 0.20$$

Compute $d_1$:
$$d_1 = \frac{0.07}{0.20} = 0.35$$

Compute $d_2$:
$$d_2 = d_1 - \sigma \sqrt{T} = 0.35 - 0.20 = 0.15$$

### Step 3: Evaluate Cumulative Normal Distribution Values
Using standard normal distribution tables:
$$\Phi(d_1) = \Phi(0.35) \approx 0.63683$$
$$\Phi(d_2) = \Phi(0.15) \approx 0.55962$$

### Step 4: Calculate the Option Price
Apply the modified Black-Scholes pricing formula:
$$C(0, S_0) = \tilde{S}_0 \Phi(d_1) - e^{-rT} \tilde{K} \Phi(d_2)$$

Substitute the numerical values:
$$C(0, S_0) = (120.00)(0.63683) - e^{-0.05(1.0)}(120.00)(0.55962)$$

Calculate the discount factor $e^{-0.05} \approx 0.951229$:
$$C(0, S_0) = 76.4196 - (0.951229)(120.00)(0.55962)$$
$$C(0, S_0) = 76.4196 - (0.951229)(67.1544) = 76.4196 - 63.8828 = 12.5368$$

### Economic Interpretation
The displaced call option price is approximately **$\$12.54$**. Because the displacement parameter $d = 20$ raises the effective reference point of the asset ($\tilde{S}_0 = 120$), the percentage volatility applied to the asset dynamics is damped relative to the absolute price level, impacting the terminal probability distribution and generating a lower option value compared to a standard log-nosed model with equivalent volatility on the raw spot.

---

# 6. Real-World Applications in Quantitative Finance & Risk Management

1. **Negative Interest Rate Modeling:** Following the adoption of negative monetary policy rates by central banks (e.g., European Central Bank, Bank of Japan) in the 2010s, standard log-normal Black models for caps, floors, and swaptions broke down because they assigned zero probability to negative rates. Displaced diffusion models (often termed shifted Black models in fixed-income markets) became an industry standard for pricing interest rate derivatives, accommodating negative rates by setting $d > 0$ such that $S_t + d > 0$ remains strictly valid.
2. **Volatility Smile Calibration:** In equity derivatives and foreign exchange markets, options on assets with downside skew require volatility models that increase implied volatility for low strikes. Displaced diffusion structurally increases the leverage effect for out-of-the-money puts, providing a parsimonious fit to market smiles without requiring full local volatility or stochastic volatility calibrations (such as Heston).
3. **Risk Management and Stress Testing:** Quantitative risk systems use displaced diffusion SDEs to simulate asset paths under stress scenarios where asset prices or spreads approach zero or negative domains, preventing numerical failures associated with logarithmic singularities.

---

# 7. Source Textbook Citations

*   **Björk, Thomas.** *Arbitrage Theory in Continuous Time*. Oxford University Press. (Specifically referencing foundational risk-neutral pricing frameworks, martingale measures, and Feynman-Kac PDE derivations, p. 129).
*   **Fabozzi, Frank J., et al.** *The Mathematics of Financial Modelling and Investment Management*. John Wiley & Sons. (Specifically referencing continuous-time diffusion processes and partial differential equations, p. 284).
*   **Gregoriou, Greg N., and Gabriela Pascalau.** *Financial Econometrics Modeling: Derivatives Pricing, Hedge Funds and Term Structure Models*. Palgrave Macmillan. (Specifically referencing stochastic differential equations and Brownian motion dynamics, p. 188).
*   **Rubinstein, Mark.** "Alternative Paths to Binomial Pricing." *Financial Analysts Journal*, Vol. 39, No. 4, 1983, pp. 33-49. (Original conceptualization of the displaced diffusion methodology).