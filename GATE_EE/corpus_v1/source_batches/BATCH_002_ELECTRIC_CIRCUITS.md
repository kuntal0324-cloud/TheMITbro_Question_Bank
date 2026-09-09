# GATE EE Production Batch 002 — Electric Circuits

**Status:** DRAFT — NOT PAPER-ELIGIBLE
**Questions:** 20

This is a deterministic view of the canonical JSONL source. Review decisions belong in checksum-bound review artifacts, not in this generated document.

---

## TMB-GATE-EE-NT-001 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Network Elements
**Type / marks / difficulty:** NAT / 1 / Easy
**Family:** `NT-NE-CAPENERGY-001`

### Question

A $6\,\mu\mathrm{F}$ capacitor and a $3\,\mu\mathrm{F}$ capacitor are connected in series across an $18\,\mathrm{V}$ DC source. Determine the total energy stored by this capacitor network; enter the numerical value in $\mathrm{mJ}$.

### Declared answer

0.324

### Canonical solution

The series equivalent capacitance is $C_{\mathrm{eq}}=\frac{(6)(3)}{6+3}\,\mu\mathrm{F}=2\,\mu\mathrm{F}$. The stored energy is $W=\frac{1}{2}C_{\mathrm{eq}}V^2=\frac{1}{2}(2\times10^{-6})(18)^2=324\times10^{-6}\,\mathrm{J}=0.324\,\mathrm{mJ}$.
Final answer: 0.324

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-002 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Network Elements
**Type / marks / difficulty:** MCQ / 1 / Medium
**Family:** `NT-NE-COUPLED-001`

### Question

Two coupled inductors in a series-aiding network have $L_1=4\,\mathrm{H}$, $L_2=9\,\mathrm{H}$ and coefficient of coupling $k=0.5$. Determine the equivalent inductance.

### Options

- A. $7\,\mathrm{H}$
- B. $13\,\mathrm{H}$
- C. $19\,\mathrm{H}$
- D. $25\,\mathrm{H}$

### Declared answer

C

### Canonical solution

The mutual inductance is $M=k\sqrt{L_1L_2}=0.5\sqrt{(4)(9)}=3\,\mathrm{H}$. For a series-aiding connection, $L_{\mathrm{eq}}=L_1+L_2+2M=4+9+6=19\,\mathrm{H}$.
Final answer: C

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-003 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Circuit Laws and Analysis
**Type / marks / difficulty:** MCQ / 2 / Hard
**Family:** `NT-CA-DEPPORT-001`

### Question

At the input port of a linear network, a $4\,\Omega$ resistor is connected from the port to ground. A dependent current source of value $0.5i_R$, where $i_R$ is the resistor current, is also directed from the port to ground. Determine the resistance seen at the port.

### Options

- A. $2\,\Omega$
- B. $\frac{8}{3}\,\Omega$
- C. $4\,\Omega$
- D. $6\,\Omega$

### Declared answer

B

### Canonical solution

Apply a test voltage $v$ at the port. The resistor current is $i_R=\frac{v}{4}$, and the dependent-source current is $0.5i_R$. Hence $i_{\mathrm{in}}=\frac{v}{4}+0.5\left(\frac{v}{4}\right)=\frac{3v}{8}$, so $R_{\mathrm{in}}=\frac{v}{i_{\mathrm{in}}}=\frac{8}{3}\,\Omega$.
Final answer: B

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-004 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Network Elements
**Type / marks / difficulty:** MSQ / 1 / Easy
**Family:** `NT-NE-CONTINUITY-001`

### Question

Select every correct statement about ideal passive network elements under finite, impulse-free excitation; one or more options may be correct.

### Options

- A. The energy stored in a capacitor is $\frac{1}{2}Cv^2$.
- B. The energy stored in an inductor is $Li^2$.
- C. A capacitor voltage cannot change instantaneously.
- D. An inductor current cannot change instantaneously.

### Declared answer

A, C, D

### Canonical solution

