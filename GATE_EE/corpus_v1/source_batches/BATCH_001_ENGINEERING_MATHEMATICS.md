# GATE EE Corpus V1 — Production Batch 001

**Domain:** Engineering Mathematics  
**Questions:** 20  
**Commercial status:** NOT YET PAPER-ELIGIBLE  
**Lifecycle state:** DRAFT — automated structural/mathematical checks included; independent human review remains mandatory.  
**Originality:** ORIGINAL_THEMITBRO

> This is original TheMITbro-style practice content. It is not copied from an official GATE paper.

---

## TMB-GATE-EE-EM-001

- **Subject:** Engineering Mathematics
- **Topic:** Linear Algebra
- **Subtopic:** Eigenvalues
- **Concept:** Eigenvalues of a symmetric 2x2 matrix
- **Difficulty:** Easy
- **Type:** MCQ
- **Marks:** 1
- **Estimated Time:** 75 s
- **Family ID:** EM-LA-EIG-001
- **Revision:** 1
- **Status:** DRAFT

### Question
For the matrix $A=\begin{bmatrix}2&1\\1&2\end{bmatrix}$, the largest eigenvalue is

### Options
A. 1
B. 2
C. 3
D. 4

### Answer
C

### Detailed Solution
The characteristic polynomial is $\det(A-\lambda I)=(2-\lambda)^2-1=\lambda^2-4\lambda+3$. Hence the eigenvalues are $1$ and $3$. The largest eigenvalue is $3$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-002

- **Subject:** Engineering Mathematics
- **Topic:** Linear Algebra
- **Subtopic:** Matrix inverse
- **Concept:** Trace of inverse using explicit inverse
- **Difficulty:** Medium
- **Type:** NAT
- **Marks:** 2
- **Estimated Time:** 120 s
- **Family ID:** EM-LA-INVTRACE-001
- **Revision:** 1
- **Status:** DRAFT

### Question
Let $A=\begin{bmatrix}1&2\\3&5\end{bmatrix}$. The value of $\operatorname{tr}(A^{-1})$ is ______.

### Answer
-6

**Accepted tolerance:** 0.0

### Detailed Solution
Here $\det A=1\cdot5-2\cdot3=-1$. Therefore $A^{-1}=\frac{1}{-1}\begin{bmatrix}5&-2\\-3&1\end{bmatrix}=\begin{bmatrix}-5&2\\3&-1\end{bmatrix}$. Thus $\operatorname{tr}(A^{-1})=-5-1=-6$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-003

- **Subject:** Engineering Mathematics
- **Topic:** Linear Algebra
- **Subtopic:** Idempotent matrices
- **Concept:** Spectral properties of symmetric idempotent matrices
- **Difficulty:** Hard
- **Type:** MSQ
- **Marks:** 2
- **Estimated Time:** 150 s
- **Family ID:** EM-LA-IDEMP-001
- **Revision:** 1
- **Status:** DRAFT

### Question
Let $P$ be a real symmetric idempotent matrix, i.e. $P^T=P$ and $P^2=P$. Which of the following statements are necessarily true?

### Options
A. Every eigenvalue of $P$ is either $0$ or $1$.
B. $P$ is positive semidefinite.
C. $\operatorname{tr}(P)=\operatorname{rank}(P)$.
D. $\det(P)=1$.

### Answer
A, B, C

### Detailed Solution
If $Pv=\lambda v$, then $P^2v=\lambda^2v$, but $P^2=P$, so $\lambda^2=\lambda$ and $\lambda\in\{0,1\}$. Since $P$ is symmetric, it is orthogonally diagonalizable with nonnegative eigenvalues, hence positive semidefinite. The trace is the sum of eigenvalues and therefore equals the number of unit eigenvalues, which is the rank. The determinant need not be $1$; it is $0$ whenever $P$ has a zero eigenvalue.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-004

