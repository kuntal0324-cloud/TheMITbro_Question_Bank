# GATE EE Batch 002 — Human Final QA Packet

Canonical source SHA-256: `23b749225f9128864b1e1545c865ba1d08b8ee706b3faf69e6202099b913db36`
Strict Formatter report SHA-256: `78bab267e0abc034fc0927952b39b0a6328bda0a82d32e1ce877e92c56eaa342`
Strict result: **20 PASS / 0 REVIEW / 0 invalid**
Independent AI recomputation: **20/20 PASS (not a human-review substitute)**
Paper eligible: **0 — promotion remains blocked pending named human signoff**

> **Editing note:** the `☐` and `☑` symbols in this Markdown packet are display-only. Use `output/pdf/GATE_EE_BATCH002_HUMAN_FINAL_QA_MOBILE_FILLABLE.pdf`, save the completed form, then import it with `scripts/import_gate_ee_batch_002_human_qa_pdf.py`.

## Reviewer identity and attestation

- Name: ______________________________
- Role or qualification: ______________________________
- Review date (YYYY-MM-DD): ______________________________
- Required attestation: “I independently reviewed the Batch 002 questions, answers and solutions and approve only the question IDs marked PASS below.”

For every question, independently check the mathematics, declared answer, complete solution, clarity, and originality-conflict risk. Do not copy the AI result as the human decision.

---

## TMB-GATE-EE-NT-001 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Network Elements
**Type / marks / difficulty:** NAT / 1 / Easy

### Question

A 6 microfarad capacitor and a 3 microfarad capacitor are connected in series across an 18 V DC source. Determine the total energy stored by this capacitor network in millijoules.

### Declared answer

0.324

### Independent recomputation evidence

Ceq=2 microfarads; (1/2)Ceq(18)^2=0.324 mJ.

### Canonical solution

The series equivalent capacitance is C_eq=(6 x 3)/(6+3)=2 microfarads. The stored energy is (1/2) C_eq V^2=(1/2)(2 x 10^-6)(18)^2=324 x 10^-6 J=0.324 mJ.
Final answer: 0.324

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-002 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Network Elements
**Type / marks / difficulty:** MCQ / 1 / Medium

### Question

Two coupled inductors in a series-aiding network have L1=4 H, L2=9 H and coefficient of coupling k=0.5. Determine the equivalent inductance.

### Options

- A. 7 H
- B. 13 H
- C. 19 H
- D. 25 H

### Declared answer

C

### Independent recomputation evidence

M=0.5 sqrt(4x9)=3 H; series-aiding Leq=4+9+2M=19 H, option C.

### Canonical solution

The mutual inductance is M=k sqrt(L1 L2)=0.5 sqrt(4 x 9)=3 H. For a series-aiding connection, L_eq=L1+L2+2M=4+9+6=19 H.
Final answer: C

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-003 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Circuit Laws and Analysis
**Type / marks / difficulty:** MCQ / 2 / Hard

### Question

At the input port of a linear network, a 4 ohm resistor is connected from the port to ground. A dependent current source of value 0.5 times the resistor current is also directed from the port to ground. Determine the resistance seen at the port.

### Options

- A. 2 ohm
- B. 8/3 ohm
- C. 4 ohm
- D. 6 ohm

### Declared answer

B

### Independent recomputation evidence

A test voltage v draws v/4+0.5(v/4)=3v/8; v/i=8/3 ohm, option B.

### Canonical solution

Apply a test voltage v at the port. The resistor current is v/4 and the dependent-source current is 0.5(v/4). Hence the total input current is i=(3v/8), so the driving-point resistance is v/i=8/3 ohm.
Final answer: B

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-004 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Network Elements
**Type / marks / difficulty:** MSQ / 1 / Easy

### Question

Select every correct statement about ideal passive network elements under finite, impulse-free excitation; one or more options may be correct.

### Options

- A. The energy stored in a capacitor is (1/2)Cv^2.
- B. The energy stored in an inductor is Li^2.
- C. A capacitor voltage cannot change instantaneously.
- D. An inductor current cannot change instantaneously.

### Declared answer

A, C, D

### Independent recomputation evidence

Ideal stored energies are Cv^2/2 and Li^2/2; capacitor voltage and inductor current cannot jump under finite impulse-free excitation.

### Canonical solution

Capacitor energy is (1/2)Cv^2 and inductor energy is (1/2)Li^2, so option B misses the factor 1/2. With finite impulse-free excitation, capacitor voltage and inductor current cannot change instantaneously. Therefore A, C and D are correct.
Final answer: A, C, D

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-005 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Circuit Laws and Analysis
**Type / marks / difficulty:** NAT / 2 / Medium