Capacitor energy is $\frac{1}{2}Cv^2$, whereas inductor energy is $\frac{1}{2}Li^2$; therefore option B is missing the factor $\frac{1}{2}$. With finite, impulse-free excitation, capacitor voltage and inductor current cannot change instantaneously. Therefore A, C and D are correct.
Final answer: A, C, D

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-005 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Circuit Laws and Analysis
**Type / marks / difficulty:** NAT / 2 / Medium
**Family:** `NT-CA-NODAL2-001`

### Question

In a resistive network, node $v_1$ is connected to a $12\,\mathrm{V}$ source through $3\,\Omega$, to ground through $6\,\Omega$, and to node $v_2$ through $2\,\Omega$. Node $v_2$ is connected to ground through $4\,\Omega$. Using KCL and node-voltage analysis, determine $v_2$; enter the numerical value in $\mathrm{V}$.

### Declared answer

4

### Canonical solution

KCL at $v_2$ gives $\frac{v_2-v_1}{2}+\frac{v_2}{4}=0$, hence $v_1=1.5v_2$. KCL at $v_1$ gives $\frac{v_1-12}{3}+\frac{v_1}{6}+\frac{v_1-v_2}{2}=0$. Multiplying by $6$ yields $6v_1-3v_2=24$. Substitution gives $6(1.5v_2)-3v_2=24$, so $v_2=4\,\mathrm{V}$.
Final answer: 4

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-006 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Circuit Laws and Analysis
**Type / marks / difficulty:** NAT / 2 / Hard
**Family:** `NT-CA-SUPERNODE-001`

### Question

Two non-reference node voltages satisfy $v_1-v_2=5\,\mathrm{V}$ because of an ideal voltage source between them. A $2\,\Omega$ branch connects $v_1$ to ground, a $3\,\Omega$ branch connects $v_2$ to ground, and a $4\,\mathrm{A}$ current source injects current into $v_2$. Using supernode KCL, determine $v_1$; enter the numerical value in $\mathrm{V}$.

### Declared answer

6.8

### Canonical solution

KCL for the supernode is $\frac{v_1}{2}+\frac{v_2}{3}=4$. The voltage-source constraint is $v_1=v_2+5$. Substituting and multiplying by $6$ gives $3(v_2+5)+2v_2=24$, so $v_2=1.8\,\mathrm{V}$ and $v_1=6.8\,\mathrm{V}$.
Final answer: 6.8

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-007 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Circuit Laws and Analysis
**Type / marks / difficulty:** MCQ / 2 / Medium
**Family:** `NT-CA-MESH2-001`

### Question

Clockwise mesh currents $I_1$ and $I_2$ in a resistor network satisfy $5I_1-2I_2=8$ and $-2I_1+4I_2=2$. Determine the current in their common branch, directed with $I_1$.

### Options

- A. $0.625\,\mathrm{A}$
- B. $1.625\,\mathrm{A}$
- C. $2.250\,\mathrm{A}$
- D. $3.875\,\mathrm{A}$

### Declared answer

A

### Canonical solution

Solving the mesh-current equations gives $I_1=\frac{36}{16}=2.25\,\mathrm{A}$ and $I_2=\frac{26}{16}=1.625\,\mathrm{A}$. The common-branch current in the $I_1$ direction is $I_1-I_2=0.625\,\mathrm{A}$.
Final answer: A

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-008 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Circuit Laws and Analysis
**Type / marks / difficulty:** MSQ / 1 / Easy
**Family:** `NT-CA-NODALRULES-001`

### Question

Select every correct statement about node-voltage analysis of a connected electrical network; one or more options may be correct.

### Options

- A. One node is selected as the reference node.
- B. An ideal voltage source between two non-reference nodes can be handled using a supernode.
- C. For $n$ nodes, at most $n-1$ independent KCL node equations are required.
- D. The method cannot be used when dependent sources are present.

### Declared answer

A, B, C

### Canonical solution

