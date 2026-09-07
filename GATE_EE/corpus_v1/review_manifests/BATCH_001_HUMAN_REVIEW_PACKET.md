# GATE EE Batch 001 — Human Final QA Packet

Canonical source SHA-256: `cf815b061af0d357df02796f34021b69c3e2465835a1ab1caab7d1ae16d61256`
Strict Formatter report SHA-256: `ea12ea1c9806ca46600b474f67981e8092d3239eef7d93ce790798102cbd8c39`
Strict result: **20 PASS / 0 REVIEW / 0 invalid**
Independent AI recomputation: **20/20 PASS (not a human-review substitute)**
Paper eligible: **0 — promotion remains blocked pending named human signoff**

## Reviewer identity and attestation

- Name: ______________________________
- Role or qualification: ______________________________
- Review date (YYYY-MM-DD): ______________________________
- Required attestation: “I independently reviewed the Batch 001 questions, answers and solutions and approve only the question IDs marked PASS below.”

For every question, independently check the mathematics, declared answer, complete solution, clarity, and originality-conflict risk. Do not copy the AI result as the human decision.

---

## TMB-GATE-EE-EM-001 — revision 2

**Route:** Engineering Mathematics → Linear Algebra → Eigenvalues
**Type / marks / difficulty:** MCQ / 1 / Easy

### Question

Determine the largest eigenvalue of the matrix $A=\begin{bmatrix}2&1\\1&2\end{bmatrix}$.

### Options

- A. 1
- B. 2
- C. 3
- D. 4

### Declared answer

C

### Independent recomputation evidence

det(A−λI)=(2−λ)²−1=(λ−1)(λ−3); the largest eigenvalue is 3, which is option C.

### Canonical solution

The characteristic equation is $\det(A-\lambda I)=0$, so $(2-\lambda)^2-1=0$, or $\lambda^2-4\lambda+3=0$. Thus the eigenvalues are $1$ and $3$, and the largest is $3$.
Final answer: C

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☑ | Matrix is exposed as raw LaTeX in the mobile review packet and is not rendered for human review.
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☑ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-002 — revision 2

**Route:** Engineering Mathematics → Linear Algebra → Matrix inverse
**Type / marks / difficulty:** NAT / 2 / Medium

### Question

For the matrix $A=\begin{bmatrix}1&2\\3&5\end{bmatrix}$, calculate $\operatorname{tr}(A^{-1})$. Enter the numerical value.

### Declared answer

-6

### Independent recomputation evidence

det(A)=−1 and A⁻¹=[−5  2; 3  −1], so tr(A⁻¹)=−6.

### Canonical solution

Here $\det A=1\cdot5-2\cdot3=-1$. Therefore $A^{-1}=\frac{1}{-1}\begin{bmatrix}5&-2\\-3&1\end{bmatrix}=\begin{bmatrix}-5&2\\3&-1\end{bmatrix}$. Thus $\operatorname{tr}(A^{-1})=-5-1=-6$.
Final answer: -6

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-003 — revision 2

**Route:** Engineering Mathematics → Linear Algebra → Idempotent matrices
**Type / marks / difficulty:** MSQ / 2 / Hard

### Question

Let $P$ be a real symmetric idempotent matrix, i.e. $P^T=P$ and $P^2=P$. Which of the following statements are necessarily true?

### Options

- A. Every eigenvalue of $P$ is either $0$ or $1$.
- B. $P$ is positive semidefinite.
- C. $\operatorname{tr}(P)=\operatorname{rank}(P)$.
- D. $\det(P)=1$.

### Declared answer

A, B, C

### Independent recomputation evidence

P²=P implies λ²=λ, hence λ∈{0,1}; symmetry gives orthogonal diagonalization and positive semidefiniteness; trace equals rank. A, B and C follow, while D need not.

### Canonical solution

