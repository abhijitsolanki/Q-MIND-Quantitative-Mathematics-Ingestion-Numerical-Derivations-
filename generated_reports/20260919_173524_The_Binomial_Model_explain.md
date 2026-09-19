# 1. Executive Summary & Theoretical Intuition

The one-period binomial asset pricing model, foundational to modern quantitative finance, establishes the core mechanics of no-arbitrage pricing and contingent claim replication in a simplified discrete setting. As formalized by Tomas Björk in *Arbitrage Theory in Continuous Time* (pp. 19–20), this model strips away the complexities of continuous-time stochastic calculus while retaining the fundamental economic principles of financial market equilibrium: absence of arbitrage, portfolio replication, and risk-neutral valuation. 

In this framework, uncertainty is reduced to a single binary transition over a discrete time horizon $t \in \{0, 1\}$. By introducing two primary securities—a risk-free money market bond and a risky stock—we can construct self-financing trading portfolios that span all possible future states of nature. The central intuition is that any derivative security (or contingent claim) whose payoff is contingent upon the terminal price of the stock can be perfectly replicated by a dynamic portfolio of the underlying stock and the bond. 

Consequently, the absence of arbitrage dictates a unique price for this derivative, which must equal the cost of the replicating portfolio. This establishes the bedrock for risk-neutral pricing: asset prices today equal the expected future payoffs discounted at the risk-free rate, evaluated under a synthetic probability measure.

---

# 2. Mathematical Framework & Underlying Assumptions

We define a filtered probability space $(\Omega, \mathcal{F}, \{\mathcal{F}_t\}_{t=0}^{1}, \mathbb{P})$, where time is discrete and restricted to $t \in \{0, 1\}$. The sample space $\Omega$ consists of two distinct states of nature at $t = 1$, driven by a discrete random variable $Z$. 

The market consists of two traded assets:
1. **The Risk-Free Bond ($B_t$):** The bond price evolves deterministically. At $t=0$, the price is normalized to $B_0 = 1$. At $t=1$, the price is given by:
   $$B_1 = 1 + r$$
   where $r > -1$ represents the constant risk-free interest rate per period.

2. **The Risky Stock ($S_t$):** The initial stock price at $t=0$ is a known positive constant $S_0 = s$. At $t=1$, the stock price is driven by the realization of the random variable $Z$:
   $$S_1 = S_0 \cdot Z$$

The probability distribution of $Z$ under the objective (real-world) probability measure $\mathbb{P}$ is defined as:
$$\mathbb{P}(Z = u) = p_u, \quad \mathbb{P}(Z = d) = p_d, \quad p_u + p_d = 1$$

To ensure economic viability and preclude trivial or arbitrage-violating price paths, we impose the structural constraints:
$$0 < d < u, \quad p_u > 0, \quad p_d > 0$$
where $u$ represents the up-factor and $d$ represents the down-factor for the stock price.

---

# 3. Step-by-Step Derivation & Formula Mechanics

### Step 1: Portfolio Construction and Value Dynamics
A trading strategy (portfolio) is defined as a static vector $h = (x, y) \in \mathbb{R}^2$, where $x$ represents the number of risk-free bonds held and $y$ represents the number of shares of the risky stock held.

The initial market value of this portfolio at time $t=0$, denoted $V_0$, is obtained by summing the product of the holdings and their respective asset prices:
$$V_0 = x B_0 + y S_0$$

Substituting $B_0 = 1$ and $S_0 = s$, we obtain:
$$V_0 = x + yS_0$$

$$\begin{array}{|l|l|l|l|}
\hline
\textbf{Variable} & \textbf{Full Name / Meaning} & \textbf{Units / Domain} \\
\hline
V_0 & \text{Total portfolio market value at time } t=0 & \text{Currency (\$)} \\
x & \text{Number of holdings in the risk-free bond } B & \text{ dimensionless (shares/units)} \\
y & \text{Number of holdings in the risky stock } S & \text{ dimensionless (shares)} \\
S_0 & \text{Initial stock price at } t=0 & \text{Currency (\$) per share} \\
\hline
\end{array}$$

At time $t=1$, the value of the portfolio $V_1$ becomes a random variable dependent upon the realization of $Z$:
$$V_1 = x B_1 + y S_1$$

Substituting $B_1 = 1+r$ and $S_1 = S_0 Z$, we write the state-dependent terminal values explicitly:
* **Up State ($Z = u$):**
  $$V_1(u) = x(1+r) + y S_0 u$$
* **Down State ($Z = d$):**
  $$V_1(d) = x(1+r) + y S_0 d$$

