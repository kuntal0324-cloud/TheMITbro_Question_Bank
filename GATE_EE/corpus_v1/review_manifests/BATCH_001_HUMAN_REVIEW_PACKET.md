# GATE EE Batch 001 — Human Final QA Review Packet

**Questions:** 20  
**Canonical source SHA-256:** `2c218be6055cfa977da0842a6bdbc1edb61fe1712bf88794dc461052ae050b9e`  
**Formatter v2.0:** 20 PASS / 0 REVIEW  
**Independent AI QA:** 20/20 PASS  
**Human final QA:** REQUIRED  

> Automated/AI evidence is supporting evidence only. The human reviewer must independently judge each question.

---

## TMB-GATE-EE-EM-001 — Revision 1

**Topic:** Linear Algebra → Eigenvalues  
**Concept:** Eigenvalues of a symmetric 2x2 matrix  
**Type / Marks / Difficulty:** MCQ / 1 / Easy  

### Question
For the matrix $A=\begin{bmatrix}2&1\\1&2\end{bmatrix}$, the largest eigenvalue is

### Options
A. 1
B. 2
C. 3
D. 4

### Keyed answer
C

### Worked solution
The characteristic polynomial is $\det(A-\lambda I)=(2-\lambda)^2-1=\lambda^2-4\lambda+3$. Hence the eigenvalues are $1$ and $3$. The largest eigenvalue is $3$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Recomputed eigenvalues: 1 and 3; keyed answer confirmed.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-002 — Revision 1

**Topic:** Linear Algebra → Matrix inverse  
**Concept:** Trace of inverse using explicit inverse  
**Type / Marks / Difficulty:** NAT / 2 / Medium  

### Question
Let $A=\begin{bmatrix}1&2\\3&5\end{bmatrix}$. The value of $\operatorname{tr}(A^{-1})$ is ______.

### Keyed answer
-6

### Worked solution
Here $\det A=1\cdot5-2\cdot3=-1$. Therefore $A^{-1}=\frac{1}{-1}\begin{bmatrix}5&-2\\-3&1\end{bmatrix}=\begin{bmatrix}-5&2\\3&-1\end{bmatrix}$. Thus $\operatorname{tr}(A^{-1})=-5-1=-6$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Recomputed inverse and trace: -6.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-003 — Revision 1

**Topic:** Linear Algebra → Idempotent matrices  
**Concept:** Spectral properties of symmetric idempotent matrices  
**Type / Marks / Difficulty:** MSQ / 2 / Hard  

### Question
Let $P$ be a real symmetric idempotent matrix, i.e. $P^T=P$ and $P^2=P$. Which of the following statements are necessarily true?

### Options
A. Every eigenvalue of $P$ is either $0$ or $1$.
B. $P$ is positive semidefinite.
C. $\operatorname{tr}(P)=\operatorname{rank}(P)$.
D. $\det(P)=1$.

### Keyed answer
A, B, C

### Worked solution
If $Pv=\lambda v$, then $P^2v=\lambda^2v$, but $P^2=P$, so $\lambda^2=\lambda$ and $\lambda\in\{0,1\}$. Since $P$ is symmetric, it is orthogonally diagonalizable with nonnegative eigenvalues, hence positive semidefinite. The trace is the sum of eigenvalues and therefore equals the number of unit eigenvalues, which is the rank. The determinant need not be $1$; it is $0$ whenever $P$ has a zero eigenvalue.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Verified symmetric idempotent eigenvalues in {0,1}, PSD property, trace=rank, determinant claim false in general.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-004 — Revision 1

**Topic:** Calculus → Limits  
**Concept:** Second-order exponential limit  
**Type / Marks / Difficulty:** MCQ / 1 / Easy  

### Question
The value of $\displaystyle\lim_{x\to0}\frac{e^{2x}-1-2x}{x^2}$ is

### Options
A. 1
B. 2
C. 4
D. Does not exist

### Keyed answer
B

### Worked solution
Using $e^{2x}=1+2x+\frac{(2x)^2}{2}+O(x^3)=1+2x+2x^2+O(x^3)$, the numerator is $2x^2+O(x^3)$. Dividing by $x^2$ and taking the limit gives $2$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Series expansion independently gives limit 2.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-005 — Revision 2