- **Subject:** Engineering Mathematics
- **Topic:** Calculus
- **Subtopic:** Limits
- **Concept:** Second-order exponential limit
- **Difficulty:** Easy
- **Type:** MCQ
- **Marks:** 1
- **Estimated Time:** 75 s
- **Family ID:** EM-CAL-LIMIT-001
- **Revision:** 1
- **Status:** DRAFT

### Question
The value of $\displaystyle\lim_{x\to0}\frac{e^{2x}-1-2x}{x^2}$ is

### Options
A. 1
B. 2
C. 4
D. Does not exist

### Answer
B

### Detailed Solution
Using $e^{2x}=1+2x+\frac{(2x)^2}{2}+O(x^3)=1+2x+2x^2+O(x^3)$, the numerator is $2x^2+O(x^3)$. Dividing by $x^2$ and taking the limit gives $2$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-005

- **Subject:** Engineering Mathematics
- **Topic:** Calculus
- **Subtopic:** Optimization
- **Concept:** Absolute minimum on a closed interval
- **Difficulty:** Medium
- **Type:** NAT
- **Marks:** 2
- **Estimated Time:** 120 s
- **Family ID:** EM-CAL-OPT-001
- **Revision:** 1
- **Status:** DRAFT

### Question
For $f(x)=x^3-3x^2+2$ on the interval $0\le x\le3$, the minimum value of $f(x)$ is ______.

### Answer
-2

**Accepted tolerance:** 0.0

### Detailed Solution
$f'(x)=3x(x-2)$, so the interior critical point is $x=2$. Evaluate the candidates: $f(0)=2$, $f(2)=8-12+2=-2$, and $f(3)=27-27+2=2$. Hence the minimum value is $-2$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-006

- **Subject:** Engineering Mathematics
- **Topic:** Calculus
- **Subtopic:** Integration
- **Concept:** Substitution in a rational integral
- **Difficulty:** Medium
- **Type:** MCQ
- **Marks:** 2
- **Estimated Time:** 105 s
- **Family ID:** EM-CAL-INT-001
- **Revision:** 1
- **Status:** DRAFT

### Question
The value of $\displaystyle\int_0^1\frac{x}{1+x^2}\,dx$ is

### Options
A. $\ln 2$
B. $\frac{1}{2}\ln 2$
C. $\frac{1}{4}\ln 2$
D. $1-\ln2$

### Answer
B

### Detailed Solution
Put $u=1+x^2$, so $du=2x\,dx$. Then $\int_0^1\frac{x}{1+x^2}dx=\frac12\int_1^2\frac{du}{u}=\frac12\ln2$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-007

- **Subject:** Engineering Mathematics
- **Topic:** Differential Equations
- **Subtopic:** First-order linear ODE
- **Concept:** Initial-value problem
- **Difficulty:** Medium
- **Type:** NAT
- **Marks:** 2
- **Estimated Time:** 120 s
- **Family ID:** EM-DE-FIRSTORDER-001
- **Revision:** 1
- **Status:** DRAFT

### Question
The solution of $y'+2y=4$ satisfies $y(0)=1$. The value of $y(\ln2)$ is ______.

### Answer
1.75

**Accepted tolerance:** 0.001

### Detailed Solution
The solution is $y=2+Ce^{-2x}$. From $y(0)=1$, $C=-1$, hence $y=2-e^{-2x}$. At $x=\ln2$, $e^{-2\ln2}=1/4$, so $y=2-1/4=7/4=1.75$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-008

- **Subject:** Engineering Mathematics
- **Topic:** Differential Equations
- **Subtopic:** Second-order linear ODE
- **Concept:** Solution space for distinct real roots
- **Difficulty:** Medium
- **Type:** MSQ
- **Marks:** 2
- **Estimated Time:** 135 s
- **Family ID:** EM-DE-SECONDORDER-001
- **Revision:** 1
- **Status:** DRAFT

### Question
Consider $y''+4y'+3y=0$. Which of the following are solutions?