Node-voltage analysis selects a reference, uses supernodes for ideal voltage sources between unknown nodes, and requires at most $n-1$ independent KCL equations. Dependent sources are permitted when their controlling relations are included. Thus A, B and C are correct.
Final answer: A, B, C

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-009 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Network Theorems
**Type / marks / difficulty:** MCQ / 2 / Medium
**Family:** `NT-TH-THEVENINLOAD-001`

### Question

An $18\,\mathrm{V}$ ideal source feeds a $3\,\Omega$ series resistor and an output node; a $6\,\Omega$ resistor connects that node to ground. A $4\,\Omega$ load is then connected from the output node to ground. Determine the load current using the Thevenin equivalent of the source network.

### Options

- A. $1\,\mathrm{A}$
- B. $2\,\mathrm{A}$
- C. $3\,\mathrm{A}$
- D. $4\,\mathrm{A}$

### Declared answer

B

### Canonical solution

The open-circuit voltage is $V_{\mathrm{th}}=18\left(\frac{6}{3+6}\right)=12\,\mathrm{V}$. With the independent source deactivated, $R_{\mathrm{th}}=3\parallel6=2\,\Omega$. Therefore $I_L=\frac{12}{2+4}=2\,\mathrm{A}$.
Final answer: B

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-010 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Network Theorems
**Type / marks / difficulty:** MCQ / 1 / Easy
**Family:** `NT-TH-NORTONDIV-001`

### Question

A Norton network consists of a $3\,\mathrm{A}$ current source in parallel with $6\,\Omega$. When a $3\,\Omega$ load is connected across the network, determine the load current.

### Options

- A. $0.5\,\mathrm{A}$
- B. $1\,\mathrm{A}$
- C. $2\,\mathrm{A}$
- D. $3\,\mathrm{A}$

### Declared answer

C

### Canonical solution

By current division, the $3\,\mathrm{A}$ Norton current splits between $6\,\Omega$ and $3\,\Omega$. The load current is $I_L=3\left(\frac{6}{6+3}\right)=2\,\mathrm{A}$.
Final answer: C

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-011 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Network Theorems
**Type / marks / difficulty:** NAT / 2 / Hard
**Family:** `NT-TH-ACMAXPOWER-001`

### Question

A sinusoidal network has Thevenin RMS voltage $V_{\mathrm{th}}=10\,\mathrm{V}$ and Thevenin impedance $Z_{\mathrm{th}}=(3+j4)\,\Omega$. A conjugately matched load is connected. Determine the maximum average load power; enter the numerical value in $\mathrm{W}$.

### Declared answer

8.333

### Canonical solution

For conjugate matching, $Z_L=Z_{\mathrm{th}}^*=(3-j4)\,\Omega$. The maximum average load power is $P_{\max}=\frac{|V_{\mathrm{th}}|^2}{4R_{\mathrm{th}}}=\frac{10^2}{4(3)}=8.333\,\mathrm{W}$.
Final answer: 8.333

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-012 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Network Theorems
**Type / marks / difficulty:** MSQ / 1 / Medium
**Family:** `NT-TH-SUPERPOSITION-001`

### Question

Select every correct statement about superposition in a linear electrical network; one or more options may be correct.

### Options

- A. An independent ideal voltage source is replaced by a short circuit when deactivated.
- B. An independent ideal current source is replaced by an open circuit when deactivated.
- C. Dependent sources remain active.
- D. The total power cannot in general be obtained by adding the powers caused by the individual sources.

### Declared answer

A, B, C, D

### Canonical solution

Superposition deactivates only independent sources: ideal voltage sources become shorts and ideal current sources become opens. Dependent sources remain because they are part of the network model. Voltages and currents superpose, but power is nonlinear, so the separate-source powers do not generally add. All four statements are correct.
Final answer: A, B, C, D

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-013 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Transient Analysis
**Type / marks / difficulty:** NAT / 2 / Medium
**Family:** `NT-TR-RCONE-001`

### Question