**Topic:** Calculus → Optimization  
**Concept:** Absolute minimum on a closed interval  
**Type / Marks / Difficulty:** NAT / 2 / Medium  

### Question
Using the derivative of $f(x)=x^3-3x^2+2$, determine its absolute minimum value on the interval $0\le x\le3$. The minimum value is ______.

### Keyed answer
-2

### Worked solution
$f'(x)=3x(x-2)$, so the interior critical point is $x=2$. Evaluate the candidates: $f(0)=2$, $f(2)=8-12+2=-2$, and $f(3)=27-27+2=2$. Hence the minimum value is $-2$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Checked derivative, critical points and endpoints; absolute minimum is -2.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-006 — Revision 1

**Topic:** Calculus → Integration  
**Concept:** Substitution in a rational integral  
**Type / Marks / Difficulty:** MCQ / 2 / Medium  

### Question
The value of $\displaystyle\int_0^1\frac{x}{1+x^2}\,dx$ is

### Options
A. $\ln 2$
B. $\frac{1}{2}\ln 2$
C. $\frac{1}{4}\ln 2$
D. $1-\ln2$

### Keyed answer
B

### Worked solution
Put $u=1+x^2$, so $du=2x\,dx$. Then $\int_0^1\frac{x}{1+x^2}dx=\frac12\int_1^2\frac{du}{u}=\frac12\ln2$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Independent substitution yields (1/2) ln 2.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-007 — Revision 1

**Topic:** Differential Equations → First-order linear ODE  
**Concept:** Initial-value problem  
**Type / Marks / Difficulty:** NAT / 2 / Medium  

### Question
The solution of $y'+2y=4$ satisfies $y(0)=1$. The value of $y(\ln2)$ is ______.

### Keyed answer
1.75

### Worked solution
The solution is $y=2+Ce^{-2x}$. From $y(0)=1$, $C=-1$, hence $y=2-e^{-2x}$. At $x=\ln2$, $e^{-2\ln2}=1/4$, so $y=2-1/4=7/4=1.75$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Solved IVP independently; y(ln 2)=7/4=1.75.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-008 — Revision 1

**Topic:** Differential Equations → Second-order linear ODE  
**Concept:** Solution space for distinct real roots  
**Type / Marks / Difficulty:** MSQ / 2 / Medium  

### Question
Consider $y''+4y'+3y=0$. Which of the following are solutions?

### Options
A. $e^{-x}$
B. $e^{-3x}$
C. $e^{-2x}$
D. $2e^{-x}-5e^{-3x}$

### Keyed answer
A, B, D

### Worked solution
The characteristic equation is $r^2+4r+3=(r+1)(r+3)=0$, giving roots $-1$ and $-3$. Hence every solution has the form $C_1e^{-x}+C_2e^{-3x}$. Therefore A, B and D are solutions, while $e^{-2x}$ is not.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Characteristic roots -1 and -3; A, B and D verified.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-009 — Revision 1

**Topic:** Complex Variables → Complex algebra  
**Concept:** Powers of a complex number  
**Type / Marks / Difficulty:** MCQ / 1 / Easy  

### Question
The value of $(1+i)^4$ is

### Options
A. $4$
B. $-4$
C. $4i$
D. $-4i$

### Keyed answer
B

### Worked solution
$(1+i)^2=1+2i+i^2=2i$. Therefore $(1+i)^4=(2i)^2=-4$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Independent power calculation gives -4.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-010 — Revision 1

**Topic:** Complex Variables → Quadratic roots  
**Concept:** Distance between conjugate complex roots  
**Type / Marks / Difficulty:** NAT / 2 / Medium  

### Question
If $z_1$ and $z_2$ are the roots of $z^2-2z+5=0$, then $|z_1-z_2|$ is ______.

### Keyed answer
4

### Worked solution
The roots are $z=\frac{2\pm\sqrt{4-20}}{2}=1\pm2i$. Thus $z_1-z_2=4i$ up to sign, and therefore $|z_1-z_2|=4$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Roots 1±2i; separation magnitude 4.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-011 — Revision 1