### Options
A. $e^{-x}$
B. $e^{-3x}$
C. $e^{-2x}$
D. $2e^{-x}-5e^{-3x}$

### Answer
A, B, D

### Detailed Solution
The characteristic equation is $r^2+4r+3=(r+1)(r+3)=0$, giving roots $-1$ and $-3$. Hence every solution has the form $C_1e^{-x}+C_2e^{-3x}$. Therefore A, B and D are solutions, while $e^{-2x}$ is not.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-009

- **Subject:** Engineering Mathematics
- **Topic:** Complex Variables
- **Subtopic:** Complex algebra
- **Concept:** Powers of a complex number
- **Difficulty:** Easy
- **Type:** MCQ
- **Marks:** 1
- **Estimated Time:** 60 s
- **Family ID:** EM-CV-POWER-001
- **Revision:** 1
- **Status:** DRAFT

### Question
The value of $(1+i)^4$ is

### Options
A. $4$
B. $-4$
C. $4i$
D. $-4i$

### Answer
B

### Detailed Solution
$(1+i)^2=1+2i+i^2=2i$. Therefore $(1+i)^4=(2i)^2=-4$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-010

- **Subject:** Engineering Mathematics
- **Topic:** Complex Variables
- **Subtopic:** Quadratic roots
- **Concept:** Distance between conjugate complex roots
- **Difficulty:** Medium
- **Type:** NAT
- **Marks:** 2
- **Estimated Time:** 105 s
- **Family ID:** EM-CV-ROOTDIST-001
- **Revision:** 1
- **Status:** DRAFT

### Question
If $z_1$ and $z_2$ are the roots of $z^2-2z+5=0$, then $|z_1-z_2|$ is ______.

### Answer
4

**Accepted tolerance:** 0.0

### Detailed Solution
The roots are $z=\frac{2\pm\sqrt{4-20}}{2}=1\pm2i$. Thus $z_1-z_2=4i$ up to sign, and therefore $|z_1-z_2|=4$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-011

- **Subject:** Engineering Mathematics
- **Topic:** Probability and Statistics
- **Subtopic:** Probability axioms
- **Concept:** Union of independent events
- **Difficulty:** Easy
- **Type:** MCQ
- **Marks:** 1
- **Estimated Time:** 75 s
- **Family ID:** EM-PS-INDEP-001
- **Revision:** 1
- **Status:** DRAFT

### Question
Events $A$ and $B$ are independent with $P(A)=0.6$ and $P(B)=0.5$. Then $P(A\cup B)$ equals

### Options
A. 0.30
B. 0.50
C. 0.80
D. 1.10

### Answer
C

### Detailed Solution
Independence gives $P(A\cap B)=0.6\times0.5=0.3$. Therefore $P(A\cup B)=P(A)+P(B)-P(A\cap B)=0.6+0.5-0.3=0.8$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-012

- **Subject:** Engineering Mathematics
- **Topic:** Probability and Statistics
- **Subtopic:** Discrete random variables
- **Concept:** Second moment
- **Difficulty:** Medium
- **Type:** NAT
- **Marks:** 2
- **Estimated Time:** 105 s
- **Family ID:** EM-PS-MOMENT-001
- **Revision:** 1
- **Status:** DRAFT

### Question
A random variable $X$ takes values $0,1,2$ with probabilities $0.2,0.5,0.3$, respectively. The value of $E[X^2]$ is ______.

### Answer
1.7

**Accepted tolerance:** 0.001

### Detailed Solution
$E[X^2]=0^2(0.2)+1^2(0.5)+2^2(0.3)=0+0.5+1.2=1.7$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-013

- **Subject:** Engineering Mathematics
- **Topic:** Probability and Statistics
- **Subtopic:** Expectation and variance
- **Concept:** Basic moment identities
- **Difficulty:** Medium
- **Type:** MSQ
- **Marks:** 2
- **Estimated Time:** 135 s
- **Family ID:** EM-PS-VARIDENT-001
- **Revision:** 1
- **Status:** DRAFT