### Question

In a resistive network, node v1 is connected to a 12 V voltage source through 3 ohm, to ground through 6 ohm, and to node v2 through 2 ohm. Node v2 is connected to ground through 4 ohm. Using KCL and node-voltage analysis, determine v2 in volts.

### Declared answer

4

### Independent recomputation evidence

KCL gives v1=1.5v2 and 6v1-3v2=24; hence v2=4 V.

### Canonical solution

KCL at v2 gives (v2-v1)/2+v2/4=0, hence v1=1.5v2. KCL at v1 gives (v1-12)/3+v1/6+(v1-v2)/2=0. Multiplying by 6 yields 6v1-3v2=24. Substitution gives 6(1.5v2)-3v2=24, so v2=4 V.
Final answer: 4

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-006 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Circuit Laws and Analysis
**Type / marks / difficulty:** NAT / 2 / Hard

### Question

Two non-reference node voltages satisfy v1-v2=5 V because of an ideal voltage source between them. A 2 ohm branch connects v1 to ground, a 3 ohm branch connects v2 to ground, and a 4 A current source injects current into v2. Using supernode KCL, determine v1 in volts.

### Declared answer

6.8

### Independent recomputation evidence

v1/2+v2/3=4 with v1-v2=5 gives v2=1.8 V and v1=6.8 V.

### Canonical solution

KCL for the supernode is v1/2+v2/3=4. The voltage-source constraint is v1=v2+5. Substituting and multiplying by 6 gives 3(v2+5)+2v2=24, so v2=1.8 V and v1=6.8 V.
Final answer: 6.8

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-007 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Circuit Laws and Analysis
**Type / marks / difficulty:** MCQ / 2 / Medium

### Question

Clockwise mesh currents I1 and I2 in a resistor network satisfy the KVL equations 5I1-2I2=8 and -2I1+4I2=2. Determine the current in their common branch, directed with I1.

### Options

- A. 0.625 A
- B. 1.625 A
- C. 2.250 A
- D. 3.875 A

### Declared answer

A

### Independent recomputation evidence

The two equations give I1=2.25 A and I2=1.625 A; I1-I2=0.625 A, option A.

### Canonical solution

Solving the two mesh-current equations gives I1=36/16=2.25 A and I2=26/16=1.625 A. The common-branch current in the I1 direction is I1-I2=0.625 A.
Final answer: A

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-008 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Circuit Laws and Analysis
**Type / marks / difficulty:** MSQ / 1 / Easy

### Question

Select every correct statement about node-voltage analysis of a connected electrical network; one or more options may be correct.

### Options

- A. One node is selected as the reference node.
- B. An ideal voltage source between two non-reference nodes can be handled using a supernode.
- C. For n nodes, at most n-1 independent KCL node equations are required.
- D. The method cannot be used when dependent sources are present.

### Declared answer

A, B, C

### Independent recomputation evidence

A reference node, a supernode for an inter-node ideal voltage source, and at most n-1 independent KCL equations are valid; dependent sources do not prohibit nodal analysis.

### Canonical solution

Node-voltage analysis selects a reference, uses supernodes for ideal voltage sources between unknown nodes, and requires at most n-1 independent KCL equations. Dependent sources are permitted when their controlling relations are included. Thus A, B and C are correct.
Final answer: A, B, C

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-009 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Network Theorems
**Type / marks / difficulty:** MCQ / 2 / Medium

### Question

An 18 V ideal voltage source feeds a 3 ohm series resistor and an output node; a 6 ohm resistor connects that node to ground. A 4 ohm load is then connected from the output node to ground. Determine the load current using the Thevenin equivalent of the source network.

### Options

- A. 1 A
- B. 2 A
- C. 3 A
- D. 4 A

### Declared answer

B

### Independent recomputation evidence

Vth=18(6/9)=12 V and Rth=3||6=2 ohm; IL=12/(2+4)=2 A, option B.

### Canonical solution

The open-circuit voltage is V_th=18(6/(3+6))=12 V. With the independent source deactivated, R_th=3 parallel 6=2 ohm. Therefore the 4 ohm load current is 12/(2+4)=2 A.
Final answer: B

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-010 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Network Theorems
**Type / marks / difficulty:** MCQ / 1 / Easy

### Question

A Norton network consists of a 3 A current source in parallel with 6 ohm. When a 3 ohm load is connected across the network, determine the load current.

### Options