**Topic:** Probability and Statistics → Probability axioms  
**Concept:** Union of independent events  
**Type / Marks / Difficulty:** MCQ / 1 / Easy  

### Question
Events $A$ and $B$ are independent with $P(A)=0.6$ and $P(B)=0.5$. Then $P(A\cup B)$ equals

### Options
A. 0.30
B. 0.50
C. 0.80
D. 1.10

### Keyed answer
C

### Worked solution
Independence gives $P(A\cap B)=0.6\times0.5=0.3$. Therefore $P(A\cup B)=P(A)+P(B)-P(A\cap B)=0.6+0.5-0.3=0.8$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Independent-event union recomputed as 0.8.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-012 — Revision 1

**Topic:** Probability and Statistics → Discrete random variables  
**Concept:** Second moment  
**Type / Marks / Difficulty:** NAT / 2 / Medium  

### Question
A random variable $X$ takes values $0,1,2$ with probabilities $0.2,0.5,0.3$, respectively. The value of $E[X^2]$ is ______.

### Keyed answer
1.7

### Worked solution
$E[X^2]=0^2(0.2)+1^2(0.5)+2^2(0.3)=0+0.5+1.2=1.7$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Second moment recomputed as 1.7.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-013 — Revision 1

**Topic:** Probability and Statistics → Expectation and variance  
**Concept:** Basic moment identities  
**Type / Marks / Difficulty:** MSQ / 2 / Medium  

### Question
Let a random variable $X$ have finite mean $\mu$ and variance $\sigma^2$. Which statements are necessarily true?

### Options
A. $E[X-\mu]=0$
B. $E[X^2]=\sigma^2+\mu^2$
C. $\operatorname{Var}(aX+b)=a^2\sigma^2$ for constants $a,b$
D. $E[(X-\mu)^2]=\sigma^2$

### Keyed answer
A, B, C, D

### Worked solution
By definition $\mu=E[X]$, so $E[X-\mu]=0$. Also $\sigma^2=E[X^2]-\mu^2$, giving $E[X^2]=\sigma^2+\mu^2$. Adding a constant does not change variance and scaling by $a$ scales variance by $a^2$. Finally, variance is defined as $E[(X-\mu)^2]$. Hence all four statements are true.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: All expectation/variance identities independently verified.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-014 — Revision 1

**Topic:** Numerical Methods → Newton-Raphson method  
**Concept:** One Newton iteration for a square root  
**Type / Marks / Difficulty:** NAT / 2 / Medium  

### Question
Newton-Raphson iteration is applied to $f(x)=x^2-2$ with $x_0=1.5$. The value of $x_1$, rounded to four decimal places, is ______.

### Keyed answer
1.4167

### Worked solution
Newton-Raphson gives $x_{n+1}=x_n-f(x_n)/f'(x_n)=\frac12(x_n+2/x_n)$. Thus $x_1=\frac12(1.5+2/1.5)=1.416666\ldots$, which rounds to $1.4167$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Newton step recomputed as 1.416666..., rounded 1.4167.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-015 — Revision 1

**Topic:** Numerical Methods → Interpolation  
**Concept:** Linear interpolation  
**Type / Marks / Difficulty:** MCQ / 1 / Easy  

### Question
The straight line interpolating the data points $(0,1)$ and $(2,5)$ has value at $x=1.5$ equal to

### Options
A. 3
B. 3.5
C. 4
D. 4.5

### Keyed answer
C

### Worked solution
The slope is $(5-1)/(2-0)=2$, so the interpolating line is $y=1+2x$. At $x=1.5$, $y=1+3=4$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Linear interpolation independently gives 4.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-016 — Revision 2

**Topic:** Linear Algebra → Linear systems  
**Concept:** Consistency and infinitely many solutions  
**Type / Marks / Difficulty:** NAT / 2 / Medium  

### Question
Consider the linear system whose coefficient matrix has proportional rows: $x+y=2$ and $2x+2y=k$. The system has infinitely many solutions for $k=$ ______.