### Question
Let a random variable $X$ have finite mean $\mu$ and variance $\sigma^2$. Which statements are necessarily true?

### Options
A. $E[X-\mu]=0$
B. $E[X^2]=\sigma^2+\mu^2$
C. $\operatorname{Var}(aX+b)=a^2\sigma^2$ for constants $a,b$
D. $E[(X-\mu)^2]=\sigma^2$

### Answer
A, B, C, D

### Detailed Solution
By definition $\mu=E[X]$, so $E[X-\mu]=0$. Also $\sigma^2=E[X^2]-\mu^2$, giving $E[X^2]=\sigma^2+\mu^2$. Adding a constant does not change variance and scaling by $a$ scales variance by $a^2$. Finally, variance is defined as $E[(X-\mu)^2]$. Hence all four statements are true.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-014

- **Subject:** Engineering Mathematics
- **Topic:** Numerical Methods
- **Subtopic:** Newton-Raphson method
- **Concept:** One Newton iteration for a square root
- **Difficulty:** Medium
- **Type:** NAT
- **Marks:** 2
- **Estimated Time:** 120 s
- **Family ID:** EM-NM-NEWTON-001
- **Revision:** 1
- **Status:** DRAFT

### Question
Newton-Raphson iteration is applied to $f(x)=x^2-2$ with $x_0=1.5$. The value of $x_1$, rounded to four decimal places, is ______.

### Answer
1.4167

**Accepted tolerance:** 0.0001

### Detailed Solution
Newton-Raphson gives $x_{n+1}=x_n-f(x_n)/f'(x_n)=\frac12(x_n+2/x_n)$. Thus $x_1=\frac12(1.5+2/1.5)=1.416666\ldots$, which rounds to $1.4167$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-015

- **Subject:** Engineering Mathematics
- **Topic:** Numerical Methods
- **Subtopic:** Interpolation
- **Concept:** Linear interpolation
- **Difficulty:** Easy
- **Type:** MCQ
- **Marks:** 1
- **Estimated Time:** 75 s
- **Family ID:** EM-NM-INTERP-001
- **Revision:** 1
- **Status:** DRAFT

### Question
The straight line interpolating the data points $(0,1)$ and $(2,5)$ has value at $x=1.5$ equal to

### Options
A. 3
B. 3.5
C. 4
D. 4.5

### Answer
C

### Detailed Solution
The slope is $(5-1)/(2-0)=2$, so the interpolating line is $y=1+2x$. At $x=1.5$, $y=1+3=4$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-016

- **Subject:** Engineering Mathematics
- **Topic:** Linear Algebra
- **Subtopic:** Linear systems
- **Concept:** Consistency and infinitely many solutions
- **Difficulty:** Medium
- **Type:** NAT
- **Marks:** 2
- **Estimated Time:** 90 s
- **Family ID:** EM-LA-SYSTEM-001
- **Revision:** 1
- **Status:** DRAFT

### Question
The system $x+y=2$ and $2x+2y=k$ has infinitely many solutions for $k=$ ______.

### Answer
4

**Accepted tolerance:** 0.0

### Detailed Solution
For infinitely many solutions, the second equation must be exactly twice the first. Twice $x+y=2$ gives $2x+2y=4$. Hence $k=4$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-017

- **Subject:** Engineering Mathematics
- **Topic:** Calculus
- **Subtopic:** Multivariable calculus
- **Concept:** Directional derivative
- **Difficulty:** Hard
- **Type:** MCQ
- **Marks:** 2
- **Estimated Time:** 150 s
- **Family ID:** EM-CAL-DIRDER-001
- **Revision:** 1
- **Status:** DRAFT

### Question
For $f(x,y)=x^2y+y^2$, the directional derivative at $(1,2)$ in the direction of the vector $3\mathbf{i}+4\mathbf{j}$ is