$$\begin{array}{|l|l|l|l|}
\hline
\textbf{Variable} & \textbf{Full Name / Meaning} & \textbf{Units / Domain} \\
\hline
V_1(u), V_1(d) & \text{Portfolio value at } t=1 \text{ in the up/down state} & \text{Currency (\$)} \\
r & \text{Risk-free interest rate per period} & \text{Dimensionless (fraction)} \\
u & \text{Up-factor for stock price movement} & \text{Dimensionless, } u > 0 \\
d & \text{Down-factor for stock price movement} & \text{Dimensionless, } d > 0 \\
Z & \text{Discrete state-space random variable} & \text{Dimensionless, } Z \in \{u, d\} \\
\hline
\end{array}$$

### Step 2: Contingent Claim Pricing via Replication
Consider a European contingent claim (e.g., an option) with a payoff $X$ at $t=1$ that depends on the stock price $S_1$. In the binomial tree, $X$ takes two possible values:
$$X(u) \quad \text{if } S_1 = S_0 u$$
$$X(d) \quad \text{if } S_1 = S_0 d$$

We seek a replicating portfolio $h = (x, y)$ such that its terminal value matches the claim's payoff in all states:
$$V_1(u) = x(1+r) + y S_0 u = X(u)$$
$$V_1(d) = x(1+r) + y S_0 d = X(d)$$

This forms a linear system of two equations with two unknowns ($x$ and $y$). Subtracting the down-state equation from the up-state equation eliminates $x$:
$$y S_0 (u - d) = X(u) - X(d)$$

Solving for the optimal stock holding $y$:
$$y = \frac{X(u) - X(d)}{S_0 (u - d)}$$

$$\begin{array}{|l|l|l|l|}
\hline
\textbf{Variable} & \textbf{Full Name / Meaning} & \textbf{Units / Domain} \\
\hline
X(u), X(d) & \text{Payoff of contingent claim in up/down state} & \text{Currency (\$)} \\
y & \text{Replicating portfolio stock units (Delta)} & \text{Shares} \\
\hline
\end{array}$$

To solve for the bond holding $x$, substitute $y$ back into the down-state equation:
$$x(1+r) + \left[ \frac{X(u) - X(d)}{S_0 (u - d)} \right] S_0 d = X(d)$$

$$x(1+r) = X(d) - \frac{d}{u - d} [X(u) - X(d)]$$

$$x = \frac{1}{1+r} \left[ \frac{u X(d) - d X(u)}{u - d} \right]$$

$$\begin{array}{|l|l|l|l|}
\hline
\textbf{Variable} & \textbf{Full Name / Meaning} & \textbf{Units / Domain} \\
\hline
x & \text{Replicating portfolio bond units} & \text{Bond units} \\
\hline
\end{array}$$

### Step 3: Risk-Neutral Pricing Formula
The no-arbitrage price $\Pi(0)$ of the contingent claim at $t=0$ must equal the initial value of the replicating portfolio $V_0$:
$$\Pi(0) = V_0 = x + y S_0$$

Substitute our derived expressions for $x$ and $y$:
$$\Pi(0) = \frac{1}{1+r} \left[ \frac{u X(d) - d X(u)}{u - d} \right] + \left[ \frac{X(u) - X(d)}{u - d} \right]$$

Rearranging terms over a common denominator $(1+r)(u-d)$:
$$\Pi(0) = \frac{1}{1+r} \left[ \frac{u X(d) - d X(u) + (1+r)X(u) - (1+r)X(d)}{u - d} \right]$$

$$\Pi(0) = \frac{1}{1+r} \left[ \frac{(1+r - d)X(u) + (u - (1+r))X(d)}{u - d} \right]$$

We define the risk-neutral probabilities $q_u$ and $q_d$ as:
$$q_u = \frac{(1+r) - d}{u - d}, \quad q_d = \frac{u - (1+r)}{u - d}$$

Note that $q_u + q_d = 1$ and, under the no-arbitrage condition $d < 1+r < u$, we have $0 < q_u, q_d < 1$. Thus, the pricing equation simplifies to the risk-neutral expectation formula:
$$\Pi(0) = \frac{1}{1+r} \mathbb{E}^{\mathbb{Q}}[X] = \frac{1}{1+r} \big( q_u X(u) + q_d X(d) \big)$$

$$\begin{array}{|l|l|l|l|}
\hline
\textbf{Variable} & \textbf{Full Name / Meaning} & \textbf{Units / Domain} \\
\hline
\Pi(0) & \text{No-arbitrage derivative price at } t=0 & \text{Currency (\$)} \\
q_u, q_d & \text{Risk-neutral probabilities of up/down states} & \text{Dimensionless, } [0,1] \\
\mathbb{E}^{\mathbb{Q}}[\cdot] & \text{Expectation operator under measure } \mathbb{Q} & \text{Dimensionless} \\
\hline
\end{array}$$

---

# 4. Comprehensive Variable Dictionary

To maintain absolute mathematical clarity, the complete set of symbols, indices, parameters, and their operational meanings is detailed below:

$$\begin{array}{|l|l|l|}
\hline
\textbf{Symbol} & \textbf{Full Name / Description} & \textbf{Typical Units / Domain} \\
\hline
t & \text{Discrete time parameter} & t \in \{0, 1\} \\
\Omega & \text{Sample space of market states} & \text{Set } \{\omega_u, \omega_d\} \\
\mathcal{F} & \text{Sigma-algebra of measurable events} & \text{Power set of } \Omega \\
\mathbb{P} & \text{Objective (real-world) probability measure} & \text{Probability function, } [0, 1] \\
\mathbb{Q} & \text{Risk-neutral (martingale) probability measure} & \text{Probability function, } [0, 1] \\
B_t & \text{Price of the risk-free bond at time } t & \text{Currency (\$)} \\
S_t & \text{Price of the risky stock at time } t & \text{Currency (\$) per share} \\
s & \text{Deterministic initial stock price } S_0 & \text{Currency (\$)} \\
r & \text{Risk-free interest rate per period} & \text{Dimensionless fraction, } r > -1 \\
u & \text{Stock price up-factor} & \text{Dimensionless, } u > 0 \\
d & \text{Stock price down-factor} & \text{Dimensionless, } d > 0, d < u \\
Z & \text{Binomial state multiplier random variable} & \text{Discrete, } Z \in \{u, d\} \\
p_u, p_d & \text{Real-world probabilities for } Z = u \text{ and } Z = d & \text{Dimensionless, } p_u + p_d = 1 \\
h = (x, y) & \text{Trading strategy / portfolio vector} & \text{Vector in } \mathbb{R}^2 \\
x & \text{Number of risk-free bonds held} & \text{Real number} \\
y & \text{Number of risky stock shares held} & \text{Real number} \\
V_t & \text{Portfolio market value (wealth) at time } t & \text{Currency (\$)} \\
X & \text{Contingent claim terminal payoff at } t=1 & \text{Currency (\$)} \\
q_u, q_d & \text{Risk-neutral probabilities for up and down states} & \text{Dimensionless, } q_u + q_d = 1 \\
\Pi(0) & \text{No-arbitrage price of contingent claim at } t=0 & \text{Currency (\$)} \\
\hline
\end{array}$$

---

# 5. Worked Numerical Financial Example (Step-by-Step)

### Problem Statement
Consider a single-period financial market with the following parameters:
* Initial stock price: $S_0 = \$100$
* Risk-free interest rate: $r = 0.05$ (5% per period)
* Up-factor: $u = 1.20$
* Down-factor: $d = 0.90$
* Contingent Claim: A European call option with strike price $K = \$105$ expiring at $t=1$.

### Step 1: Compute Terminal Stock Prices
Using $S_1 = S_0 Z$:
* **Up State ($Z = u = 1.20$):**
  $$S_1(u) = 100 \times 1.20 = \$120.00$$
* **Down State ($Z = d = 0.90$):**
  $$S_1(d) = 100 \times 0.90 = \$90.00$$

### Step 2: Compute Option Payoffs $X(u)$ and $X(d)$
The payoff for a European call option is $X = \max(S_1 - K, 0)$:
* **Up State:**
  $$X(u) = \max(120 - 105, 0) = \max(15, 0) = \$15.00$$
* **Down State:**
  $$X(d) = \max(90 - 105, 0) = \max(-15, 0) = \$0.00$$

### Step 3: Compute Replicating Portfolio Holdings ($x, y$)
Calculate stock holdings $y$:
$$y = \frac{X(u) - X(d)}{S_0 (u - d)} = \frac{15 - 0}{100 (1.20 - 0.90)} = \frac{15}{100 \times 0.30} = \frac{15}{30} = 0.50$$
*Interpretation:* The investor must hold $0.50$ shares of the stock (Delta of 0.50).

Calculate bond holdings $x$:
$$x = \frac{1}{1+r} \left[ \frac{u X(d) - d X(u)}{u - d} \right] = \frac{1}{1.05} \left[ \frac{1.20(0) - 0.90(15)}{1.20 - 0.90} \right]$$
$$x = \frac{1}{1.05} \left[ \frac{-13.50}{0.30} \right] = \frac{1}{1.05} [-45.00] = -42.8571$$
*Interpretation:* The investor must borrow $\$42.86$ (holding $-42.8571$ bonds).

### Step 4: Calculate No-Arbitrage Option Price $\Pi(0)$
$$\Pi(0) = x + y S_0 = -42.8571 + (0.50 \times 100) = -42.8571 + 50.00 = \$7.1429$$

### Step 5: Verification via Risk-Neutral Pricing
Calculate risk-neutral probabilities $q_u$ and $q_d$:
$$q_u = \frac{(1+r) - d}{u - d} = \frac{1.05 - 0.90}{1.20 - 