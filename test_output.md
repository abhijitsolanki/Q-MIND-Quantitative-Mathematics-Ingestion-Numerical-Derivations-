# 1. Executive Summary & Theoretical Intuition

The derivation of the Black-Scholes partial differential equation (PDE) represents a foundational milestone in quantitative finance. First formulated by Fischer Black, Myron Scholes, and Robert Merton in 1973, the model provides a theoretical valuation framework for European-style financial options. The core economic intuition underpinning the Black-Scholes pricing framework is the concept of **dynamic hedging** and the **no-arbitrage principle**. 

By constructing a continuously rebalanced portfolio consisting of the derivative security and its underlying asset, an investor can completely eliminate the market risk associated with the price fluctuations of the underlying asset. Because the resulting portfolio is instantaneously risk-free, its return must equal the risk-free rate of return; otherwise, arbitrage opportunities would exist in the market. A remarkable consequence of this hedging argument is that the expected rate of return of the underlying asset ($\mu$) drops out of the pricing equation entirely. Consequently, options can be priced without knowing investors' risk preferences regarding the future direction of the stock.

---

# 2. Mathematical Framework & Underlying Assumptions

To formalize the model, we operate on a filtered probability space $(\Omega, \mathcal{F}, (\mathcal{F}_t)_{t \ge 0}, \mathbb{P})$, where $\mathbb{P}$ is the real-world (objective) probability measure. The financial market consists of two tradable assets: a risk-free money market account (savings account) and a risky underlying stock.

1. **Risk-Free Savings Account ($N_t$):** The price of the savings account grows deterministically at the constant risk-free rate $r$:
   $$\mathrm{d}N_t = r N_t \mathrm{d}t$$
2. **Risky Underlying Asset ($S_t$):** The stock price is assumed to follow a Geometric Brownian Motion (GBM) driven by a standard Brownian motion $W_t$ under measure $\mathbb{P}$:
   $$\mathrm{d}S_t = \mu S_t \mathrm{d}t + \sigma S_t \mathrm{d}W_t$$

---

# 3. Step-by-Step Derivation & Formula Mechanics

## Step 1: Apply Itô's Lemma to the Derivative Price
Let $V(S_t, t)$ be a European contingent claim whose value is a twice continuously differentiable function of the stock price $S_t$ and time $t$. By Itô's Lemma for time-space dependent stochastic processes, the differential $\mathrm{d}V$ is given by:

$$\mathrm{d}V = \frac{\partial V}{\partial t}\mathrm{d}t + \frac{\partial V}{\partial S}\mathrm{d}S_t + \frac{1}{2}\frac{\partial^2 V}{\partial S^2}(\mathrm{d}S_t)^2$$

Substituting the SDE for $\mathrm{d}S_t = \mu S_t \mathrm{d}t + \sigma S_t \mathrm{d}W_t$ into the expansion yields:

$$\mathrm{d}V = \frac{\partial V}{\partial t}\mathrm{d}t + \frac{\partial V}{\partial S}\left( \mu S_t \mathrm{d}t + \sigma S_t \mathrm{d}W_t \right) + \frac{1}{2}\frac{\partial^2 V}{\partial S^2}\left( \mu S_t \mathrm{d}t + \sigma S_t \mathrm{d}W_t \right)^2$$

Expanding the quadratic term and applying the standard Itô multiplication rules ($\mathrm{d}W_t^2 = \mathrm{d}t$, $\mathrm{d}W_t\mathrm{d}t = 0$, $(\mathrm{d}t)^2 = 0$):

$$(\mathrm{d}S_t)^2 = \mu^2 S_t^2 (\mathrm{d}t)^2 + 2\mu\sigma S_t^2 \mathrm{d}t\mathrm{d}W_t + \sigma^2 S_t^2 (\mathrm{d}W_t)^2 = \sigma^2 S_t^2 \mathrm{d}t$$

Substituting this back into the expansion for $\mathrm{d}V$ and collecting terms by powers of $\mathrm{d}t$ and $\mathrm{d}W_t$:

$$\mathrm{d}V = \left( \frac{\partial V}{\partial t} + \mu S_t \frac{\partial V}{\partial S} + \frac{1}{2}\sigma^2 S_t^2 \frac{\partial^2 V}{\partial S^2} \right)\mathrm{d}t + \sigma S_t \frac{\partial V}{\partial S}\mathrm{d}W_t$$

---
## Step 2: Construct the Delta-Hedged Portfolio
We construct a portfolio $\Pi_t$ consisting of a short position in one derivative contract $V(S_t, t)$ and a long position in $\Delta = \frac{\partial V}{\partial S}$ shares of the underlying stock:

$$\Pi_t = V(S_t, t) - \frac{\partial V}{\partial S} S_t$$

The change in the portfolio value over the infinitesimal time interval $\mathrm{d}t$ is:

$$\mathrm{d}\Pi_t = \mathrm{d}V - \frac{\partial V}{\partial S}\mathrm{d}S_t$$

Substitute the expansion of $\mathrm{d}V$ and $\mathrm{d}S_t$ into $\mathrm{d}\Pi_t$:

$$\mathrm{d}\Pi_t = \left[ \left( \frac{\partial V}{\partial t} + \mu S_t \frac{\partial V}{\partial S} + \frac{1}{2}\sigma^2 S_t^2 \frac{\partial^2 V}{\partial S^2} \right)\mathrm{d}t + \sigma S_t \frac{\partial V}{\partial S}\mathrm{d}W_t \right] - \frac{\partial V}{\partial S}\left( \mu S_t \mathrm{d}t + \sigma S_t \mathrm{d}W_t \right)$$

Simplifying the algebraic expression, notice that the drift terms involving $\mu S_t \frac{\partial V}{\partial S}$ and the stochastic terms involving $\sigma S_t \frac{\partial V}{\partial S}\mathrm{d}W_t$ cancel out completely:

$$\mathrm{d}\Pi_t = \left( \frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S_t^2 \frac{\partial^2 V}{\partial S^2} \right)\mathrm{d}t$$

Because all terms containing $\mathrm{d}W_t$ have vanished, the portfolio is instantaneously risk-free over the interval $\mathrm{d}t$.

---
## Step 3: Invoke No-Arbitrage and Derive the PDE
By the absence of arbitrage in frictionless markets, any risk-free portfolio must instantaneously earn the risk-free rate of return $r$. Therefore, the return on the portfolio must satisfy:

$$\mathrm{d}\Pi_t = r \Pi_t \mathrm{d}t$$

Substitute the definition of the portfolio $\Pi_t = V - \frac{\partial V}{\partial S}S_t$ and the calculated differential $\mathrm{d}\Pi_t$ into the no-arbitrage condition:

$$\left( \frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S_t^2 \frac{\partial^2 V}{\partial S^2} \right)\mathrm{d}t = r \left( V - S_t \frac{\partial V}{\partial S} \right)\mathrm{d}t$$

Dividing both sides by $\mathrm{d}t$ and rearranging all terms to one side yields the canonical Black-Scholes Partial Differential Equation:

$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + r S \frac{\partial V}{\partial S} - r V = 0$$

---

# 4. Comprehensive Variable Dictionary

| Symbol | Full Name | Physical / Financial Meaning | Typical Units |
| :--- | :--- | :--- | :--- |
| $t$ | Current Time | Elapsed time from the inception of the contract | Years ($\text{yr}$) |
| $T$ | Maturity Time | Expiration date of the derivative contract | Years ($\text{yr}$) |
| $S_t$ | Stock Price | Spot price of the underlying risky asset at time $t$ | Currency ($\text{USD}$) |
| $W_t$ | Brownian Motion | Standard Wiener process providing stochastic shocks | Dimensionless ($\sqrt{\text{yr}}$) |
| $r$ | Risk-Free Rate | Annualized constant return of the savings account | Percentage per annum ($\text{yr}^{-1}$) |
| $\mu$ | Expected Drift | Expected annualized rate of return of the stock | Percentage per annum ($\text{yr}^{-1}$) |
| $\sigma$ | Volatility | Annualized standard deviation of stock returns | Percentage per annum ($\text{yr}^{-1/2}$) |
| $V(S_t, t)$ | Option Price | Value of the European contingent claim | Currency ($\text{USD}$) |
| $\Pi_t$ | Portfolio Value | Total market value of the delta-hedged portfolio | Currency ($\text{USD}$) |
| $\Delta$ | Delta Hedge Ratio | Sensitivity of option value to underlying price (${\partial V}/{\partial S}$) | Shares ($\text{shares}$) |