If $Pv=\lambda v$, then $P^2v=\lambda^2v$, but $P^2=P$, so $\lambda^2=\lambda$ and $\lambda\in\{0,1\}$. Since $P$ is symmetric, it is orthogonally diagonalizable with nonnegative eigenvalues, hence positive semidefinite. The trace is the sum of eigenvalues and therefore equals the number of unit eigenvalues, which is the rank. The determinant need not be $1$; it is $0$ whenever $P$ has a zero eigenvalue.
Final answer: A, B, C

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-004 — revision 2

**Route:** Engineering Mathematics → Calculus → Limits
**Type / marks / difficulty:** MCQ / 1 / Easy

### Question

Evaluate the exponential limit $\displaystyle\lim_{x\to0}\frac{e^{2x}-1-2x}{x^2}$.

### Options

- A. 1
- B. 2
- C. 4
- D. Does not exist

### Declared answer

B

### Independent recomputation evidence

e²ˣ=1+2x+2x²+O(x³); division by x² gives the limit 2, option B.

### Canonical solution

Using $e^{2x}=1+2x+\frac{(2x)^2}{2}+O(x^3)=1+2x+2x^2+O(x^3)$, the numerator is $2x^2+O(x^3)$. Dividing by $x^2$ and taking the limit gives $2$.
Final answer: B

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-005 — revision 3

**Route:** Engineering Mathematics → Calculus → Optimization
**Type / marks / difficulty:** NAT / 2 / Medium

### Question

Using the derivative of $f(x)=x^3-3x^2+2$, determine its absolute minimum value on the interval $0\le x\le3$. The minimum value is ______.

### Declared answer

-2

### Independent recomputation evidence

f′(x)=3x(x−2); checking x=0,2,3 gives 2,−2,2, so the absolute minimum is −2.

### Canonical solution

$f'(x)=3x(x-2)$, so the interior critical point is $x=2$. Evaluate the candidates: $f(0)=2$, $f(2)=8-12+2=-2$, and $f(3)=27-27+2=2$. Hence the minimum value is $-2$.
Final answer: -2

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-006 — revision 2

**Route:** Engineering Mathematics → Calculus → Integration
**Type / marks / difficulty:** MCQ / 2 / Medium

### Question

Evaluate $\displaystyle\int_0^1\frac{x}{1+x^2}\,dx$.

### Options

- A. $\ln 2$
- B. $\frac{1}{2}\ln 2$
- C. $\frac{1}{4}\ln 2$
- D. $1-\ln2$

### Declared answer

B

### Independent recomputation evidence

With u=1+x², the integral becomes (1/2)∫₁² du/u=(1/2)ln 2, option B.

### Canonical solution

Put $u=1+x^2$, so $du=2x\,dx$. Then $\int_0^1\frac{x}{1+x^2}dx=\frac12\int_1^2\frac{du}{u}=\frac12\ln2$.
Final answer: B

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-007 — revision 2

**Route:** Engineering Mathematics → Differential Equations → First-order linear ODE
**Type / marks / difficulty:** NAT / 2 / Medium

### Question

Solve the initial-value problem $y'+2y=4$, $y(0)=1$, and determine $y(\ln 2)$. Enter the numerical value.

### Declared answer

1.75

### Independent recomputation evidence

The IVP gives y=2−e⁻²ˣ; at x=ln 2, y=2−1/4=7/4=1.75.

### Canonical solution

The solution is $y=2+Ce^{-2x}$. From $y(0)=1$, $C=-1$, hence $y=2-e^{-2x}$. At $x=\ln2$, $e^{-2\ln2}=1/4$, so $y=2-1/4=7/4=1.75$.
Final answer: 1.75

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-008 — revision 2

**Route:** Engineering Mathematics → Differential Equations → Second-order linear ODE
**Type / marks / difficulty:** MSQ / 2 / Medium

### Question

Consider the second-order linear ordinary differential equation $y''+4y'+3y=0$. Which of the following functions are solutions?

### Options

- A. $e^{-x}$
- B. $e^{-3x}$
- C. $e^{-2x}$
- D. $2e^{-x}-5e^{-3x}$