### Keyed answer
4

### Worked solution
For infinitely many solutions, the second equation must be exactly twice the first. Twice $x+y=2$ gives $2x+2y=4$. Hence $k=4$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Linear-system consistency independently gives k=4.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-017 — Revision 1

**Topic:** Calculus → Multivariable calculus  
**Concept:** Directional derivative  
**Type / Marks / Difficulty:** MCQ / 2 / Hard  

### Question
For $f(x,y)=x^2y+y^2$, the directional derivative at $(1,2)$ in the direction of the vector $3\mathbf{i}+4\mathbf{j}$ is

### Options
A. $5$
B. $\frac{32}{5}$
C. $8$
D. $\frac{41}{5}$

### Keyed answer
B

### Worked solution
$\nabla f=(2xy,x^2+2y)$. At $(1,2)$, $\nabla f=(4,5)$. The unit vector in the direction $(3,4)$ is $(3/5,4/5)$. Hence the directional derivative is $(4,5)\cdot(3/5,4/5)=12/5+20/5=32/5$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Directional derivative independently gives 32/5.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-018 — Revision 1

**Topic:** Calculus → Vector calculus  
**Concept:** Divergence, curl and Green/Stokes circulation  
**Type / Marks / Difficulty:** MSQ / 2 / Hard  

### Question
For the planar vector field $\mathbf{F}=y\mathbf{i}-x\mathbf{j}$, which statements are true?

### Options
A. $\nabla\cdot\mathbf{F}=0$
B. $\nabla\times\mathbf{F}=-2\mathbf{k}$
C. $\mathbf{F}$ is conservative on $\mathbb{R}^2$
D. The counter-clockwise circulation around the unit circle is $-2\pi$

### Keyed answer
A, B, D

### Worked solution
With $P=y$ and $Q=-x$, divergence is $\partial P/\partial x+\partial Q/\partial y=0+0=0$. The scalar curl is $\partial Q/\partial x-\partial P/\partial y=-1-1=-2$, i.e. $-2\mathbf{k}$. Since the curl is nonzero, the field is not conservative. Green's theorem gives the counter-clockwise circulation as $\iint_D(-2)\,dA=-2\pi$ for the unit disk.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Divergence 0, curl -2k and CCW circulation -2π independently verified.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-019 — Revision 1

**Topic:** Probability and Statistics → Bernoulli distribution  
**Concept:** Variance of a Bernoulli random variable  
**Type / Marks / Difficulty:** NAT / 2 / Easy  

### Question
If $X$ is a Bernoulli random variable with $P(X=1)=0.4$, then $\operatorname{Var}(X)$ is ______.

### Keyed answer
0.24

### Worked solution
For a Bernoulli random variable with parameter $p$, $\operatorname{Var}(X)=p(1-p)$. Thus the variance is $0.4\times0.6=0.24$.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Bernoulli variance independently gives 0.24.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---

## TMB-GATE-EE-EM-020 — Revision 1

**Topic:** Numerical Methods → Numerical integration  
**Concept:** Simpson one-third rule  
**Type / Marks / Difficulty:** MCQ / 2 / Medium  

### Question
Using Simpson's $1/3$ rule with two equal subintervals, the approximation to $\displaystyle\int_0^2 x^2\,dx$ is

### Options
A. $2$
B. $\frac{7}{3}$
C. $\frac{8}{3}$
D. $3$

### Keyed answer
C

### Worked solution
With $h=1$, Simpson's rule gives $\frac{h}{3}[f(0)+4f(1)+f(2)]=\frac13[0+4(1)+4]=\frac83$. Since the integrand is a polynomial of degree two, Simpson's rule is exact here.

### Supporting evidence
- Formatter v2.0: PASS
- Independent AI QA: PASS
- AI recomputation note: Simpson 1/3 calculation independently gives 8/3.

### Human reviewer checklist
- [ ] Technical correctness independently checked
- [ ] Answer independently checked
- [ ] Solution independently checked
- [ ] Clarity / ambiguity checked
- [ ] Originality-conflict check performed
- Decision: PASS / REVISE / REJECT
- Notes:

---