---

# 5. Worked Numerical Financial Example

Consider a European Call Option with the following parameters:
* Current Stock Price ($S_0$): $\$100.00$
* Strike Price ($K$): $\$100.00$
* Risk-Free Interest Rate ($r$): $5\%$ per annum ($0.05$)
* Volatility ($\sigma$): $20\%$ per annum ($0.20$)
* Time to Maturity ($T$): $1.0$ year ($1.0$)

## Step 1: Compute Black-Scholes $d_1$ and $d_2$ Parameters
The closed-form analytical solution for a European call option $C(S, t)$ derived from the Black-Scholes PDE is given by:
$$C(S_0, t) = S_0 N(d_1) - K e^{-r(T-t)} N(d_2)$$
where $N(\cdot)$ is the cumulative distribution function of the standard normal distribution, and:
$$d_1 = \frac{\ln(S_0 / K) + \left(r + \frac{1}{2}\sigma^2\right)(T-t)}{\sigma \sqrt{T-t}}$$
$$d_2 = d_1 - \sigma \sqrt{T-t}$$

Substituting our parameters into $d_1$:
$$d_1 = \frac{\ln(100 / 100) + \left(0.05 + \frac{1}{2}(0.20)^2\right)(1.0)}{0.20 \sqrt{1.0}}$$
$$d_1 = \frac{0 + (0.05 + 0.02)(1.0)}{0.20} = \frac{0.07}{0.20} = 0.35$$

Now, compute $d_2$:
$$d_2 = 0.35 - 0.20 \sqrt{1.0} = 0.35 - 0.20 = 0.15$$

## Step 2: Evaluate Normal Cumulative Distribution Functions
Using standard normal distribution tables:
$$N(0.35) \approx 0.63683$$
$$N(0.15) \approx 0.55962$$

## Step 3: Calculate Option Price
$$C(100, 0) = 100 \times 0.63683 - 100 \times e^{-0.05(1.0)} \times 0.55962$$
$$e^{-0.05} \approx 0.951229$$
$$C(100, 0) = 63.683 - (100 \times 0.951229 \times 0.55962)$$
$$C(100, 0) = 63.683 - 53.232 = 10.451$$
**Economic Interpretation:** The fair theoretical price of this European call option is **$\$10.45$**.

---

# 6. Real-World Applications in Quantitative Finance & Risk Management

The Black-Scholes PDE and its analytical solutions serve as foundational tools throughout quantitative finance:
* **Derivative Pricing & Market Making:** Options desks use extensions of the Black-Scholes framework to quote bid-ask spreads and calculate theoretical prices for vanilla and exotic options.
* **Delta Hedging & Risk Management:** Financial institutions maintain delta-neutral portfolios to protect against directional price movements. The hedge ratio $\Delta = \frac{\partial V}{\partial S}$ dictates the exact number of shares required to neutralize risk.
* **Implied Volatility Surfaces:** By inverting the Black-Scholes formula, traders calculate "implied volatility" from market option prices, mapping volatility smiles and skews essential for cross-sectional risk management.
* **Credit Risk & Structural Models:** The Merton model (a direct application of Black-Scholes methodology) views a firm's equity as a call option on its total asset value, allowing risk managers to compute corporate default probabilities.

---

# 7. Source Textbook Citations

1. **Paul Wilmott on Quantitative Finance**, Chapter 5, Page 112: *Foundations of derivatives theory, delta hedging mechanics, and the no-arbitrage framework.*
2. **Mathematical Finance** by Achim K. Fries, Section 7.3.1, Page 99: *Specification of stock price SDEs under Geometric Brownian Motion and money market dynamics.*
3. **Basics of Financial Mathematics**, Section 22, Page 91: *Application of multivariate Itô's formula to contingent claim portfolios $V_t = f(S_t, t)$.*