### Declared answer

A, B, D

### Independent recomputation evidence

The characteristic roots are −1 and −3; e⁻ˣ, e⁻³ˣ and every linear combination of them solve the ODE. Thus A, B and D.

### Canonical solution

The characteristic equation is $r^2+4r+3=(r+1)(r+3)=0$, giving roots $-1$ and $-3$. Hence every solution has the form $C_1e^{-x}+C_2e^{-3x}$. Therefore A, B and D are solutions, while $e^{-2x}$ is not.
Final answer: A, B, D

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-009 — revision 2

**Route:** Engineering Mathematics → Complex Variables → Complex algebra
**Type / marks / difficulty:** MCQ / 1 / Easy

### Question

Evaluate $(1+i)^4$.

### Options

- A. $4$
- B. $-4$
- C. $4i$
- D. $-4i$

### Declared answer

B

### Independent recomputation evidence

(1+i)²=2i and (2i)²=−4, option B.

### Canonical solution

$(1+i)^2=1+2i+i^2=2i$. Therefore $(1+i)^4=(2i)^2=-4$.
Final answer: B

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-010 — revision 2

**Route:** Engineering Mathematics → Complex Variables → Quadratic roots
**Type / marks / difficulty:** NAT / 2 / Medium

### Question

If $z_1$ and $z_2$ are the complex roots of $z^2-2z+5=0$, determine $|z_1-z_2|$. Enter the numerical value.

### Declared answer

4

### Independent recomputation evidence

The roots are 1±2i, whose separation has modulus |4i|=4.

### Canonical solution

The roots are $z=\frac{2\pm\sqrt{4-20}}{2}=1\pm2i$. Thus $z_1-z_2=4i$ up to sign, and therefore $|z_1-z_2|=4$.
Final answer: 4

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-011 — revision 2

**Route:** Engineering Mathematics → Probability and Statistics → Probability axioms
**Type / marks / difficulty:** MCQ / 1 / Easy

### Question

Events $A$ and $B$ are independent with $P(A)=0.6$ and $P(B)=0.5$. Calculate $P(A\cup B)$.

### Options

- A. 0.30
- B. 0.50
- C. 0.80
- D. 1.10

### Declared answer

C

### Independent recomputation evidence

Independence gives P(A∩B)=0.3; inclusion–exclusion gives 0.6+0.5−0.3=0.8, option C.

### Canonical solution

Independence gives $P(A\cap B)=0.6\times0.5=0.3$. Therefore $P(A\cup B)=P(A)+P(B)-P(A\cap B)=0.6+0.5-0.3=0.8$.
Final answer: C

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-012 — revision 2

**Route:** Engineering Mathematics → Probability and Statistics → Discrete random variables
**Type / marks / difficulty:** NAT / 2 / Medium

### Question

A random variable $X$ takes values $0,1,2$ with probabilities $0.2,0.5,0.3$, respectively. Calculate $E[X^2]$.

### Declared answer

1.7

### Independent recomputation evidence

E[X²]=0²(0.2)+1²(0.5)+2²(0.3)=1.7.

### Canonical solution

$E[X^2]=0^2(0.2)+1^2(0.5)+2^2(0.3)=0+0.5+1.2=1.7$.
Final answer: 1.7

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-013 — revision 2

**Route:** Engineering Mathematics → Probability and Statistics → Expectation and variance
**Type / marks / difficulty:** MSQ / 2 / Medium

### Question

Let a random variable $X$ have finite mean $\mu$ and variance $\sigma^2$. Which statements are necessarily true?

### Options

- A. $E[X-\mu]=0$
- B. $E[X^2]=\sigma^2+\mu^2$
- C. $\operatorname{Var}(aX+b)=a^2\sigma^2$ for constants $a,b$
- D. $E[(X-\mu)^2]=\sigma^2$

### Declared answer

A, B, C, D

### Independent recomputation evidence