- A. 0.5 A
- B. 1 A
- C. 2 A
- D. 3 A

### Declared answer

C

### Independent recomputation evidence

Current division gives IL=3[6/(6+3)]=2 A, option C.

### Canonical solution

By current division, the 3 A Norton current splits between 6 ohm and 3 ohm. The load current is 3[6/(6+3)]=2 A.
Final answer: C

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-011 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Network Theorems
**Type / marks / difficulty:** NAT / 2 / Hard

### Question

A sinusoidal network has Thevenin RMS voltage 10 V and Thevenin impedance 3+j4 ohm. A conjugately matched load is connected. Determine the maximum average load power in watts.

### Declared answer

8.333

### Independent recomputation evidence

Conjugate matching gives Pmax=|Vth|^2/(4Rth)=100/12=8.333 W.

### Canonical solution

For conjugate matching, the load impedance is 3-j4 ohm. The maximum average load power is |V_th|^2/(4R_th)=10^2/(4 x 3)=8.333 W.
Final answer: 8.333

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-012 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Network Theorems
**Type / marks / difficulty:** MSQ / 1 / Medium

### Question

Select every correct statement about superposition in a linear electrical network; one or more options may be correct.

### Options

- A. An independent ideal voltage source is replaced by a short circuit when deactivated.
- B. An independent ideal current source is replaced by an open circuit when deactivated.
- C. Dependent sources remain active.
- D. The total power cannot in general be obtained by adding the powers caused by the individual sources.

### Declared answer

A, B, C, D

### Independent recomputation evidence

Independent voltage/current sources become shorts/opens, dependent sources remain, and nonlinear power does not superpose.

### Canonical solution

Superposition deactivates only independent sources: ideal voltage sources become shorts and ideal current sources become opens. Dependent sources remain because they are part of the network model. Voltages and currents superpose, but power is nonlinear, so the separate-source powers do not generally add. All four statements are correct.
Final answer: A, B, C, D

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-013 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Transient Analysis
**Type / marks / difficulty:** NAT / 2 / Medium

### Question

In a first-order RC network, the capacitor voltage is initially 2 V and its steady-state value after switching is 10 V. The resistance is 2 kilo-ohm and the capacitance is 100 microfarad. Determine the capacitor voltage, in volts, one time constant after switching.

### Declared answer

7.057

### Independent recomputation evidence

tau=RC=0.2 s; vC(tau)=10+(2-10)e^-1=7.057 V.

### Canonical solution

The time constant is tau=RC=(2000)(100 x 10^-6)=0.2 s. At t=tau, v_C=10+(2-10)e^-1=10-8/e=7.057 V.
Final answer: 7.057

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-014 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Transient Analysis
**Type / marks / difficulty:** NAT / 2 / Medium

### Question

A 12 V DC source is applied at t=0 to an initially unenergized series RL network with resistance 4 ohm and inductance 2 H. Determine the inductor current in amperes at t=0.5 ln(2) seconds.

### Declared answer

1.5

### Independent recomputation evidence

Iinfinity=3 A, tau=L/R=0.5 s and t/tau=ln2; i=3(1-1/2)=1.5 A.

### Canonical solution

The final current is 12/4=3 A and the time constant is tau=L/R=2/4=0.5 s. Here t/tau=ln(2), so i_L=3[1-e^(-ln(2))]=3(1-1/2)=1.5 A.
Final answer: 1.5

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-015 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Resonance and Two-Port Networks
**Type / marks / difficulty:** MCQ / 1 / Easy

### Question

A series RLC network has inductance 50 mH and capacitance 20 microfarad. Determine its undamped resonant angular frequency.

### Options

- A. 100 rad/s
- B. 500 rad/s
- C. 1000 rad/s
- D. 5000 rad/s

### Declared answer

C

### Independent recomputation evidence

LC=10^-6 and omega0=1/sqrt(LC)=1000 rad/s, option C.

### Canonical solution

The resonant angular frequency is omega_0=1/sqrt(LC). Since LC=(50 x 10^-3)(20 x 10^-6)=10^-6, omega_0=1/10^-3=1000 rad/s.
Final answer: C

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-016 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Resonance and Two-Port Networks
**Type / marks / difficulty:** MCQ / 1 / Medium

### Question

A series RLC network has resistance 20 ohm and inductance 0.1 H. Determine its half-power bandwidth in angular frequency.

### Options

- A. 100 rad/s
- B. 200 rad/s
- C. 500 rad/s
- D. 2000 rad/s

### Declared answer

B