In a first-order RC network, the capacitor voltage is initially $2\,\mathrm{V}$ and its steady-state value after switching is $10\,\mathrm{V}$. The resistance is $2\,\mathrm{k}\Omega$ and the capacitance is $100\,\mu\mathrm{F}$. Determine the capacitor voltage one time constant after switching; enter the numerical value in $\mathrm{V}$.

### Declared answer

7.057

### Canonical solution

The time constant is $\tau=RC=(2000)(100\times10^{-6})=0.2\,\mathrm{s}$. At $t=\tau$, $v_C(\tau)=10+(2-10)e^{-1}=10-\frac{8}{e}=7.057\,\mathrm{V}$.
Final answer: 7.057

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-014 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Transient Analysis
**Type / marks / difficulty:** NAT / 2 / Medium
**Family:** `NT-TR-RLSTEP-001`

### Question

A $12\,\mathrm{V}$ DC source is applied at $t=0$ to an initially unenergized series RL network with resistance $R=4\,\Omega$ and inductance $L=2\,\mathrm{H}$. Determine the inductor current at $t=(0.5\ln 2)\,\mathrm{s}$; enter the numerical value in $\mathrm{A}$.

### Declared answer

1.5

### Canonical solution

The final current is $I_{\infty}=\frac{12}{4}=3\,\mathrm{A}$, and the time constant is $\tau=\frac{L}{R}=\frac{2}{4}=0.5\,\mathrm{s}$. Here $\frac{t}{\tau}=\ln 2$, so $i_L(t)=3\left(1-e^{-\ln 2}\right)=3\left(1-\frac{1}{2}\right)=1.5\,\mathrm{A}$.
Final answer: 1.5

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-015 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Resonance and Two-Port Networks
**Type / marks / difficulty:** MCQ / 1 / Easy
**Family:** `NT-AC-RESONANCE-001`

### Question

A series RLC network has inductance $L=50\,\mathrm{mH}$ and capacitance $C=20\,\mu\mathrm{F}$. Determine its undamped resonant angular frequency.

### Options

- A. $100\,\mathrm{rad\,s^{-1}}$
- B. $500\,\mathrm{rad\,s^{-1}}$
- C. $1000\,\mathrm{rad\,s^{-1}}$
- D. $5000\,\mathrm{rad\,s^{-1}}$

### Declared answer

C

### Canonical solution

The resonant angular frequency is $\omega_0=\frac{1}{\sqrt{LC}}$. Since $LC=(50\times10^{-3})(20\times10^{-6})=10^{-6}$, $\omega_0=\frac{1}{10^{-3}}=1000\,\mathrm{rad\,s^{-1}}$.
Final answer: C

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-016 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Resonance and Two-Port Networks
**Type / marks / difficulty:** MCQ / 1 / Medium
**Family:** `NT-AC-BANDWIDTH-001`

### Question

A series RLC network has resistance $R=20\,\Omega$ and inductance $L=0.1\,\mathrm{H}$. Determine its half-power bandwidth in angular frequency.

### Options

- A. $100\,\mathrm{rad\,s^{-1}}$
- B. $200\,\mathrm{rad\,s^{-1}}$
- C. $500\,\mathrm{rad\,s^{-1}}$
- D. $2000\,\mathrm{rad\,s^{-1}}$

### Declared answer

B

### Canonical solution

For series RLC resonance, the angular-frequency bandwidth is $\Delta\omega=\frac{R}{L}=\frac{20}{0.1}=200\,\mathrm{rad\,s^{-1}}$.
Final answer: B

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-017 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Sinusoidal Steady State
**Type / marks / difficulty:** MSQ / 2 / Hard
**Family:** `NT-AC-PFCORRECTION-001`

### Question

A single-phase impedance load absorbs $P=8\,\mathrm{kW}$ at a lagging power factor of $0.8$. Select every correct statement about this sinusoidal steady-state network; one or more options may be correct.

### Options

- A. The load reactive power is $6\,\mathrm{kVAr}$.
- B. The apparent-power magnitude is $10\,\mathrm{kVA}$.
- C. The load current leads the load voltage.
- D. A $6\,\mathrm{kVAr}$ shunt capacitor would correct the source power factor to unity.