Linearity of expectation and the definitions of variance verify all four identities; A, B, C and D.

### Canonical solution

By definition $\mu=E[X]$, so $E[X-\mu]=0$. Also $\sigma^2=E[X^2]-\mu^2$, giving $E[X^2]=\sigma^2+\mu^2$. Adding a constant does not change variance and scaling by $a$ scales variance by $a^2$. Finally, variance is defined as $E[(X-\mu)^2]$. Hence all four statements are true.
Final answer: A, B, C, D

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-014 — revision 3

**Route:** Engineering Mathematics → Calculus → Fourier series
**Type / marks / difficulty:** NAT / 2 / Medium

### Question

A $2\pi$-periodic function is defined over one period by $f(x)=0$ for $-\pi<x<0$ and $f(x)=\sin x$ for $0<x<\pi$. If $f(x)=a_0/2+\sum_{n=1}^{\infty}(a_n\cos nx+b_n\sin nx)$, calculate $b_1$.

### Declared answer

0.5

### Independent recomputation evidence

b₁=(1/π)∫₀^π sin²x dx=(1/π)(π/2)=0.5.

### Canonical solution

By the Fourier coefficient formula, $b_1=\frac{1}{\pi}\int_{-\pi}^{\pi}f(x)\sin x\,dx=\frac{1}{\pi}\int_0^{\pi}\sin^2x\,dx$. Since $\int_0^{\pi}\sin^2x\,dx=\pi/2$, we obtain $b_1=1/2=0.5$.
Final answer: 0.5

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-015 — revision 3

**Route:** Engineering Mathematics → Complex Variables → Residue theorem
**Type / marks / difficulty:** MCQ / 2 / Hard

### Question

Let $C$ be the positively oriented contour $|z|=2$. Evaluate $\displaystyle\oint_C\frac{z^2+1}{z(z-1)}\,dz$.

### Options

- A. $0$
- B. $2\pi i$
- C. $4\pi i$
- D. $-2\pi i$

### Declared answer

B

### Independent recomputation evidence

The residues at 0 and 1 are −1 and 2; their sum is 1, so the contour integral is 2πi, option B.

### Canonical solution

The poles $z=0$ and $z=1$ both lie inside $C$. Their residues are $\operatorname{Res}(f,0)=-1$ and $\operatorname{Res}(f,1)=2$, so their sum is $1$. By the residue theorem, the contour integral is $2\pi i$.
Final answer: B

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-016 — revision 3

**Route:** Engineering Mathematics → Linear Algebra → Linear systems
**Type / marks / difficulty:** NAT / 2 / Medium

### Question

Consider the linear system whose coefficient matrix has proportional rows: $x+y=2$ and $2x+2y=k$. Determine the value of $k$ for which the system has infinitely many solutions.

### Declared answer

4

### Independent recomputation evidence

The second equation must be twice the first; twice the right-hand side 2 is 4, so k=4.

### Canonical solution

For infinitely many solutions, the second equation must be exactly twice the first. Twice $x+y=2$ gives $2x+2y=4$. Hence $k=4$.
Final answer: 4

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-017 — revision 2

**Route:** Engineering Mathematics → Calculus → Multivariable calculus
**Type / marks / difficulty:** MCQ / 2 / Hard

### Question

For $f(x,y)=x^2y+y^2$, calculate the directional derivative at $(1,2)$ in the direction $3\mathbf{i}+4\mathbf{j}$.

### Options

- A. $5$
- B. $\frac{32}{5}$
- C. $8$
- D. $\frac{41}{5}$

### Declared answer

B

### Independent recomputation evidence

∇f(1,2)=(4,5) and the unit direction is (3/5,4/5); their dot product is 32/5, option B.

### Canonical solution

$\nabla f=(2xy,x^2+2y)$. At $(1,2)$, $\nabla f=(4,5)$. The unit vector in the direction $(3,4)$ is $(3/5,4/5)$. Hence the directional derivative is $(4,5)\cdot(3/5,4/5)=12/5+20/5=32/5$.
Final answer: B

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-018 — revision 2