### Independent recomputation evidence

Series-RLC angular bandwidth is R/L=20/0.1=200 rad/s, option B.

### Canonical solution

For a series RLC resonance, the angular-frequency bandwidth is delta_omega=R/L=20/0.1=200 rad/s.
Final answer: B

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-017 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Sinusoidal Steady State
**Type / marks / difficulty:** MSQ / 2 / Hard

### Question

A single-phase impedance load absorbs 8 kW at 0.8 lagging power factor. Select every correct statement about this sinusoidal steady-state network; one or more options may be correct.

### Options

- A. The load reactive power is 6 kvar.
- B. The apparent power magnitude is 10 kVA.
- C. The load current leads the load voltage.
- D. A 6 kvar shunt capacitor would correct the source power factor to unity.

### Declared answer

A, B, D

### Independent recomputation evidence

tan(arccos 0.8)=0.75 gives Q=6 kvar and |S|=10 kVA; the current lags and 6 kvar capacitive compensation reaches unity power factor.

### Canonical solution

With cos(phi)=0.8, tan(phi)=0.75. Hence the reactive power is 8 x 0.75=6 kvar and the apparent-power magnitude is 8/0.8=10 kVA. A lagging load current does not lead its voltage. A 6 kvar capacitive shunt cancels the inductive reactive power, so A, B and D are correct.
Final answer: A, B, D

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-018 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Balanced Three-Phase Circuits and Complex Power
**Type / marks / difficulty:** NAT / 2 / Medium

### Question

A balanced three-phase, star-connected impedance load of 8+j6 ohm per phase is supplied at a line voltage of 400 V RMS. Determine the total real power in kilowatts.

### Declared answer

12.8

### Independent recomputation evidence

|Z|=10 ohm and cos(phi)=0.8; three-phase real power evaluates to 12.8 kW.

### Canonical solution

The phase-voltage magnitude is 400/sqrt(3) V, the phase-current magnitude is [400/sqrt(3)]/10 A, and the load power factor is 8/10. Thus the total real power is sqrt(3)(400)[400/(sqrt(3)10)](0.8)=12800 W=12.8 kW.
Final answer: 12.8

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-019 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Resonance and Two-Port Networks
**Type / marks / difficulty:** NAT / 2 / Hard

### Question

A two-port network has z11=4 ohm, z12=z21=2 ohm and z22=5 ohm. Port 2 is terminated by a 3 ohm load. Determine the input impedance in ohms.

### Declared answer

3.5

### Independent recomputation evidence

Zin=z11-z12z21/(z22+ZL)=4-4/8=3.5 ohm.

### Canonical solution

For a z-parameter two-port terminated by Z_L, the input impedance is Z_in=z11-(z12 z21)/(z22+Z_L). Therefore Z_in=4-(2 x 2)/(5+3)=4-0.5=3.5 ohm.
Final answer: 3.5

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## TMB-GATE-EE-NT-020 — revision 1

**Route:** Electrical Engineering → Electric Circuits → Balanced Three-Phase Circuits and Complex Power
**Type / marks / difficulty:** MCQ / 2 / Medium

### Question

A balanced three-phase, delta-connected impedance load has 12 ohm magnitude and 30 degree lagging phase angle per branch. It is supplied from a 240 V RMS line. Determine the approximate total real power.

### Options

- A. 7.20 kW
- B. 12.47 kW
- C. 14.40 kW
- D. 24.94 kW

### Declared answer

B

### Independent recomputation evidence

Delta phase current is 240/12=20 A; 3(240)(20)cos30=12.47 kW, option B.

### Canonical solution

For a delta load the phase voltage equals the line voltage, so each phase current is 240/12=20 A. The total real power is 3(240)(20)cos(30 degrees)=12470.8 W, approximately 12.47 kW.
Final answer: B

### Human decision fields

| Check | PASS | FAIL |
|---|:---:|:---:|
| Technical correctness | ☐ | ☐ |
| Answer correctness | ☐ | ☐ |
| Solution correctness | ☐ | ☐ |
| Clarity / ambiguity | ☐ | ☐ |
| Originality-conflict check | ☐ | ☐ |

Decision: ☐ PASS  ☐ REVISE  ☐ REJECT
Notes: ______________________________

---

## Final certification procedure

1. Enter reviewer identity, the exact attestation, all five checks, one decision and notes for every question in the companion human-final-QA JSON.
2. Run the batch human-signoff validator.
3. Promote only explicit PASS decisions after that validator succeeds.
4. Re-run every repository validator before corpus admission or paper assembly.