### Options
A. $5$
B. $\frac{32}{5}$
C. $8$
D. $\frac{41}{5}$

### Answer
B

### Detailed Solution
$\nabla f=(2xy,x^2+2y)$. At $(1,2)$, $\nabla f=(4,5)$. The unit vector in the direction $(3,4)$ is $(3/5,4/5)$. Hence the directional derivative is $(4,5)\cdot(3/5,4/5)=12/5+20/5=32/5$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-018

- **Subject:** Engineering Mathematics
- **Topic:** Calculus
- **Subtopic:** Vector calculus
- **Concept:** Divergence, curl and Green/Stokes circulation
- **Difficulty:** Hard
- **Type:** MSQ
- **Marks:** 2
- **Estimated Time:** 180 s
- **Family ID:** EM-CAL-VECCALC-001
- **Revision:** 1
- **Status:** DRAFT

### Question
For the planar vector field $\mathbf{F}=y\mathbf{i}-x\mathbf{j}$, which statements are true?

### Options
A. $\nabla\cdot\mathbf{F}=0$
B. $\nabla\times\mathbf{F}=-2\mathbf{k}$
C. $\mathbf{F}$ is conservative on $\mathbb{R}^2$
D. The counter-clockwise circulation around the unit circle is $-2\pi$

### Answer
A, B, D

### Detailed Solution
With $P=y$ and $Q=-x$, divergence is $\partial P/\partial x+\partial Q/\partial y=0+0=0$. The scalar curl is $\partial Q/\partial x-\partial P/\partial y=-1-1=-2$, i.e. $-2\mathbf{k}$. Since the curl is nonzero, the field is not conservative. Green's theorem gives the counter-clockwise circulation as $\iint_D(-2)\,dA=-2\pi$ for the unit disk.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-019

- **Subject:** Engineering Mathematics
- **Topic:** Probability and Statistics
- **Subtopic:** Bernoulli distribution
- **Concept:** Variance of a Bernoulli random variable
- **Difficulty:** Easy
- **Type:** NAT
- **Marks:** 2
- **Estimated Time:** 75 s
- **Family ID:** EM-PS-BERNOULLI-001
- **Revision:** 1
- **Status:** DRAFT

### Question
If $X$ is a Bernoulli random variable with $P(X=1)=0.4$, then $\operatorname{Var}(X)$ is ______.

### Answer
0.24

**Accepted tolerance:** 0.001

### Detailed Solution
For a Bernoulli random variable with parameter $p$, $\operatorname{Var}(X)=p(1-p)$. Thus the variance is $0.4\times0.6=0.24$.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---

## TMB-GATE-EE-EM-020

- **Subject:** Engineering Mathematics
- **Topic:** Numerical Methods
- **Subtopic:** Numerical integration
- **Concept:** Simpson one-third rule
- **Difficulty:** Medium
- **Type:** MCQ
- **Marks:** 2
- **Estimated Time:** 120 s
- **Family ID:** EM-NM-SIMPSON-001
- **Revision:** 1
- **Status:** DRAFT

### Question
Using Simpson's $1/3$ rule with two equal subintervals, the approximation to $\displaystyle\int_0^2 x^2\,dx$ is

### Options
A. $2$
B. $\frac{7}{3}$
C. $\frac{8}{3}$
D. $3$

### Answer
C

### Detailed Solution
With $h=1$, Simpson's rule gives $\frac{h}{3}[f(0)+4f(1)+f(2)]=\frac13[0+4(1)+4]=\frac83$. Since the integrand is a polynomial of degree two, Simpson's rule is exact here.

### Review State
- Technical correctness: PENDING independent review
- Answer verification: PENDING independent review
- Solution verification: PENDING independent review
- Originality review: PENDING independent review
- Formatter v2.0 validation: PENDING
- Duplicate/family review: PENDING

---