**Route:** Engineering Mathematics → Calculus → Vector calculus
**Type / marks / difficulty:** MSQ / 2 / Hard

### Question

For the planar vector field $\mathbf{F}=y\mathbf{i}-x\mathbf{j}$, which statements are true?

### Options

- A. $\nabla\cdot\mathbf{F}=0$
- B. $\nabla\times\mathbf{F}=-2\mathbf{k}$
- C. $\mathbf{F}$ is conservative on $\mathbb{R}^2$
- D. The counter-clockwise circulation along $x^2+y^2=1$ is $-2\pi$.

### Declared answer

A, B, D

### Independent recomputation evidence

The divergence is 0, the planar curl is −2, and Green’s theorem gives circulation −2 times the unit-disk area, or −2π. Thus A, B and D.

### Canonical solution

With $P=y$ and $Q=-x$, divergence is $\partial P/\partial x+\partial Q/\partial y=0+0=0$. The scalar curl is $\partial Q/\partial x-\partial P/\partial y=-1-1=-2$, i.e. $-2\mathbf{k}$. Since the curl is nonzero, the field is not conservative. Green's theorem gives the counter-clockwise circulation as $\iint_D(-2)\,dA=-2\pi$ for the unit disk.
Final answer: A, B, D

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-019 — revision 2

**Route:** Engineering Mathematics → Probability and Statistics → Bernoulli distribution
**Type / marks / difficulty:** NAT / 2 / Easy

### Question

If $X$ is a Bernoulli random variable with $P(X=1)=0.4$, calculate $\operatorname{Var}(X)$.

### Declared answer

0.24

### Independent recomputation evidence

For Bernoulli p=0.4, Var(X)=p(1−p)=0.4(0.6)=0.24.

### Canonical solution

For a Bernoulli random variable with parameter $p$, $\operatorname{Var}(X)=p(1-p)$. Thus the variance is $0.4\times0.6=0.24$.
Final answer: 0.24

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## TMB-GATE-EE-EM-020 — revision 3

**Route:** Engineering Mathematics → Differential Equations → Partial differential equations
**Type / marks / difficulty:** NAT / 2 / Hard

### Question

The function $u(x,t)$ satisfies the heat equation, a partial differential equation given by $\partial u/\partial t=\partial^2u/\partial x^2$, for $0<x<\pi$, with $u(0,t)=u(\pi,t)=0$ and $u(x,0)=3\sin 2x$. Determine $u(\pi/4,(\ln 2)/4)$.

### Declared answer

1.5

### Independent recomputation evidence

The single heat mode is u=3e⁻⁴ᵗ sin(2x); substitution gives 3(1/2)(1)=1.5.

### Canonical solution

The initial condition is a single eigenmode, so $u(x,t)=3e^{-4t}\sin 2x$. At $x=\pi/4$, $\sin(2x)=1$. At $t=(\ln2)/4$, $e^{-4t}=e^{-\ln2}=1/2$. Hence $u=3/2=1.5$.
Final answer: 1.5

### Human decision fields

| Check | PASS | FAIL | Notes |
|---|:---:|:---:|---|
| Technical correctness | ☐ | ☐ | |
| Answer correctness | ☐ | ☐ | |
| Solution correctness | ☐ | ☐ | |
| Clarity / ambiguity | ☐ | ☐ | |
| Originality-conflict check | ☐ | ☐ | |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT

---

## Final certification procedure

1. Copy the reviewer identity, exact attestation, per-question checks, decisions and notes into `BATCH_001_HUMAN_FINAL_QA.json`.
2. Run `python scripts/validate_gate_ee_batch_001_human_signoff.py`.
3. Only after that validator passes, run `python scripts/promote_gate_ee_batch_001_paper_eligibility.py`.
4. Re-run every repository validator and inspect the generated certificate/admission manifest before publication.