### Declared answer

A, B, D

### Canonical solution

With $\cos\phi=0.8$, $\tan\phi=0.75$. Hence $Q=P\tan\phi=(8)(0.75)=6\,\mathrm{kVAr}$ and $|S|=\frac{P}{\cos\phi}=\frac{8}{0.8}=10\,\mathrm{kVA}$. A lagging load current does not lead its voltage. A $6\,\mathrm{kVAr}$ capacitive shunt cancels the inductive reactive power, so A, B and D are correct.
Final answer: A, B, D

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-018 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Balanced Three-Phase Circuits and Complex Power
**Type / marks / difficulty:** NAT / 2 / Medium
**Family:** `NT-3P-STARPOWER-001`

### Question

A balanced three-phase, star-connected load has per-phase impedance $Z_{\mathrm{ph}}=(8+j6)\,\Omega$ and is supplied at a line-to-line RMS voltage $V_L=400\,\mathrm{V}$. Determine the total real power in kilowatts.

### Declared answer

12.8

### Canonical solution

The phase-voltage magnitude is $V_{\mathrm{ph}}=\frac{400}{\sqrt{3}}\,\mathrm{V}$, the phase-current magnitude is $I_{\mathrm{ph}}=\frac{400/\sqrt{3}}{10}\,\mathrm{A}$, and the load power factor is $\cos\phi=\frac{8}{10}=0.8$. Thus $P=\sqrt{3}V_LI_L\cos\phi=\sqrt{3}(400)\left(\frac{400}{10\sqrt{3}}\right)(0.8)=12800\,\mathrm{W}=12.8\,\mathrm{kW}$.
Final answer: 12.8

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-019 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Resonance and Two-Port Networks
**Type / marks / difficulty:** NAT / 2 / Hard
**Family:** `NT-2P-ZINPUT-001`

### Question

A two-port network has $z_{11}=4\,\Omega$, $z_{12}=z_{21}=2\,\Omega$, and $z_{22}=5\,\Omega$. Port 2 is terminated by a load $Z_L=3\,\Omega$. Determine the input impedance; enter the numerical value in $\Omega$.

### Declared answer

3.5

### Canonical solution

For a $z$-parameter two-port terminated by $Z_L$, the input impedance is $Z_{\mathrm{in}}=z_{11}-\frac{z_{12}z_{21}}{z_{22}+Z_L}$. Therefore $Z_{\mathrm{in}}=4-\frac{(2)(2)}{5+3}=4-0.5=3.5\,\Omega$.
Final answer: 3.5

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---

## TMB-GATE-EE-NT-020 — revision 2

**Route:** Electrical Engineering → Electric Circuits → Balanced Three-Phase Circuits and Complex Power
**Type / marks / difficulty:** MCQ / 2 / Medium
**Family:** `NT-3P-DELTAPOWER-001`

### Question

A balanced three-phase, delta-connected load has branch-impedance magnitude $|Z_{\Delta}|=12\,\Omega$ and lagging phase angle $30^{\circ}$. It is supplied at a line-to-line RMS voltage $V_L=240\,\mathrm{V}$. Determine the approximate total real power.

### Options

- A. $7.20\,\mathrm{kW}$
- B. $12.47\,\mathrm{kW}$
- C. $14.40\,\mathrm{kW}$
- D. $24.94\,\mathrm{kW}$

### Declared answer

B

### Canonical solution

For a delta load, $V_{\mathrm{ph}}=V_L=240\,\mathrm{V}$, so $I_{\mathrm{ph}}=\frac{240}{12}=20\,\mathrm{A}$. The total real power is $P=3V_{\mathrm{ph}}I_{\mathrm{ph}}\cos30^{\circ}=3(240)(20)\cos30^{\circ}=12470.8\,\mathrm{W}\approx12.47\,\mathrm{kW}$.
Final answer: B

### Review state

Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.

---
