import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import brentq
import random

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Capital Structure Lab",
    page_icon="🏗️",
    layout="wide"
)

# =========================================================
# HELPERS
# =========================================================

def pct(x, d=4):
    return f"{round(x, d)}%"

def currency(x):
    return f"₹{x:,.2f}"

# =========================================================
# TITLE
# =========================================================

st.title("🏗️ Experiential Learning Lab: Capital Structure")

st.markdown("""
Welcome to the **Capital Structure Learning Platform**.

This app covers:

- Introduction & Overview of Capital Structure
- Net Income (NI) Approach
- Net Operating Income (NOI) Approach
- Traditional Approach
- Modigliani-Miller (MM) — No Taxes
- Modigliani-Miller (MM) — With Corporate Taxes
- Miller Model (Personal Taxes)
- Trade-off Theory
- Pecking Order Theory
- Market Timing Theory
- Agency Theory & Costs
- Signalling Theory
- Financial Distress & Bankruptcy Costs
- EBIT-EPS Analysis & Indifference Point
- Degree of Financial Leverage (DFL)
- Combined / Total Leverage
- Operating Leverage (DOL)
- Capital Structure in Indian Markets
- Determinants of Capital Structure
- Optimal Capital Structure Decision

through:

✅ Interactive calculators  
✅ Real Indian corporate examples  
✅ Step-by-step solvers  
✅ Visual diagrams  
✅ Quiz engine  
✅ Common mistakes  
✅ Formula cheat sheet  
✅ Case-based learning
""")

# =========================================================
# SIDEBAR
# =========================================================

menu = st.sidebar.radio(
    "Choose Module",
    [
        "Introduction",
        # ── TRADITIONAL THEORIES ──────────────────────────
        "Net Income (NI) Approach",
        "Net Operating Income (NOI) Approach",
        "Traditional Approach",
        # ── MM THEORIES ───────────────────────────────────
        "MM — No Taxes (1958)",
        "MM — With Corporate Taxes (1963)",
        "Miller Model (Personal Taxes)",
        # ── MODERN THEORIES ───────────────────────────────
        "Trade-off Theory",
        "Pecking Order Theory",
        "Market Timing Theory",
        "Agency Theory & Costs",
        "Signalling Theory",
        "Financial Distress & Bankruptcy",
        # ── LEVERAGE ANALYSIS ────────────────────────────
        "EBIT-EPS Analysis",
        "Indifference Point",
        "Degree of Financial Leverage (DFL)",
        "Degree of Operating Leverage (DOL)",
        "Combined Leverage (DTL)",
        # ── APPLICATIONS ─────────────────────────────────
        "Capital Structure in India",
        "Determinants of Capital Structure",
        "Optimal Capital Structure Decision",
        # ── TOOLS ────────────────────────────────────────
        "Theory Comparison Dashboard",
        "Step-by-Step Solver",
        "AI Hint System",
        "Quiz Engine",
        "Excel Formula Trainer",
        "Formula Cheat Sheet",
        "Common Student Mistakes",
        "Advanced Quiz Bank",
        "Progress Tracker",
        "Case-Based Learning",
    ]
)

# =========================================================
# INTRODUCTION
# =========================================================

if menu == "Introduction":

    st.header("📘 Introduction to Capital Structure")

    st.markdown("""
## What is Capital Structure?

Capital structure refers to the **mix of long-term financing sources** used by a firm:
- **Debt** (bonds, debentures, loans)
- **Preference shares**
- **Equity** (retained earnings + new equity)

## The Central Question

> Does capital structure affect firm value?
> Is there an **optimal mix** that maximises firm value / minimises WACC?

---

## Capital Structure vs Financial Structure

| | Capital Structure | Financial Structure |
|---|---|---|
| Includes | Long-term debt + Equity | All financing (including current liabilities) |
| Focus | Long-term investment financing | Total asset financing |
| Relevance | Investment and value decisions | Working capital decisions |

---

## Key Approaches
""")

    approaches = pd.DataFrame({
        "Approach": [
            "Net Income (NI) Approach",
            "Net Operating Income (NOI) Approach",
            "Traditional Approach",
            "MM (No Taxes)",
            "MM (With Taxes)",
            "Trade-off Theory",
            "Pecking Order Theory",
        ],
        "Core Position": [
            "Capital structure DOES matter; debt reduces WACC",
            "Capital structure does NOT matter; WACC is constant",
            "Optimal D/E exists before financial risk increases",
            "Capital structure irrelevant (perfect markets)",
            "100% debt optimal (due to tax shield)",
            "Optimal D/E balances tax shield vs distress costs",
            "Firms prefer internal > debt > equity (info asymmetry)",
        ],
        "WACC": [
            "Falls with leverage",
            "Constant regardless of leverage",
            "Falls then rises (U-shaped)",
            "Constant = Ke(unlevered)",
            "Falls continuously",
            "U-shaped — minimum exists",
            "No explicit WACC prediction",
        ]
    })

    st.table(approaches)

    st.info("""
**Indian Context:**
- SEBI guidelines govern debt issuance (NCD, bonds)
- RBI regulates bank lending (a major debt source)
- Tax rate matters significantly for MM theorem application
- Indian firms show pecking order behaviour (prefer internal accruals)
- PSUs have different capital structure constraints vs private firms
""")

# =========================================================
# NET INCOME APPROACH
# =========================================================

elif menu == "Net Income (NI) Approach":

    st.header("📈 Net Income (NI) Approach")

    st.markdown("""
## Core Assumptions & Predictions

**Proposed by: David Durand (1952)**

1. Debt is **always cheaper** than equity (Kd < Ke)
2. Both Kd and Ke remain **constant** regardless of leverage
3. More debt → lower WACC → higher firm value
4. **Optimal structure = 100% debt** (extreme prediction)

## Formula

$$V = \\frac{EBIT - I}{K_e} + D = \\frac{EAT}{K_e} + D$$

Or equivalently:

$$V = \\frac{NOI}{WACC}$$
""")

    col1, col2, col3 = st.columns(3)
    with col1:
        ebit_ni = st.number_input("EBIT (₹)", value=200000.0, key="ni_ebit")
        ke_ni = st.number_input("Ke — Cost of Equity (%)", value=12.0, key="ni_ke")
    with col2:
        debt_ni = st.number_input("Debt (₹)", value=500000.0, key="ni_d")
        kd_ni = st.number_input("Kd — Cost of Debt (%)", value=8.0, key="ni_kd")
    with col3:
        tax_ni = st.number_input("Tax Rate (%)", value=0.0, key="ni_tax",
                                  help="NI Approach typically ignores taxes")

    interest_ni = debt_ni * kd_ni / 100
    eat_ni = (ebit_ni - interest_ni) * (1 - tax_ni/100)
    equity_value_ni = eat_ni / (ke_ni / 100)
    firm_value_ni = equity_value_ni + debt_ni
    wacc_ni = ebit_ni * (1 - tax_ni/100) / firm_value_ni * 100

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Interest", currency(interest_ni))
    with col2:
        st.metric("EAT / Earnings to Equity", currency(eat_ni))
    with col3:
        st.metric("Equity Value (EAT/Ke)", currency(equity_value_ni))
    with col4:
        st.metric("Firm Value (E + D)", currency(firm_value_ni))

    st.success(f"**WACC = {pct(wacc_ni)}**")

    # Show WACC declining with debt
    st.subheader("📊 NI Approach: WACC Falls as Debt Increases")

    debt_range = np.arange(0, 1000001, 50000)
    wacc_ni_range = []
    fv_ni_range = []

    for d in debt_range:
        int_d = d * kd_ni / 100
        eat_d = max(ebit_ni - int_d, 0) * (1 - tax_ni/100)
        e_val = eat_d / (ke_ni/100) if ke_ni > 0 else 0
        v_ni = e_val + d
        w_ni = ebit_ni*(1-tax_ni/100)/v_ni*100 if v_ni > 0 else 0
        wacc_ni_range.append(w_ni)
        fv_ni_range.append(v_ni)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=debt_range/1000, y=wacc_ni_range,
                             name="WACC", line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=debt_range/1000, y=[ke_ni]*len(debt_range),
                             name="Ke (constant)", line=dict(color='blue', dash='dash')))
    fig.add_trace(go.Scatter(x=debt_range/1000, y=[kd_ni]*len(debt_range),
                             name="Kd (constant)", line=dict(color='green', dash='dot')))
    fig.update_layout(title="NI Approach: WACC Continuously Falls",
                      xaxis_title="Debt (₹ Thousands)",
                      yaxis_title="Cost / Return (%)")
    st.plotly_chart(fig, use_container_width=True)

    st.warning("""
⚠️ **Criticism:** The NI approach is unrealistic because:
- Ke does NOT remain constant as risk increases with leverage
- 100% debt is practically impossible (lenders would refuse)
- Ignores financial distress and bankruptcy costs
""")

# =========================================================
# NET OPERATING INCOME APPROACH
# =========================================================

elif menu == "Net Operating Income (NOI) Approach":

    st.header("📊 Net Operating Income (NOI) Approach")

    st.markdown("""
## Core Assumptions & Predictions

**Also proposed by: David Durand (1952)**

1. **Overall capitalisation rate (Ko / WACC) remains CONSTANT** regardless of leverage
2. Ke rises exactly to offset the benefit of cheaper debt
3. Capital structure is **irrelevant** — firm value is determined by NOI alone
4. **Firm value = NOI / Ko** (constant)

This is essentially the **pre-cursor to MM Theorem (no taxes)**.

## Formula

$$V = \\frac{NOI}{K_o}$$

$$K_e = K_o + (K_o - K_d) \\times \\frac{D}{E}$$
""")

    col1, col2, col3 = st.columns(3)
    with col1:
        noi = st.number_input("NOI / EBIT (₹)", value=200000.0, key="noi_noi")
        ko = st.number_input("Overall Capitalisation Rate Ko (%)", value=12.0)
    with col2:
        kd_noi = st.number_input("Cost of Debt Kd (%)", value=8.0, key="noi_kd")
        debt_noi = st.number_input("Debt (₹)", value=400000.0, key="noi_d")
    with col3:
        tax_noi = st.number_input("Tax Rate (%)", value=0.0, key="noi_tax")

    firm_value_noi = noi / (ko / 100)
    equity_noi = firm_value_noi - debt_noi
    interest_noi = debt_noi * kd_noi / 100
    eat_noi = noi - interest_noi
    ke_noi = eat_noi / equity_noi * 100 if equity_noi > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Firm Value V = NOI/Ko", currency(firm_value_noi))
    with col2:
        st.metric("Equity Value E = V - D", currency(equity_noi))
    with col3:
        st.metric("EAT = NOI - Interest", currency(eat_noi))
    with col4:
        st.metric("Ke = EAT/E (implied)", pct(ke_noi))

    st.success(f"**WACC = Ko = {pct(ko)} (constant regardless of leverage)**")

    # Show Ke rising, WACC constant
    st.subheader("📈 NOI Approach: Ke Rises, WACC Stays Constant")

    debt_range_noi = np.arange(0, firm_value_noi, firm_value_noi/20)
    ke_noi_range = []
    for d in debt_range_noi:
        e = firm_value_noi - d
        int_d = d * kd_noi/100
        eat_d = noi - int_d
        ke_d = eat_d/e*100 if e > 0 else 0
        ke_noi_range.append(ke_d)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=debt_range_noi/1000, y=ke_noi_range,
                             name="Ke (rising)", line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=debt_range_noi/1000, y=[ko]*len(debt_range_noi),
                             name="WACC (constant = Ko)", line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=debt_range_noi/1000, y=[kd_noi]*len(debt_range_noi),
                             name="Kd (constant)", line=dict(color='green', dash='dot')))
    fig.update_layout(title="NOI Approach: WACC Constant, Ke Rises with Leverage",
                      xaxis_title="Debt (₹ Thousands)", yaxis_title="Rate (%)")
    st.plotly_chart(fig, use_container_width=True)

    st.info("""
**Key insight:** In the NOI approach, as leverage increases, Ke rises exactly enough
to keep WACC constant. This is the same prediction as MM (no taxes).
""")

# =========================================================
# TRADITIONAL APPROACH
# =========================================================

elif menu == "Traditional Approach":

    st.header("🏛️ Traditional Approach")

    st.markdown("""
## Core Prediction

**Proposed by: Ezra Solomon**

The Traditional approach argues that an **optimal capital structure EXISTS** —
a middle ground between the NI and NOI extremes.

### Three Stages:

| Stage | D/E Level | Effect |
|---|---|---|
| **Stage 1** | Low leverage | WACC falls — debt benefit > risk increase |
| **Stage 2** | Moderate leverage | WACC at minimum — OPTIMAL zone |
| **Stage 3** | High leverage | WACC rises — distress risk dominates |

### Assumptions:
- Kd remains constant at low leverage, then rises at high leverage
- Ke rises moderately at first, then sharply at high leverage
- WACC is **U-shaped** — minimum exists at optimal D/E
""")

    col1, col2, col3 = st.columns(3)
    with col1:
        noi_trad = st.number_input("NOI / EBIT (₹)", value=200000.0, key="trad_noi")
        ke_base_trad = st.number_input("Ke at zero debt (%)", value=12.0)
    with col2:
        kd_base_trad = st.number_input("Kd at low leverage (%)", value=8.0)
    with col3:
        tax_trad = st.number_input("Tax Rate (%)", value=0.0, key="trad_tax")

    # Simulate traditional approach
    de_range = np.arange(0, 2.1, 0.1)
    ke_trad = []
    kd_trad = []
    wacc_trad = []

    for de in de_range:
        # Ke rises slowly then steeply
        ke = ke_base_trad + de * 1.5 + max(0, (de - 1.0) * 5)
        ke_trad.append(ke)
        # Kd constant then rises
        kd = kd_base_trad + max(0, (de - 0.8) * 3)
        kd_trad.append(kd)

        wd = de / (1 + de)
        we = 1 / (1 + de)
        wacc = wd * kd * (1 - tax_trad/100) + we * ke
        wacc_trad.append(wacc)

    optimal_idx = np.argmin(wacc_trad)
    optimal_de = de_range[optimal_idx]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=de_range, y=wacc_trad, name="WACC",
                             line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=de_range, y=ke_trad, name="Ke",
                             line=dict(color='blue', dash='dash')))
    fig.add_trace(go.Scatter(x=de_range, y=[kd*(1-tax_trad/100) for kd in kd_trad],
                             name="Kd (after-tax)", line=dict(color='green', dash='dot')))
    fig.add_vline(x=optimal_de, line_dash="dash", line_color="purple",
                  annotation_text=f"Optimal D/E = {round(optimal_de,1)}")
    fig.update_layout(title="Traditional Approach: U-Shaped WACC",
                      xaxis_title="D/E Ratio", yaxis_title="Rate (%)")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Optimal D/E Ratio", round(optimal_de, 1))
    with col2:
        st.metric("Minimum WACC", pct(min(wacc_trad)))

    st.info("""
**Traditional approach is the basis for practical capital structure decisions.**
Most CFOs in practice follow this approach — seek the D/E ratio that minimises WACC,
recognising that both very low and very high leverage are suboptimal.
""")

# =========================================================
# MM — NO TAXES
# =========================================================

elif menu == "MM — No Taxes (1958)":

    st.header("🎓 Modigliani-Miller — No Taxes (1958)")

    st.markdown("""
## The Irrelevance Proposition

> **In perfect capital markets without taxes, the value of a firm is independent
> of its capital structure.**

### MM Proposition I (No Taxes)
$$V_L = V_U$$

### MM Proposition II (No Taxes)
$$K_e^L = K_e^U + (K_e^U - K_d) \\times \\frac{D}{E}$$

WACC remains **constant = Ke(unlevered)** regardless of debt.

### Key Assumptions (Perfect Market)
""")

    assumptions = [
        "No corporate or personal taxes",
        "No transaction costs or flotation costs",
        "No bankruptcy or financial distress costs",
        "Perfect information — symmetric between managers and investors",
        "Investors can borrow at same rate as firms (homemade leverage)",
        "All firms in same risk class have same business risk",
        "Debt is risk-free (at low leverage levels)",
    ]
    for a in assumptions:
        st.markdown(f"- {a}")

    st.subheader("🔢 Interactive Calculator")

    col1, col2, col3 = st.columns(3)
    with col1:
        ke_u_mm = st.number_input("Ke (Unlevered / all-equity) %", value=12.0)
        vu_mm = st.number_input("VU — Unlevered Firm Value (₹)", value=1000000.0)
    with col2:
        kd_mm = st.number_input("Cost of Debt Kd %", value=8.0, key="mm1_kd")
        debt_mm = st.number_input("Debt D (₹)", value=400000.0, key="mm1_d")
    with col3:
        st.markdown("**Results:**")

    vl_mm = vu_mm  # No taxes: VL = VU
    equity_mm = vl_mm - debt_mm
    de_mm = debt_mm / equity_mm if equity_mm > 0 else 0
    ke_l_mm = ke_u_mm + (ke_u_mm - kd_mm) * de_mm
    wd = debt_mm / vl_mm
    we = equity_mm / vl_mm
    wacc_mm1 = wd * kd_mm + we * ke_l_mm

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("VL = VU", currency(vl_mm))
    with col2:
        st.metric("Ke (Levered)", pct(ke_l_mm))
    with col3:
        st.metric("WACC", pct(wacc_mm1))
    with col4:
        st.metric("WACC = Ke(U)?", "✅ Yes" if abs(wacc_mm1 - ke_u_mm) < 0.01 else "❌ Check")

    st.success(f"WACC = {pct(wacc_mm1)} = Ke(Unlevered) = {pct(ke_u_mm)} — Capital structure is IRRELEVANT!")

    # Show WACC constant, Ke rising
    de_vals = np.arange(0, 2.0, 0.05)
    ke_l_vals = [ke_u_mm + (ke_u_mm - kd_mm) * de for de in de_vals]
    wacc_vals = [(de/(1+de))*kd_mm + (1/(1+de))*ke_l for de, ke_l in zip(de_vals, ke_l_vals)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=de_vals, y=ke_l_vals, name="Ke (rising)",
                             line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=de_vals, y=wacc_vals, name="WACC (constant)",
                             line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=de_vals, y=[kd_mm]*len(de_vals), name="Kd",
                             line=dict(color='green', dash='dash')))
    fig.update_layout(title="MM (No Taxes): WACC Constant as D/E Increases",
                      xaxis_title="D/E Ratio", yaxis_title="Rate (%)")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔄 Arbitrage Proof (Homemade Leverage)")
    st.info("""
MM proved irrelevance through **arbitrage**:
If VL ≠ VU, investors can replicate any capital structure through personal borrowing
(homemade leverage) at no cost → prices equalise → VL = VU always.

**Example:** If levered firm is overpriced, investors:
1. Sell shares in levered firm
2. Borrow personally (same rate as firm)
3. Buy shares in unlevered firm
4. Earn same return at lower price → arbitrage profit → prices converge
""")

# =========================================================
# MM — WITH TAXES
# =========================================================

elif menu == "MM — With Corporate Taxes (1963)":

    st.header("🏛️ Modigliani-Miller — With Corporate Taxes (1963)")

    st.markdown("""
## The Tax Shield Effect

When corporate taxes are introduced, **interest is tax-deductible** but **dividends are not**.
This creates a **permanent advantage** for debt financing.

### MM Proposition I (With Taxes)

$$V_L = V_U + t \\times D$$

**Tax Shield = t × D** (for permanent debt)

### MM Proposition II (With Taxes)

$$K_e^L = K_e^U + (K_e^U - K_d)(1-t) \\times \\frac{D}{E}$$

WACC **falls continuously** as debt increases.
""")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        vu_mt = st.number_input("VU (₹)", value=1000000.0, key="mt_vu")
    with col2:
        debt_mt = st.number_input("Debt D (₹)", value=400000.0, key="mt_d")
    with col3:
        tax_mt = st.number_input("Tax Rate t (%)", value=30.0, key="mt_tax")
    with col4:
        kd_mt = st.number_input("Kd (%)", value=8.0, key="mt_kd")

    ke_u_mt = st.number_input("Ke (Unlevered) %", value=12.0, key="mt_keu")

    ts_mt = (tax_mt / 100) * debt_mt
    vl_mt = vu_mt + ts_mt
    equity_mt = vl_mt - debt_mt

    de_mt = debt_mt / equity_mt if equity_mt > 0 else 0
    ke_l_mt = ke_u_mt + (ke_u_mt - kd_mt) * (1 - tax_mt/100) * de_mt
    wd_mt = debt_mt / vl_mt
    we_mt = equity_mt / vl_mt
    wacc_mt = wd_mt * kd_mt * (1 - tax_mt/100) + we_mt * ke_l_mt

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tax Shield (t×D)", currency(ts_mt))
    with col2:
        st.metric("VL = VU + tD", currency(vl_mt))
    with col3:
        st.metric("Ke (Levered)", pct(ke_l_mt))
    with col4:
        st.metric("WACC", pct(wacc_mt))

    st.success(f"VL = {currency(vu_mt)} + {currency(ts_mt)} = **{currency(vl_mt)}**")
    st.info(f"WACC = {pct(wacc_mt)} < Ke(Unlevered) = {pct(ke_u_mt)} — Debt reduces WACC via tax shield")

    # WACC declining
    de_range_mt = np.arange(0, 2.0, 0.05)
    ke_l_mt_range = [ke_u_mt + (ke_u_mt-kd_mt)*(1-tax_mt/100)*de for de in de_range_mt]
    wacc_mt_range = [(de/(1+de))*kd_mt*(1-tax_mt/100)+(1/(1+de))*ke_l
                     for de, ke_l in zip(de_range_mt, ke_l_mt_range)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=de_range_mt, y=wacc_mt_range, name="WACC (with taxes)",
                             line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=de_range_mt, y=[ke_u_mt]*len(de_range_mt),
                             name="WACC (no taxes — flat)", line=dict(color='gray', dash='dash')))
    fig.add_trace(go.Scatter(x=de_range_mt, y=ke_l_mt_range, name="Ke",
                             line=dict(color='blue', dash='dot')))
    fig.update_layout(title="MM With Taxes: WACC Falls Continuously",
                      xaxis_title="D/E Ratio", yaxis_title="Rate (%)")
    st.plotly_chart(fig, use_container_width=True)

    st.warning("""
**MM implication with taxes: 100% debt is optimal** — which is unrealistic.
This leads to the **Trade-off Theory** which adds financial distress costs.
""")

# =========================================================
# MILLER MODEL
# =========================================================

elif menu == "Miller Model (Personal Taxes)":

    st.header("🔄 Miller Model — Personal Taxes (1977)")

    st.markdown("""
## Adding Personal Taxes

Miller (1977) extended MM to include **personal taxes** on:
- **Interest income** (taxed at personal rate Td)
- **Equity income** (dividends + capital gains, taxed at Te)

## Miller's Formula

$$V_L = V_U + \\left[1 - \\frac{(1-T_c)(1-T_e)}{(1-T_d)}\\right] \\times D$$

Where:
- **Tc** = Corporate tax rate
- **Td** = Personal tax rate on debt income (interest)
- **Te** = Personal tax rate on equity income (dividends/capital gains)
""")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        tc = st.number_input("Corporate Tax Rate Tc (%)", value=30.0)
    with col2:
        td = st.number_input("Personal Tax Rate on Debt Income Td (%)", value=25.0)
    with col3:
        te = st.number_input("Personal Tax Rate on Equity Income Te (%)", value=10.0)
    with col4:
        d_mil = st.number_input("Debt (₹)", value=500000.0)

    vu_mil = st.number_input("VU — Unlevered Firm Value (₹)", value=1000000.0)

    leverage_gain = 1 - ((1 - tc/100) * (1 - te/100)) / (1 - td/100)
    ts_miller = leverage_gain * d_mil
    vl_miller = vu_mil + ts_miller

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Leverage Gain Factor", round(leverage_gain, 4))
    with col2:
        st.metric("Effective Tax Shield", currency(ts_miller))
    with col3:
        st.metric("VL (Miller)", currency(vl_miller))

    # Compare with MM (corporate taxes only)
    ts_mm_only = (tc/100) * d_mil
    vl_mm_only = vu_mil + ts_mm_only

    comparison = pd.DataFrame({
        "Model": ["MM (No Taxes)", "MM (Corporate Tax Only)", "Miller (All Taxes)"],
        "Tax Shield": [currency(0), currency(ts_mm_only), currency(ts_miller)],
        "VL": [currency(vu_mil), currency(vl_mm_only), currency(vl_miller)],
        "Implication": [
            "100% equity = 100% debt (irrelevant)",
            "100% debt optimal",
            f"Tax shield = {round(leverage_gain*100,2)}% of debt benefit"
        ]
    })
    st.table(comparison)

    st.info("""
**Miller's key insight:**
When personal taxes are high (especially on interest income), the tax advantage of debt
at the corporate level may be partially or fully offset at the personal level.

**Special case:** If (1-Tc)(1-Te) = (1-Td) → VL = VU (no gain from leverage — back to MM no-tax)
""")

    if abs(leverage_gain) < 0.02:
        st.success("✅ Miller equilibrium: Personal taxes fully offset corporate tax shield — capital structure irrelevant!")
    elif leverage_gain > 0:
        st.info(f"Debt still beneficial but less so than MM predicts. Net gain = {round(leverage_gain*100,2)}% of debt.")
    else:
        st.warning("Debt is actually VALUE-DESTROYING when personal taxes on interest are very high.")

# =========================================================
# TRADE-OFF THEORY
# =========================================================

elif menu == "Trade-off Theory":

    st.header("⚖️ Trade-off Theory")

    st.markdown("""
## Core Concept

The optimal capital structure **balances**:

$$V_L = V_U + PV(\\text{Tax Shield}) - PV(\\text{Financial Distress Costs})$$

At the optimal point:
**Marginal tax benefit of debt = Marginal cost of financial distress**

## Two Types of Financial Distress Costs
""")

    col1, col2 = st.columns(2)
    with col1:
        st.info("""
**Direct Costs**
- Legal and administrative fees in bankruptcy
- Typically 2–4% of firm value
- Accountants, lawyers, court costs
- Examples: Kingfisher Airlines collapse
        """)
    with col2:
        st.warning("""
**Indirect Costs**
- Lost sales (customers distrust)
- Loss of key employees
- Inability to invest in positive NPV projects
- Higher supplier prices (demand prepayment)
- Often 10–20% of firm value
        """)

    st.subheader("📊 Trade-off Theory — Interactive Model")

    col1, col2, col3 = st.columns(3)
    with col1:
        vu_to = st.number_input("VU (₹ Cr)", value=100.0, key="to_vu")
        max_ts = st.number_input("Max Possible Tax Shield (₹ Cr)", value=30.0)
    with col2:
        distress_onset = st.slider("Debt ratio where distress starts", 0.3, 0.8, 0.5)
        distress_severity = st.slider("Severity of distress costs", 1.0, 10.0, 3.0)

    d_ratio = np.arange(0, 1.0, 0.01)
    ts_pv = [max_ts * (1 - np.exp(-3*d)) for d in d_ratio]
    distress_pv = [distress_severity * np.exp(5*(d - distress_onset)) if d > distress_onset else 0
                   for d in d_ratio]
    firm_vals = [vu_to + ts - dc for ts, dc in zip(ts_pv, distress_pv)]

    optimal_idx = np.argmax(firm_vals)
    optimal_dr = d_ratio[optimal_idx]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d_ratio, y=firm_vals, name="VL (Trade-off)",
                             line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=d_ratio, y=[vu_to + ts for ts in ts_pv],
                             name="VU + Tax Shield (MM)", line=dict(color='green', dash='dash')))
    fig.add_trace(go.Scatter(x=d_ratio, y=[vu_to]*len(d_ratio),
                             name="VU (No debt)", line=dict(color='gray', dash='dot')))
    fig.add_vline(x=optimal_dr, line_dash="dash", line_color="red",
                  annotation_text=f"Optimal D/V = {round(optimal_dr*100,0):.0f}%")
    fig.update_layout(title="Trade-off Theory: Optimal Capital Structure",
                      xaxis_title="Debt Ratio (D/V)", yaxis_title="Firm Value (₹ Crore)")
    st.plotly_chart(fig, use_container_width=True)

    st.metric("Optimal Debt Ratio (D/V)", f"{round(optimal_dr*100,1)}%")
    st.metric("Maximum Firm Value", f"₹{round(max(firm_vals),2)} Cr")

    st.subheader("Determinants of Optimal D/E under Trade-off Theory")

    det_df = pd.DataFrame({
        "Factor": ["Tax Rate", "Asset Tangibility", "Profitability", "Business Risk",
                   "Firm Size", "Growth Options"],
        "Effect on Optimal Debt": ["↑", "↑", "↑", "↓", "↑", "↓"],
        "Reason": [
            "Higher tax rate → larger tax shield → more debt optimal",
            "Tangible assets can be pledged → lower distress cost",
            "More profit → more tax to shield → use more debt",
            "Higher business risk → distress more likely → less debt",
            "Larger firms → more diversified → lower distress probability",
            "Growth options lost in distress → avoid high debt"
        ]
    })
    st.table(det_df)

# =========================================================
# PECKING ORDER THEORY
# =========================================================

elif menu == "Pecking Order Theory":

    st.header("🐦 Pecking Order Theory")

    st.markdown("""
## Core Concept (Myers & Majluf, 1984)

Due to **information asymmetry** between managers and investors,
firms follow a **pecking order** of financing:

$$\\text{Internal Funds} \\succ \\text{Debt} \\succ \\text{New Equity}$$

## Why This Order?

1. **Internal funds** — no information problem, no issuance costs, cheapest
2. **Debt** — reveals less information than equity, investors understand debt
3. **New equity** — sends negative signal (managers issue equity when overvalued)

## Myers-Majluf (1984) Result

When firms issue equity, the market interprets it as a **signal that managers
believe the firm is overvalued** → stock price falls on equity issuance announcement.

> **Evidence:** Average stock price drop of 2–3% on equity issue announcement in Indian markets.
""")

    st.subheader("📊 Pecking Order Hierarchy")

    hierarchy = pd.DataFrame({
        "Order": ["1st (Most Preferred)", "2nd", "3rd (Least Preferred)"],
        "Source": ["Internal Funds (Retained Earnings)", "External Debt (Bonds/Loans)", "New Equity Issue"],
        "Why Preferred": [
            "No info asymmetry, no issuance cost, no signal",
            "Debt signals confidence (firm can service it)",
            "Signals overvaluation — market penalises"
        ],
        "Cost": ["Lowest", "Moderate", "Highest (including signalling cost)"],
        "Signal to Market": ["Neutral", "Positive (confidence)", "Negative (overvaluation)"]
    })
    st.table(hierarchy)

    st.subheader("📈 Pecking Order — Financing Deficit Model")

    st.markdown("""
$$\\text{Financing Deficit} = \\text{Dividends} + \\text{Capex} + \\Delta WC - \\text{Operating CF}$$

**When deficit exists:** Firms first use internal reserves, then issue debt.
**When surplus exists:** Firms repay debt, build up internal reserves.
""")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        dividends = st.number_input("Dividends Paid (₹ Cr)", value=20.0)
    with col2:
        capex = st.number_input("Capital Expenditure (₹ Cr)", value=80.0)
    with col3:
        delta_wc = st.number_input("Increase in Working Capital (₹ Cr)", value=10.0)
    with col4:
        ocf = st.number_input("Operating Cash Flow (₹ Cr)", value=50.0)

    deficit = dividends + capex + delta_wc - ocf

    if deficit > 0:
        st.warning(f"**Financing Deficit = ₹{round(deficit,2)} Cr**")
        st.markdown("**Pecking Order says:** Use internal reserves first, then issue debt.")
    else:
        st.success(f"**Financing Surplus = ₹{round(abs(deficit),2)} Cr**")
        st.markdown("**Pecking Order says:** Repay debt, then accumulate cash reserves.")

    st.subheader("⚠️ Empirical Evidence")
    evidence = [
        "Large profitable firms (TCS, Infosys) use little debt — high internal generation",
        "Firms prefer debt over equity when external funds are needed",
        "IPO/FPO announcements often cause stock price dip (-2% to -4%)",
        "Firms issue equity only when overvalued or distressed",
        "Indian IT firms: nearly zero debt (high FCF, little need for external funds)",
    ]
    for e in evidence:
        st.markdown(f"- {e}")

# =========================================================
# MARKET TIMING THEORY
# =========================================================

elif menu == "Market Timing Theory":

    st.header("⏰ Market Timing Theory")

    st.markdown("""
## Core Concept (Baker & Wurgler, 2002)

Firms **time the market** when making capital structure decisions:
- Issue **equity when market price is HIGH** (stock seems overvalued)
- Issue **debt when equity prices are LOW** (avoid dilution)

## Formula: Market-to-Book Ratio

$$M/B = \\frac{\\text{Market Value of Equity}}{\\text{Book Value of Equity}}$$

When M/B is high → firms issue equity (capital is cheap)
When M/B is low → firms avoid equity, use debt

## Key Findings (Baker & Wurgler, 2002)

> Capital structure is the **cumulative outcome of past market timing decisions** —
> not driven by any target optimal structure.

Firms with historically high M/B ratios tend to have **lower leverage today**
(because they issued equity when they were overvalued).
""")

    st.subheader("🔢 Market Timing Signal Calculator")

    col1, col2 = st.columns(2)
    with col1:
        market_cap = st.number_input("Current Market Cap (₹ Cr)", value=5000.0)
        book_equity = st.number_input("Book Value of Equity (₹ Cr)", value=2000.0)
    with col2:
        hist_avg_mb = st.number_input("Historical Average M/B", value=2.0)

    mb = market_cap / book_equity if book_equity > 0 else 0

    st.metric("Current M/B Ratio", round(mb, 2))

    if mb > hist_avg_mb * 1.2:
        st.success(f"✅ M/B ({round(mb,2)}) significantly above historical average ({hist_avg_mb}) — **GOOD TIME TO ISSUE EQUITY**")
    elif mb < hist_avg_mb * 0.8:
        st.error(f"❌ M/B ({round(mb,2)}) significantly below historical average ({hist_avg_mb}) — **AVOID EQUITY ISSUE; USE DEBT**")
    else:
        st.info(f"M/B near historical average — timing signal is neutral")

    st.info("""
**Criticism of Market Timing Theory:**
- Capital structure becomes path-dependent (no optimal target)
- Requires managers to accurately identify market mispricing
- Conflicts with efficient market hypothesis
- Still, empirically, firms DO time equity issuances with high M/B periods
""")

# =========================================================
# AGENCY THEORY
# =========================================================

elif menu == "Agency Theory & Costs":

    st.header("🤝 Agency Theory & Costs")

    st.markdown("""
## Agency Problem in Capital Structure

**Jensen & Meckling (1976)** identified that capital structure affects:
1. **Owner-Manager conflicts** (equity agency costs)
2. **Shareholder-Creditor conflicts** (debt agency costs)
""")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Equity Agency Costs")
        st.info("""
**Problem:** Managers may not act in shareholders' best interest.

**Perquisite consumption** — managers enjoy excess perks
**Underinvestment** — managers avoid risky +NPV projects
**Overinvestment** — managers build empires beyond optimal

**How debt HELPS:**
- Debt reduces free cash flow available for wasteful spending
- Debt payments impose discipline (Jensen's "control hypothesis")
- Managers with skin in the game (equity stakes) align incentives
- Debt threat of bankruptcy motivates efficiency
        """)

    with col2:
        st.subheader("Debt Agency Costs")
        st.warning("""
**Problem:** Equity holders may expropriate wealth from debt holders.

**Asset substitution** — shift to riskier projects after debt issuance
**Underinvestment** — refuse good projects if gains go to creditors
**Milking the firm** — pay excessive dividends before bankruptcy

**How creditors RESPOND:**
- Restrictive covenants (debt covenants)
- Higher interest rates to compensate for risk
- Shorter maturity, collateral requirements
- Monitoring and reporting requirements
        """)

    st.subheader("Net Agency Cost and Optimal Structure")

    st.markdown("""
$$\\text{Total Agency Cost} = \\text{Equity Agency Cost} + \\text{Debt Agency Cost}$$

**Optimal capital structure minimises total agency cost.**

At zero debt: equity agency costs are high (managerial discretion is maximum)
At 100% debt: debt agency costs are high (asset substitution etc.)
**Middle ground** minimises total agency cost.
""")

    # Visualise agency costs
    d_ratio_a = np.arange(0.01, 0.99, 0.01)
    equity_agency = [10 / d for d in d_ratio_a]  # falls as debt increases
    debt_agency = [5 * d**2 * 20 for d in d_ratio_a]  # rises with debt
    total_agency = [ea + da for ea, da in zip(equity_agency, debt_agency)]

    # Normalise for visualisation
    eq_a_norm = [min(ea, 30) for ea in equity_agency]
    tot_norm = [ea + da for ea, da in zip(eq_a_norm, debt_agency)]

    opt_a_idx = np.argmin(tot_norm)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d_ratio_a, y=eq_a_norm, name="Equity Agency Costs",
                             line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=d_ratio_a, y=debt_agency, name="Debt Agency Costs",
                             line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=d_ratio_a, y=tot_norm, name="Total Agency Costs",
                             line=dict(color='purple', width=2)))
    fig.add_vline(x=d_ratio_a[opt_a_idx], line_dash="dash",
                  annotation_text="Optimal D/V")
    fig.update_layout(title="Agency Theory: Optimal D/E Minimises Total Agency Costs",
                      xaxis_title="Debt Ratio (D/V)", yaxis_title="Agency Costs")
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# SIGNALLING THEORY
# =========================================================

elif menu == "Signalling Theory":

    st.header("📡 Signalling Theory")

    st.markdown("""
## Information Asymmetry and Signals

Managers have **inside information** about firm value that investors do not.
Capital structure decisions **signal** this private information.

## Key Signals

| Action | Signal to Market | Market Reaction |
|---|---|---|
| **Increase Debt** | Managers confident in future cash flows to service debt | ✅ Stock price rises |
| **Issue New Equity** | Managers think stock is overvalued | ❌ Stock price falls |
| **Debt Repayment** | Firm is profitable enough to repay | ✅ Positive |
| **Dividend Increase** | Strong future earnings expected | ✅ Positive |
| **Leveraged Buyout (LBO)** | Strong confidence in future performance | ✅ Very positive |

## Ross Signalling Model (1977)

In equilibrium:
- **Good firms** choose high leverage (signal quality — can afford debt service)
- **Bad firms** cannot afford to mimic (bankruptcy risk too high)
- This separation equilibrium allows investors to distinguish firm quality

## Empirical Evidence

""")

    signals = pd.DataFrame({
        "Event": [
            "Equity issuance announcement",
            "Debt issuance announcement",
            "Increase in dividends",
            "Share buyback",
            "Debt-for-equity swap",
        ],
        "Typical Market Reaction": [
            "−2% to −4% (Overvaluation signal)",
            "+0.5% to +1.5% (Confidence signal)",
            "+3% to +5% (Earnings confidence)",
            "+5% to +10% (Undervaluation signal)",
            "+8% to +12% (Strong confidence signal)",
        ],
        "Indian Evidence": [
            "Negative drift around FPO announcements",
            "Bond issue seen as positive for PSUs",
            "High dividend firms outperform in India",
            "Buybacks common in IT sector (TCS, Infosys)",
            "Seen in restructuring scenarios"
        ]
    })
    st.table(signals)

# =========================================================
# FINANCIAL DISTRESS
# =========================================================

elif menu == "Financial Distress & Bankruptcy":

    st.header("⚠️ Financial Distress & Bankruptcy Costs")

    st.markdown("""
## What is Financial Distress?

A firm is in **financial distress** when it cannot meet its debt obligations
or is likely to default — even if not yet legally bankrupt.

## The Financial Distress Spectrum
""")

    spectrum = pd.DataFrame({
        "Stage": [
            "1. Liquidity Pressure",
            "2. Financial Distress",
            "3. Technical Default",
            "4. Default",
            "5. Bankruptcy / Insolvency"
        ],
        "Description": [
            "Cash flow tight; difficulty meeting short-term obligations",
            "Breach of covenants; renegotiating with creditors",
            "Miss interest payment; violation of debt covenants",
            "Formal default; creditors can accelerate payments",
            "Legal proceeding (IBC in India); assets liquidated or restructured"
        ],
        "Indian Examples": [
            "DHFL (pre-crisis), Jet Airways (early stage)",
            "IL&FS, Yes Bank (pre-bailout)",
            "Kingfisher Airlines",
            "Essar Steel, Lanco Infratech",
            "Videocon Industries, Reliance Communications"
        ]
    })
    st.table(spectrum)

    st.subheader("🔢 Altman Z-Score (Bankruptcy Predictor)")

    st.markdown("""
$$Z = 1.2X_1 + 1.4X_2 + 3.3X_3 + 0.6X_4 + 1.0X_5$$

Where:
- X1 = Working Capital / Total Assets
- X2 = Retained Earnings / Total Assets
- X3 = EBIT / Total Assets
- X4 = Market Value of Equity / Book Value of Total Debt
- X5 = Sales / Total Assets
""")

    col1, col2, col3 = st.columns(3)
    with col1:
        wc = st.number_input("Working Capital (₹ Cr)", value=50.0)
        ta = st.number_input("Total Assets (₹ Cr)", value=500.0)
        re = st.number_input("Retained Earnings (₹ Cr)", value=80.0)
    with col2:
        ebit_z = st.number_input("EBIT (₹ Cr)", value=60.0)
        mve = st.number_input("Market Value of Equity (₹ Cr)", value=300.0)
        td_z = st.number_input("Book Value of Total Debt (₹ Cr)", value=200.0)
    with col3:
        sales = st.number_input("Net Sales (₹ Cr)", value=400.0)

    if ta > 0 and td_z > 0:
        x1 = wc / ta
        x2 = re / ta
        x3 = ebit_z / ta
        x4 = mve / td_z
        x5 = sales / ta
        z_score = 1.2*x1 + 1.4*x2 + 3.3*x3 + 0.6*x4 + 1.0*x5

        st.metric("Altman Z-Score", round(z_score, 4))

        if z_score > 2.99:
            st.success(f"✅ Z = {round(z_score,2)} > 2.99 — **SAFE ZONE** (Low bankruptcy risk)")
        elif z_score > 1.81:
            st.warning(f"⚠️ Z = {round(z_score,2)} — **GREY ZONE** (1.81-2.99) — Monitor carefully")
        else:
            st.error(f"❌ Z = {round(z_score,2)} < 1.81 — **DISTRESS ZONE** (High bankruptcy risk)")

    st.subheader("India: Insolvency & Bankruptcy Code (IBC) 2016")
    st.info("""
**IBC 2016** revolutionised bankruptcy proceedings in India:
- Time-bound resolution: 180 days (extendable to 270 days)
- **NCLT** (National Company Law Tribunal) adjudicates
- Committee of Creditors (CoC) drives resolution
- Resolution Professional (RP) manages firm during process
- Major cases: Essar Steel, Bhushan Steel, Videocon, DHFL
- Resolution rate improving but still challenged by delays
""")

# =========================================================
# EBIT-EPS ANALYSIS
# =========================================================

elif menu == "EBIT-EPS Analysis":

    st.header("📊 EBIT-EPS Analysis")

    st.markdown("""
## Purpose

EBIT-EPS analysis compares **Earnings per Share (EPS) under different capital structures**
at various EBIT levels to identify:
1. Which plan gives higher EPS at given EBIT
2. The **indifference point** (EBIT at which EPS is equal)

## Formula

$$EPS = \\frac{(EBIT - I)(1-t) - PD}{N}$$

Where:
- **I** = Interest charges
- **t** = Tax rate
- **PD** = Preference dividend
- **N** = Number of equity shares
""")

    st.subheader("🔢 Multi-Plan EBIT-EPS Calculator")

    n_plans = int(st.number_input("Number of Capital Structure Plans", value=3, min_value=2, max_value=4, step=1))
    tax_ebit = st.number_input("Tax Rate (%)", value=30.0, key="ebit_tax")

    plans = []
    cols = st.columns(n_plans)

    default_plans = [
        ("Plan A (All Equity)", 0, 0, 100000),
        ("Plan B (50% Debt)", 50000, 0, 50000),
        ("Plan C (75% Debt)", 100000, 5000, 25000),
        ("Plan D (Pref + Debt)", 60000, 10000, 40000),
    ]

    for i in range(n_plans):
        with cols[i]:
            plan_name = st.text_input("Plan Name", value=default_plans[i][0], key=f"ep_name_{i}")
            interest = st.number_input("Interest (₹)", value=float(default_plans[i][1]), key=f"ep_int_{i}")
            pref_div = st.number_input("Preference Dividend (₹)", value=float(default_plans[i][2]), key=f"ep_pd_{i}")
            shares = st.number_input("No. of Equity Shares", value=float(default_plans[i][3]), key=f"ep_sh_{i}")
            plans.append({"name": plan_name, "interest": interest, "pref_div": pref_div, "shares": shares})

    ebit_range = np.arange(0, 400001, 5000)
    fig = go.Figure()

    colors = ['blue', 'red', 'green', 'orange']
    for i, p in enumerate(plans):
        eps_vals = []
        for ebit in ebit_range:
            eat = max((ebit - p["interest"]) * (1 - tax_ebit/100) - p["pref_div"], 0)
            eps = eat / p["shares"] if p["shares"] > 0 else 0
            eps_vals.append(eps)
        fig.add_trace(go.Scatter(x=ebit_range/1000, y=eps_vals,
                                 name=p["name"], line=dict(color=colors[i], width=2)))

    fig.add_hline(y=0, line_color="black", line_width=0.5)
    fig.update_layout(title="EBIT-EPS Analysis",
                      xaxis_title="EBIT (₹ Thousands)",
                      yaxis_title="EPS (₹)")
    st.plotly_chart(fig, use_container_width=True)

    # EPS table at specific EBIT
    ebit_check = st.number_input("Calculate EPS at EBIT = ₹", value=150000.0)

    eps_table = []
    for p in plans:
        eat = max((ebit_check - p["interest"]) * (1 - tax_ebit/100) - p["pref_div"], 0)
        eps_val = eat / p["shares"] if p["shares"] > 0 else 0
        eps_table.append({"Plan": p["name"], "Interest (₹)": p["interest"],
                           "EAT (₹)": round(eat, 2), "Shares": p["shares"],
                           "EPS (₹)": round(eps_val, 4)})

    df_eps = pd.DataFrame(eps_table)
    st.dataframe(df_eps, use_container_width=True)

    best = df_eps.loc[df_eps["EPS (₹)"].idxmax(), "Plan"]
    st.success(f"At EBIT = ₹{ebit_check:,.0f}, **{best}** gives the highest EPS.")

# =========================================================
# INDIFFERENCE POINT
# =========================================================

elif menu == "Indifference Point":

    st.header("🎯 Indifference Point (EPS Equality)")

    st.markdown("""
## What is the Indifference Point?

The **indifference EBIT** is the level of EBIT at which EPS is **equal** under two capital structure plans.

- **Below indifference EBIT:** Equity plan gives higher EPS (less leverage is better)
- **Above indifference EBIT:** Levered plan gives higher EPS (leverage amplifies EPS)

## Formula (Two Plans)

$$\\frac{(EBIT - I_1)(1-t) - PD_1}{N_1} = \\frac{(EBIT - I_2)(1-t) - PD_2}{N_2}$$

Cross-multiply and solve for EBIT.
""")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Plan A**")
        i1 = st.number_input("Interest I₁ (₹)", value=0.0, key="ind_i1")
        pd1 = st.number_input("Preference Dividend PD₁ (₹)", value=0.0, key="ind_pd1")
        n1 = st.number_input("No. of Shares N₁", value=100000.0, key="ind_n1")

    with col2:
        st.markdown("**Plan B**")
        i2 = st.number_input("Interest I₂ (₹)", value=50000.0, key="ind_i2")
        pd2 = st.number_input("Preference Dividend PD₂ (₹)", value=0.0, key="ind_pd2")
        n2 = st.number_input("No. of Shares N₂", value=50000.0, key="ind_n2")

    tax_ind = st.number_input("Tax Rate (%)", value=30.0, key="ind_tax")

    t = tax_ind / 100
    # (EBIT - I1)(1-t) - PD1) / N1 = (EBIT - I2)(1-t) - PD2) / N2
    # N2 * [(EBIT - I1)(1-t) - PD1] = N1 * [(EBIT - I2)(1-t) - PD2]
    # N2*(EBIT-I1)*(1-t) - N2*PD1 = N1*(EBIT-I2)*(1-t) - N1*PD2
    # EBIT*(1-t)*(N2-N1) = N2*(1-t)*I1 - N1*(1-t)*I2 - N1*PD2 + N2*PD1

    try:
        lhs_coeff = (1-t)*(n2 - n1)
        rhs = n2*(1-t)*i1 - n1*(1-t)*i2 - n1*pd2 + n2*pd1
        if abs(lhs_coeff) > 0:
            indiff_ebit = rhs / lhs_coeff
        else:
            indiff_ebit = None
    except:
        indiff_ebit = None

    if indiff_ebit is not None and indiff_ebit > 0:
        st.success(f"**Indifference EBIT = ₹{indiff_ebit:,.2f}**")

        eps_a = (indiff_ebit - i1)*(1-t)/n1
        eps_b = (indiff_ebit - i2)*(1-t)/n2
        st.metric("EPS at Indifference (both plans)", f"₹{round(eps_a,4)}")

        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**If EBIT < ₹{indiff_ebit:,.0f}:** Plan A (less debt) gives higher EPS")
        with col2:
            st.success(f"**If EBIT > ₹{indiff_ebit:,.0f}:** Plan B (more debt) gives higher EPS")

        st.latex(f"Indifference\\ EBIT = ₹{round(indiff_ebit,2)}")
    else:
        st.error("Could not compute indifference point. Check inputs (N1 ≠ N2 required).")

    st.subheader("📐 Step-by-Step Formula")
    st.latex(r"\frac{(EBIT - I_1)(1-t) - PD_1}{N_1} = \frac{(EBIT - I_2)(1-t) - PD_2}{N_2}")
    st.markdown("Cross-multiply and solve for EBIT.")

# =========================================================
# DEGREE OF FINANCIAL LEVERAGE
# =========================================================

elif menu == "Degree of Financial Leverage (DFL)":

    st.header("📐 Degree of Financial Leverage (DFL)")

    st.markdown("""
## Formulas

$$DFL = \\frac{EBIT}{EBIT - I - \\frac{PD}{(1-t)}}$$

For simple case (no preference dividend):

$$DFL = \\frac{EBIT}{EBIT - I} = \\frac{\\% \\Delta EPS}{\\% \\Delta EBIT}$$

DFL measures how sensitive EPS is to changes in EBIT.
- **DFL = 1:** No financial leverage (all-equity)
- **DFL > 1:** Financial leverage magnifies EPS changes
- **DFL = ∞:** Firm is at breakeven (EBIT = Interest)
""")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ebit_dfl = st.number_input("EBIT (₹)", value=200000.0, key="dfl_ebit")
    with col2:
        interest_dfl = st.number_input("Interest I (₹)", value=50000.0, key="dfl_int")
    with col3:
        pref_div_dfl = st.number_input("Preference Dividend PD (₹)", value=0.0, key="dfl_pd")
    with col4:
        tax_dfl = st.number_input("Tax Rate (%)", value=30.0, key="dfl_tax")

    denom = ebit_dfl - interest_dfl - (pref_div_dfl / (1 - tax_dfl/100) if tax_dfl < 100 else 0)

    if denom > 0:
        dfl = ebit_dfl / denom
        st.success(f"**DFL = {round(dfl, 4)}**")
        st.info(f"A 10% increase in EBIT will lead to a **{round(dfl*10, 2)}% increase in EPS**")

        # DFL at different EBIT levels
        ebit_range_dfl = np.arange(interest_dfl + 10000, ebit_dfl*3, ebit_dfl/20)
        dfl_vals = [e/(e - interest_dfl - (pref_div_dfl/(1-tax_dfl/100) if tax_dfl < 100 else 0))
                    for e in ebit_range_dfl if e > interest_dfl]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ebit_range_dfl[:len(dfl_vals)]/1000, y=dfl_vals,
                                 mode='lines', name='DFL', line=dict(color='red', width=2)))
        fig.add_vline(x=ebit_dfl/1000, line_dash="dash", line_color="blue",
                      annotation_text=f"Current EBIT (DFL={round(dfl,2)})")
        fig.update_layout(title="DFL at Different EBIT Levels",
                          xaxis_title="EBIT (₹ Thousands)",
                          yaxis_title="Degree of Financial Leverage (DFL)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("EBIT ≤ Interest + Adjusted PD — firm cannot cover fixed charges!")

    st.subheader("DFL Interpretation Table")

    dfl_table = pd.DataFrame({
        "DFL Value": ["DFL = 1.0", "1.0 < DFL < 2.0", "DFL = 2.0", "DFL > 2.0", "DFL → ∞"],
        "Interpretation": [
            "No financial leverage (all equity)",
            "Low-moderate financial risk",
            "EPS changes 2× as fast as EBIT",
            "High financial risk",
            "Company at financial breakeven — extreme risk"
        ]
    })
    st.table(dfl_table)

# =========================================================
# DEGREE OF OPERATING LEVERAGE
# =========================================================

elif menu == "Degree of Operating Leverage (DOL)":

    st.header("⚙️ Degree of Operating Leverage (DOL)")

    st.markdown("""
## Formula

$$DOL = \\frac{\\text{Contribution}}{EBIT} = \\frac{\\text{Sales} - \\text{Variable Costs}}{EBIT}$$

$$DOL = \\frac{\\% \\Delta EBIT}{\\% \\Delta \\text{Sales}}$$

DOL measures how sensitive EBIT is to changes in Sales.
High fixed costs → High DOL → More operating risk.
""")

    col1, col2, col3 = st.columns(3)
    with col1:
        sales_dol = st.number_input("Sales Revenue (₹)", value=1000000.0)
        vc_dol = st.number_input("Variable Costs (₹)", value=600000.0)
    with col2:
        fc_dol = st.number_input("Fixed Costs (₹)", value=200000.0)
    with col3:
        st.markdown("**Derived:**")

    contribution = sales_dol - vc_dol
    ebit_dol_calc = contribution - fc_dol
    dol = contribution / ebit_dol_calc if ebit_dol_calc > 0 else float('inf')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Contribution", currency(contribution))
    with col2:
        st.metric("EBIT", currency(ebit_dol_calc))
    with col3:
        st.metric("DOL", round(dol, 4))

    if ebit_dol_calc > 0:
        st.success(f"**DOL = {round(dol, 4)}** — A 10% rise in sales → {round(dol*10,2)}% rise in EBIT")
    else:
        st.error("EBIT ≤ 0 — Company is operating at a loss (DOL not meaningful)")

    # Break-even analysis
    st.subheader("📊 Break-even Analysis")

    if vc_dol < sales_dol:
        vc_ratio = vc_dol / sales_dol
        pv_ratio = 1 - vc_ratio  # P/V ratio (contribution margin ratio)
        bep_sales = fc_dol / pv_ratio
        bep_units_note = "BEP Sales = Fixed Cost / P/V Ratio"

        col1, col2 = st.columns(2)
        with col1:
            st.metric("P/V Ratio (Contribution Margin %)", pct(pv_ratio*100))
            st.metric("Break-even Sales", currency(bep_sales))
        with col2:
            margin_of_safety = (sales_dol - bep_sales) / sales_dol * 100
            st.metric("Margin of Safety", pct(margin_of_safety))
            st.metric("MOS (₹)", currency(sales_dol - bep_sales))

# =========================================================
# COMBINED LEVERAGE
# =========================================================

elif menu == "Combined Leverage (DTL)":

    st.header("🔗 Combined / Total Leverage (DTL)")

    st.markdown("""
## Degree of Total Leverage (DTL)

$$DTL = DOL \\times DFL$$

$$DTL = \\frac{\\text{Contribution}}{EBIT - I - \\frac{PD}{(1-t)}}$$

$$DTL = \\frac{\\% \\Delta EPS}{\\% \\Delta \\text{Sales}}$$

DTL measures the **combined effect of operating and financial leverage** on EPS
for a given change in sales.
""")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Operating Data**")
        sales_dtl = st.number_input("Sales (₹)", value=1000000.0, key="dtl_s")
        vc_dtl = st.number_input("Variable Costs (₹)", value=600000.0, key="dtl_vc")
        fc_dtl = st.number_input("Fixed Costs (₹)", value=200000.0, key="dtl_fc")

    with col2:
        st.markdown("**Financial Data**")
        interest_dtl = st.number_input("Interest (₹)", value=50000.0, key="dtl_int")
        pd_dtl = st.number_input("Preference Dividend (₹)", value=0.0, key="dtl_pd")
        tax_dtl = st.number_input("Tax Rate (%)", value=30.0, key="dtl_tax")

    contrib_dtl = sales_dtl - vc_dtl
    ebit_dtl = contrib_dtl - fc_dtl
    adjusted_pd = pd_dtl / (1 - tax_dtl/100) if tax_dtl < 100 else 0
    denom_dtl = ebit_dtl - interest_dtl - adjusted_pd

    if ebit_dtl > 0:
        dol_dtl = contrib_dtl / ebit_dtl
    else:
        dol_dtl = float('inf')

    if denom_dtl > 0:
        dfl_dtl = ebit_dtl / denom_dtl
        dtl = dol_dtl * dfl_dtl
    else:
        dfl_dtl = float('inf')
        dtl = float('inf')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("DOL", round(dol_dtl, 4))
    with col2:
        st.metric("DFL", round(dfl_dtl, 4))
    with col3:
        st.metric("DTL = DOL × DFL", round(dtl, 4) if dtl != float('inf') else "∞")

    if dtl != float('inf'):
        st.success(f"**DTL = {round(dtl,4)}** — A 10% rise in sales leads to a **{round(dtl*10,2)}% rise in EPS**")

    st.subheader("Leverage Summary")

    lev_df = pd.DataFrame({
        "Leverage Type": ["Operating Leverage (DOL)", "Financial Leverage (DFL)", "Total Leverage (DTL)"],
        "Measures": ["Sensitivity of EBIT to Sales", "Sensitivity of EPS to EBIT", "Sensitivity of EPS to Sales"],
        "Formula": ["Contribution/EBIT", "EBIT/(EBIT-I-PD/(1-t))", "DOL × DFL"],
        "Driver": ["Fixed Operating Costs", "Fixed Financial Charges (Interest + PD)", "Both combined"],
        "Value": [round(dol_dtl,4), round(dfl_dtl,4), round(dtl,4) if dtl!=float('inf') else "∞"]
    })
    st.table(lev_df)

# =========================================================
# CAPITAL STRUCTURE IN INDIA
# =========================================================

elif menu == "Capital Structure in India":

    st.header("🇮🇳 Capital Structure in Indian Markets")

    st.markdown("""
## Key Features of Indian Capital Structure

### 1. Regulatory Framework
- **SEBI** regulates equity issuance (IPO, FPO, Rights Issue)
- **RBI** regulates bank borrowings and external commercial borrowings (ECB)
- **Companies Act 2013** governs debt covenants and share issuance
- **IBC 2016** governs bankruptcy and insolvency

### 2. Sources of Finance — Indian Context
""")

    sources = pd.DataFrame({
        "Source": [
            "Bank Loans (Term Loans)",
            "Non-Convertible Debentures (NCDs)",
            "External Commercial Borrowings (ECB)",
            "Commercial Paper (CP)",
            "Initial Public Offering (IPO)",
            "Rights Issue",
            "Qualified Institutional Placement (QIP)",
            "Internal Accruals (Retained Earnings)",
            "Venture Capital / Private Equity",
        ],
        "Type": ["Debt","Debt","Debt","Debt","Equity","Equity","Equity","Equity","Equity"],
        "Key Feature": [
            "Most common; secured; interest tax-deductible",
            "Bond market instrument; listed on NSE/BSE",
            "Foreign borrowing; forex risk; LIBOR/SOFR based",
            "Short-term debt (<1 yr); working capital",
            "First public equity sale; expensive process",
            "Additional equity to existing shareholders",
            "Fast equity raise from institutional investors",
            "Cheapest; zero flotation cost; most preferred",
            "Dilutes equity but no debt obligation"
        ]
    })
    st.table(sources)

    st.subheader("📊 Sector-wise Capital Structure Patterns")

    sector_data = pd.DataFrame({
        "Sector": ["IT Services", "FMCG", "Banking", "Infrastructure", "Metals & Mining",
                   "Pharmaceuticals", "Telecom", "Real Estate"],
        "Typical D/E Ratio": ["0.0-0.2", "0.0-0.5", "10-15x (leverage)", "2-5x", "0.5-1.5x",
                               "0.2-0.8x", "2-4x", "2-5x"],
        "Primary Debt Source": ["Minimal", "Minimal", "Deposits", "Bonds/Loans", "Bonds",
                                 "Loans", "Bonds/Loans", "Loans"],
        "Capital Structure Logic": [
            "High FCF generation; no need for debt",
            "Asset-light; high margins; use minimal debt",
            "Leverage is business model (deposits fund loans)",
            "Capital-intensive; long gestation; needs debt",
            "Commodity cycle risk; moderate leverage",
            "R&D intensive; moderate leverage",
            "High capex (spectrum, towers); high debt",
            "Project-based; high land + construction debt"
        ]
    })
    st.table(sector_data)

    st.subheader("Recent Trends in Indian Capital Structure")

    trends = [
        "**Deleveraging trend (2019-2024):** Many Indian corporates reduced debt post-IL&FS crisis",
        "**Rise of green bonds:** Renewable energy firms (Adani Green, ReNew) using green debt",
        "**QIP popularity:** Listed firms prefer QIP over rights issue (faster, less disclosure)",
        "**AT1 bonds:** Banks use Additional Tier-1 bonds (controversial after Yes Bank write-off)",
        "**ECB surge:** Indian firms borrowing cheaply in US dollars (now costlier with strong USD)",
        "**Promoter pledging:** High pledging is a capital structure risk signal in India",
    ]
    for t in trends:
        st.markdown(f"- {t}")

# =========================================================
# DETERMINANTS
# =========================================================

elif menu == "Determinants of Capital Structure":

    st.header("🔍 Determinants of Capital Structure")

    st.subheader("Key Factors and Their Effect on Debt")

    det_df = pd.DataFrame({
        "Factor": [
            "Asset Tangibility",
            "Firm Profitability",
            "Business Risk (Operating Risk)",
            "Tax Rate",
            "Firm Size",
            "Growth Opportunities",
            "Financial Flexibility",
            "Market Timing (M/B ratio)",
            "Industry Norms",
            "Management Attitude",
        ],
        "Effect on Debt Ratio": [
            "↑ More tangible assets → More debt (better collateral)",
            "↓ More profitable → Use internal funds first (Pecking Order)",
            "↓ Higher business risk → Less financial risk desired",
            "↑ Higher tax → Larger tax shield → More debt optimal",
            "↑ Larger firms → Easier debt access, lower distress risk",
            "↓ High growth → Avoid debt (protect investment options)",
            "↓ Need flexibility → Maintain debt capacity for future",
            "↓ High M/B → Issue equity instead of debt",
            "→ Firms gravitate toward industry average D/E",
            "Varies by risk appetite of management team",
        ],
        "Trade-off Theory": ["✅","❌","✅","✅","✅","✅","❌","❌","—","—"],
        "Pecking Order": ["—","✅","—","—","—","—","✅","—","—","—"],
        "Indian Evidence": [
            "Infra/metal firms borrow more (physical assets)",
            "IT/FMCG generate high internal cash — low debt",
            "Cyclical sectors (steel, power) use less debt",
            "30% tax rate makes debt shields valuable",
            "Reliance, Tata group have easier bond market access",
            "Startups avoid debt; mature firms borrow more",
            "Firms maintain credit lines for M&A flexibility",
            "FPOs clustered at market peaks",
            "IT sector uniformly low-leverage",
            "Promoter conservatism drives Indian family businesses"
        ]
    })

    st.dataframe(det_df, use_container_width=True)

    st.subheader("🔢 Capital Structure Score Calculator")

    st.markdown("Rate each factor to get a recommended debt level:")

    col1, col2 = st.columns(2)
    with col1:
        tang = st.slider("Asset Tangibility (1=low, 5=high)", 1, 5, 3)
        profit = st.slider("Profitability (1=low, 5=high)", 1, 5, 3)
        biz_risk = st.slider("Business Risk (1=low, 5=high)", 1, 5, 3)
        tax_r = st.slider("Effective Tax Rate (1=low, 5=high)", 1, 5, 3)
    with col2:
        size = st.slider("Firm Size (1=small, 5=large)", 1, 5, 3)
        growth = st.slider("Growth Opportunities (1=low, 5=high)", 1, 5, 3)
        mb = st.slider("Market/Book Ratio (1=low, 5=high)", 1, 5, 3)

    # Score — higher = more debt
    debt_score = (tang + profit*(-0.5) + biz_risk*(-1) + tax_r + size + growth*(-1) + mb*(-0.5)) / 7 * 100

    debt_pct = max(10, min(70, 30 + debt_score * 0.5))

    st.metric("Recommended Debt Ratio (D/V)", f"{round(debt_pct,1)}%")

    if debt_pct < 25:
        st.info("Low debt recommended — high growth, high risk, or highly profitable firm")
    elif debt_pct < 45:
        st.success("Moderate debt — balanced capital structure")
    else:
        st.warning("Higher debt may be appropriate — tangible assets, tax benefit, stable cash flows")

# =========================================================
# OPTIMAL CAPITAL STRUCTURE DECISION
# =========================================================

elif menu == "Optimal Capital Structure Decision":

    st.header("🎯 Optimal Capital Structure Decision Framework")

    st.markdown("""
## Synthesising All Theories

No single theory explains capital structure completely.
The optimal decision integrates insights from multiple frameworks:
""")

    st.subheader("The Decision Matrix")

    decision_matrix = pd.DataFrame({
        "Theory": ["Trade-off", "Pecking Order", "Market Timing",
                   "Agency", "Signalling", "MM (Practical)"],
        "Key Insight": [
            "Optimal D/E where tax benefit = distress cost",
            "Use internal funds first; debt second; equity last",
            "Issue equity when stock is overvalued",
            "Debt disciplines managers; but too much creates creditor conflict",
            "Debt signals confidence in future cash flows",
            "Capital structure irrelevant in perfect markets — imperfections drive decisions"
        ],
        "Practical Takeaway": [
            "Set a target D/E based on firm characteristics",
            "Build cash reserves; avoid unnecessary equity dilution",
            "Monitor M/B ratio; time equity issuance carefully",
            "Use debt to reduce free cash flow waste",
            "Consider market signal before changing structure",
            "Focus on operational efficiency first"
        ]
    })
    st.table(decision_matrix)

    st.subheader("🔢 WACC Minimisation Check")

    st.markdown("Input different D/E scenarios and find the minimum WACC:")

    col1, col2 = st.columns(2)
    with col1:
        noi_opt = st.number_input("NOI (₹ Cr)", value=100.0)
        tax_opt = st.number_input("Tax Rate (%)", value=30.0, key="opt_tax")
        ke_base_opt = st.number_input("Ke at zero debt (%)", value=12.0)
        kd_base_opt = st.number_input("Kd at low leverage (%)", value=8.0)

    scenarios = []
    de_options = [0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]

    for de in de_options:
        ke_s = ke_base_opt + de*2 + max(0, (de-1)*4)
        kd_s = kd_base_opt + max(0, (de-0.8)*2)
        kd_at = kd_s * (1 - tax_opt/100)
        wd = de/(1+de)
        we = 1/(1+de)
        wacc_s = wd*kd_at + we*ke_s
        v_s = noi_opt*(1-tax_opt/100)/wacc_s*100

        scenarios.append({
            "D/E Ratio": de,
            "Ke (%)": round(ke_s,2),
            "Kd after-tax (%)": round(kd_at,2),
            "D/V (%)": round(wd*100,1),
            "WACC (%)": round(wacc_s,4),
            "Firm Value (₹ Cr)": round(v_s,2)
        })

    df_opt = pd.DataFrame(scenarios)
    optimal_row = df_opt.loc[df_opt["WACC (%)"].idxmin()]

    st.dataframe(df_opt, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"**Optimal D/E = {optimal_row['D/E Ratio']}** (Minimum WACC = {pct(optimal_row['WACC (%)'])})")
    with col2:
        st.success(f"**Maximum Firm Value = ₹{optimal_row['Firm Value (₹ Cr)']} Cr**")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_opt["D/E Ratio"], y=df_opt["WACC (%)"],
                             mode='lines+markers', name='WACC', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df_opt["D/E Ratio"], y=df_opt["Firm Value (₹ Cr)"],
                             mode='lines+markers', name='Firm Value (₹ Cr)',
                             yaxis='y2', line=dict(color='blue')))
    fig.update_layout(
        title="Optimal Capital Structure: WACC vs Firm Value",
        xaxis_title="D/E Ratio",
        yaxis=dict(title="WACC (%)"),
        yaxis2=dict(title="Firm Value (₹ Cr)", overlaying='y', side='right')
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# THEORY COMPARISON DASHBOARD
# =========================================================

elif menu == "Theory Comparison Dashboard":

    st.header("📊 Theory Comparison Dashboard")

    theories = pd.DataFrame({
        "Theory": ["NI Approach", "NOI Approach", "Traditional",
                   "MM (No Tax)", "MM (With Tax)", "Trade-off", "Pecking Order"],
        "WACC": ["Falls continuously", "Constant", "U-shaped (minimum exists)",
                 "Constant = Ke(U)", "Falls continuously", "U-shaped", "No specific prediction"],
        "Firm Value": ["Rises with debt", "Constant", "Rises then falls",
                       "Constant", "Rises continuously", "Rises then falls", "Varies"],
        "Optimal D/E": ["100% debt", "Irrelevant", "Exists (moderate)",
                        "Irrelevant", "100% debt", "Moderate (firm-specific)", "Firm-specific"],
        "Key Driver": ["Cheaper debt always", "Ke rises perfectly", "Ke rises after threshold",
                       "Arbitrage/perfect markets", "Tax shield on interest", "Tax shield vs distress cost",
                       "Information asymmetry"],
        "Realism": ["❌ Unrealistic", "❌ Too extreme", "✅ Practical",
                    "❌ Perfect market assumption", "⚠️ Partial (ignores distress)",
                    "✅ Most comprehensive", "✅ Strong empirical support"]
    })

    st.dataframe(theories, use_container_width=True)

    st.subheader("📈 WACC Behaviour Comparison")

    de_range_comp = np.arange(0, 2.0, 0.1)
    ke_u_c = 12.0; kd_c = 8.0; tax_c = 30.0

    # NI: WACC falls (Ke constant at 12%, Kd constant at 8%)
    wacc_ni_c = [(de/(1+de))*kd_c + (1/(1+de))*ke_u_c for de in de_range_comp]

    # NOI: WACC constant
    wacc_noi_c = [ke_u_c] * len(de_range_comp)

    # MM with tax: WACC falls (Ke rises with tax adjustment)
    ke_mm_tax = [ke_u_c + (ke_u_c-kd_c)*(1-tax_c/100)*de for de in de_range_comp]
    wacc_mm_tax_c = [(de/(1+de))*kd_c*(1-tax_c/100)+(1/(1+de))*ke for de, ke in zip(de_range_comp, ke_mm_tax)]

    # Traditional: U-shaped
    wacc_trad_c = [ke_u_c + (de*(-2) + de**2*3) for de in de_range_comp]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=de_range_comp, y=wacc_ni_c, name="NI Approach (falling)",
                             line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=de_range_comp, y=wacc_noi_c, name="NOI / MM No Tax (constant)",
                             line=dict(color='gray', dash='dot')))
    fig.add_trace(go.Scatter(x=de_range_comp, y=wacc_mm_tax_c, name="MM With Tax (falling)",
                             line=dict(color='green', dash='dash')))
    fig.add_trace(go.Scatter(x=de_range_comp, y=wacc_trad_c, name="Traditional (U-shaped)",
                             line=dict(color='blue', width=2)))
    fig.update_layout(title="WACC Behaviour Across Different Theories",
                      xaxis_title="D/E Ratio", yaxis_title="WACC (%)")
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# STEP-BY-STEP SOLVER
# =========================================================

elif menu == "Step-by-Step Solver":

    st.header("🧠 Step-by-Step Solver")

    problem = st.selectbox("Choose Problem", [
        "MM (No Taxes) — Find VL and Ke(Levered)",
        "MM (With Taxes) — Find VL and Tax Shield",
        "DFL Calculation",
        "Indifference EBIT",
        "EPS Calculation",
        "DOL Calculation",
    ])

    if problem == "MM (No Taxes) — Find VL and Ke(Levered)":
        vu = st.number_input("VU (₹)", value=1000000.0)
        keu = st.number_input("Ke(U) %", value=12.0)
        kd = st.number_input("Kd %", value=8.0)
        d = st.number_input("Debt D (₹)", value=400000.0)

        st.write("**Step 1: VL = VU (No taxes)**")
        st.latex(f"V_L = V_U = {currency(vu)}")

        st.write("**Step 2: Equity E = VL - D**")
        e = vu - d
        st.latex(f"E = {currency(vu)} - {currency(d)} = {currency(e)}")

        st.write("**Step 3: Ke(Levered)**")
        de = d/e if e > 0 else 0
        ke_l = keu + (keu-kd)*de
        st.latex(f"K_e^L = {keu} + ({keu}-{kd}) \\times {round(de,4)} = {round(ke_l,4)}\\%")
        st.success(f"Ke(Levered) = {round(ke_l,4)}%")

    elif problem == "MM (With Taxes) — Find VL and Tax Shield":
        vu = st.number_input("VU (₹)", value=1000000.0, key="sbs_mt_vu")
        d = st.number_input("Debt D (₹)", value=400000.0, key="sbs_mt_d")
        tax = st.number_input("Tax Rate t (%)", value=30.0, key="sbs_mt_t")

        st.write("**Step 1: Tax Shield = t × D**")
        ts = (tax/100)*d
        st.latex(f"TS = {tax/100} \\times {currency(d)} = {currency(ts)}")

        st.write("**Step 2: VL = VU + t×D**")
        vl = vu + ts
        st.latex(f"V_L = {currency(vu)} + {currency(ts)} = {currency(vl)}")
        st.success(f"VL = {currency(vl)}")

    elif problem == "DFL Calculation":
        ebit = st.number_input("EBIT (₹)", value=200000.0)
        interest = st.number_input("Interest I (₹)", value=50000.0)

        st.write("**Step 1: Formula**")
        st.latex(r"DFL = \frac{EBIT}{EBIT - I}")

        dfl = ebit / (ebit - interest)
        st.write("**Step 2: Substitute**")
        st.latex(f"DFL = \\frac{{{ebit}}}{{{ebit} - {interest}}} = \\frac{{{ebit}}}{{{ebit-interest}}} = {round(dfl,4)}")
        st.success(f"DFL = {round(dfl,4)}")

    elif problem == "Indifference EBIT":
        i1 = st.number_input("Interest I₁ (Plan A) (₹)", value=0.0, key="sbs_ind_i1")
        n1 = st.number_input("Shares N₁ (Plan A)", value=100000.0)
        i2 = st.number_input("Interest I₂ (Plan B) (₹)", value=60000.0, key="sbs_ind_i2")
        n2 = st.number_input("Shares N₂ (Plan B)", value=50000.0)
        tax = st.number_input("Tax Rate (%)", value=30.0, key="sbs_ind_t")

        t = tax/100
        st.write("**Step 1: Set EPS equal**")
        st.latex(r"\frac{(EBIT-I_1)(1-t)}{N_1} = \frac{(EBIT-I_2)(1-t)}{N_2}")

        lhs_c = (1-t)*(n2-n1)
        rhs_c = n2*(1-t)*i1 - n1*(1-t)*i2

        st.write("**Step 2: Cross multiply and solve**")
        if abs(lhs_c) > 0:
            indiff = rhs_c / lhs_c
            st.latex(f"EBIT \\times {round((1-t)*(n2-n1),2)} = {round(rhs_c,2)}")
            st.success(f"Indifference EBIT = ₹{indiff:,.2f}")

    elif problem == "EPS Calculation":
        ebit = st.number_input("EBIT (₹)", value=200000.0, key="sbs_eps_e")
        interest = st.number_input("Interest (₹)", value=50000.0, key="sbs_eps_i")
        pd_v = st.number_input("Preference Dividend (₹)", value=0.0, key="sbs_eps_pd")
        tax = st.number_input("Tax Rate (%)", value=30.0, key="sbs_eps_t")
        shares = st.number_input("Number of Shares", value=50000.0)

        st.write("**Step 1:** EBT = EBIT - Interest")
        ebt = ebit - interest
        st.latex(f"EBT = {ebit} - {interest} = {ebt}")

        st.write("**Step 2:** EAT = EBT × (1-t)")
        eat = ebt * (1-tax/100)
        st.latex(f"EAT = {ebt} \\times (1-{tax/100}) = {eat}")

        st.write("**Step 3:** EPS = (EAT - PD) / Shares")
        eps = (eat - pd_v)/shares
        st.success(f"EPS = ({eat} - {pd_v})/{shares} = ₹{round(eps,4)}")

    elif problem == "DOL Calculation":
        sales = st.number_input("Sales (₹)", value=1000000.0, key="sbs_dol_s")
        vc = st.number_input("Variable Costs (₹)", value=600000.0, key="sbs_dol_vc")
        fc = st.number_input("Fixed Costs (₹)", value=200000.0, key="sbs_dol_fc")

        contrib = sales - vc
        ebit = contrib - fc
        dol = contrib/ebit if ebit > 0 else float('inf')

        st.write("**Step 1:** Contribution = Sales - VC")
        st.latex(f"Contribution = {sales} - {vc} = {contrib}")

        st.write("**Step 2:** EBIT = Contribution - FC")
        st.latex(f"EBIT = {contrib} - {fc} = {ebit}")

        st.write("**Step 3:** DOL = Contribution / EBIT")
        st.success(f"DOL = {contrib}/{ebit} = {round(dol,4)}")

# =========================================================
# AI HINT SYSTEM
# =========================================================

elif menu == "AI Hint System":

    st.header("🤖 AI Hint System")

    problems_h = {
        "MM with Taxes (VL)": {
            "q": "VU = ₹20 Lakh, Debt = ₹8 Lakh, Tax rate = 30%. Find VL and Ke(L) if Ke(U)=12%, Kd=8%.",
            "correct": 20 + 0.3*8,
            "hints": [
                "VL = VU + t×D = 20 + 0.30×8",
                "Tax shield = 30% of ₹8L = ₹2.4L",
                "VL = 20 + 2.4 = ₹22.4 Lakh"
            ],
            "formula": r"V_L = V_U + tD = 20 + 0.3 \times 8 = 22.4\ \text{Lakh}"
        },
        "DFL": {
            "q": "EBIT = ₹2,00,000, Interest = ₹60,000. Find DFL.",
            "correct": 200000/(200000-60000),
            "hints": [
                "DFL = EBIT / (EBIT - Interest)",
                "Denominator = 2,00,000 - 60,000 = 1,40,000",
                "DFL = 2,00,000 / 1,40,000"
            ],
            "formula": r"DFL = \frac{200000}{200000-60000} = \frac{200000}{140000}"
        },
        "Indifference EBIT": {
            "q": "Plan A: I=0, N=1,00,000 shares. Plan B: I=₹60,000, N=50,000 shares. Tax=30%. Find indifference EBIT.",
            "correct": (50000*0.7*0 - 100000*0.7*60000) / (0.7*(50000-100000)),
            "hints": [
                "Set (EBIT-I1)(1-t)/N1 = (EBIT-I2)(1-t)/N2",
                "Cross multiply: N2(EBIT-I1)(1-t) = N1(EBIT-I2)(1-t)",
                "50000×EBIT×0.7 = 100000×(EBIT-60000)×0.7 → solve for EBIT"
            ],
            "formula": r"EBIT \times 50000 = (EBIT - 60000) \times 100000 \Rightarrow EBIT = 1,20,000"
        }
    }

    sel = st.selectbox("Choose Problem", list(problems_h.keys()))
    prob = problems_h[sel]
    st.markdown(f"**Problem:** {prob['q']}")

    ans = st.number_input("Your Answer", value=0.0, key="cs_hint_ans")
    if st.button("Check Answer"):
        correct = abs(prob["correct"])
        if abs(ans - correct) < correct * 0.02:
            st.success(f"✅ Correct! Answer ≈ {round(correct,4)}")
            st.balloons()
        else:
            st.error(f"❌ Off. Use hints below.")

    for i, h in enumerate(prob["hints"], 1):
        if st.checkbox(f"Hint {i}", key=f"csh_{sel}_{i}"):
            st.info(f"💡 {h}")

    if st.checkbox("Show Solution", key=f"css_{sel}"):
        st.latex(prob["formula"])

# =========================================================
# QUIZ ENGINE
# =========================================================

elif menu == "Quiz Engine":

    st.header("📝 Capital Structure Quiz Engine")

    difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])

    if "cs_quiz_gen" not in st.session_state or st.button("🔄 New Question"):
        if difficulty == "Beginner":
            st.session_state.cs_vu = random.choice([100,150,200])*10000
            st.session_state.cs_d = random.choice([30,40,50])*10000
            st.session_state.cs_t = random.choice([25,30,35])
            st.session_state.cs_type = "vl"
        elif difficulty == "Intermediate":
            st.session_state.cs_ebit = random.choice([150000,200000,250000])
            st.session_state.cs_int = random.choice([40000,50000,60000])
            st.session_state.cs_type = "dfl"
        else:
            st.session_state.cs_i1 = 0
            st.session_state.cs_n1 = random.choice([80000,100000])
            st.session_state.cs_i2 = random.choice([50000,60000,70000])
            st.session_state.cs_n2 = random.choice([40000,50000])
            st.session_state.cs_tax = random.choice([30,35])
            st.session_state.cs_type = "indiff"
        st.session_state.cs_quiz_gen = True

    qtype = st.session_state.cs_type

    if qtype == "vl":
        vu = st.session_state.cs_vu; d = st.session_state.cs_d; t = st.session_state.cs_t
        correct = vu + (t/100)*d
        st.markdown(f"**Find VL using MM with taxes:**\n- VU = ₹{vu:,}, Debt = ₹{d:,}, Tax = {t}%")

    elif qtype == "dfl":
        ebit = st.session_state.cs_ebit; int_v = st.session_state.cs_int
        correct = ebit/(ebit-int_v)
        st.markdown(f"**Find Degree of Financial Leverage:**\n- EBIT = ₹{ebit:,}, Interest = ₹{int_v:,}")

    else:
        i1=st.session_state.cs_i1; n1=st.session_state.cs_n1
        i2=st.session_state.cs_i2; n2=st.session_state.cs_n2; tax=st.session_state.cs_tax
        t = tax/100
        correct = (n2*(1-t)*i1 - n1*(1-t)*i2)/((1-t)*(n2-n1))
        st.markdown(f"**Find Indifference EBIT:**\n- Plan A: I=₹{i1:,}, N={n1:,} | Plan B: I=₹{i2:,}, N={n2:,} | Tax={tax}%")

    ans = st.number_input("Your Answer", value=0.0, key="cs_quiz_ans")
    if st.button("Submit"):
        tol = max(100, abs(correct)*0.01)
        if abs(ans - correct) < tol:
            st.success(f"✅ Correct! Answer = {round(correct,2)}")
            st.balloons()
        else:
            st.error(f"❌ Incorrect. Answer = {round(correct,2)}")

# =========================================================
# EXCEL FORMULA TRAINER
# =========================================================

elif menu == "Excel Formula Trainer":

    st.header("📊 Excel Formula Trainer — Capital Structure")

    problems_ex = {
        "MM Tax Shield": {
            "desc": "VU=₹100Cr, Debt=₹40Cr, Tax=30%. Find VL.",
            "fn": "=", "answer": "=100+30%*40",
            "hint": "VL = VU + t×D  — direct formula"
        },
        "DFL": {
            "desc": "EBIT=₹2L, Interest=₹60K. Find DFL.",
            "fn": "=", "answer": "=200000/(200000-60000)",
            "hint": "DFL = EBIT/(EBIT-Interest)"
        },
        "DOL": {
            "desc": "Contribution=₹4L, EBIT=₹2L. Find DOL.",
            "fn": "=", "answer": "=400000/200000",
            "hint": "DOL = Contribution/EBIT"
        },
        "EPS Calculation": {
            "desc": "EBIT=₹2L, Interest=₹50K, Tax=30%, Shares=50,000. Find EPS.",
            "fn": "=",
            "answer": "=(200000-50000)*(1-30%)/50000",
            "hint": "EPS = (EBIT-I)*(1-t)/N"
        },
        "Ke Levered (MM No Tax)": {
            "desc": "Ke(U)=12%, Kd=8%, D=₹4L, E=₹6L. Find Ke(L).",
            "fn": "=",
            "answer": "=12%+(12%-8%)*(400000/600000)",
            "hint": "Ke(L) = Ke(U) + (Ke(U)-Kd)*(D/E)"
        },
    }

    sel = st.selectbox("Choose Problem", list(problems_ex.keys()))
    prob = problems_ex[sel]
    st.subheader("Problem"); st.markdown(prob["desc"])
    st.info(f"💡 Hint: `{prob['hint']}`")

    user_inp = st.text_input("Enter Excel Formula")
    if st.button("Validate"):
        if prob["fn"] == "=" and user_inp.startswith("="):
            st.success(f"✅ Correct approach! Reference: `{prob['answer']}`")
        else:
            st.error("❌ Start with = for a direct formula")
    if st.checkbox("Show Answer"):
        st.code(prob["answer"], language="excel")

# =========================================================
# FORMULA CHEAT SHEET
# =========================================================

elif menu == "Formula Cheat Sheet":

    st.header("📘 Capital Structure — Formula Cheat Sheet")

    formulas = """
CAPITAL STRUCTURE — COMPLETE FORMULA REFERENCE
================================================

──────────────────────────────────────────────────
TRADITIONAL APPROACHES
──────────────────────────────────────────────────
1. NI Approach — Firm Value
   V = EAT/Ke + D  (where EAT = (EBIT-I)(1-t))

2. NOI Approach — Firm Value
   V = NOI / Ko  (Ko = constant WACC)
   Ke(Levered) = Ko + (Ko - Kd)(D/E)

──────────────────────────────────────────────────
MODIGLIANI-MILLER THEOREMS
──────────────────────────────────────────────────
3. MM Prop I (No Taxes)
   VL = VU  (capital structure irrelevant)

4. MM Prop II (No Taxes)
   Ke^L = Ke^U + (Ke^U - Kd)(D/E)
   WACC = Ke^U (constant)

5. MM Prop I (With Corporate Taxes)
   VL = VU + t × D
   Tax Shield = t × D

6. MM Prop II (With Corporate Taxes)
   Ke^L = Ke^U + (Ke^U - Kd)(1-t)(D/E)
   WACC falls as D increases

7. Miller Model (Personal Taxes)
   VL = VU + [1 - (1-Tc)(1-Te)/(1-Td)] × D

──────────────────────────────────────────────────
TRADE-OFF THEORY
──────────────────────────────────────────────────
8. VL = VU + PV(Tax Shield) - PV(Distress Costs)
   Optimal D/E: Marginal tax benefit = Marginal distress cost

──────────────────────────────────────────────────
LEVERAGE MEASURES
──────────────────────────────────────────────────
9. EPS Formula
   EPS = [(EBIT - I)(1-t) - PD] / N

10. Degree of Financial Leverage (DFL)
    DFL = EBIT / [EBIT - I - PD/(1-t)]
    Simple: DFL = EBIT / (EBIT - I)
    = % Change in EPS / % Change in EBIT

11. Degree of Operating Leverage (DOL)
    DOL = Contribution / EBIT
    = (Sales - Variable Costs) / EBIT
    = % Change in EBIT / % Change in Sales

12. Combined / Total Leverage (DTL)
    DTL = DOL × DFL
    = Contribution / [EBIT - I - PD/(1-t)]
    = % Change in EPS / % Change in Sales

13. Indifference EBIT (Two Plans)
    (EBIT-I1)(1-t)/N1 = (EBIT-I2)(1-t)/N2
    Cross-multiply and solve for EBIT

14. Break-even Point (Operating)
    BEP Sales = Fixed Costs / P/V Ratio
    P/V Ratio = Contribution / Sales

──────────────────────────────────────────────────
FIRM VALUE FORMULAS
──────────────────────────────────────────────────
15. Firm Value (Gordon Perpetuity)
    V = NOI(1-t) / WACC  (levered)
    V = NOI(1-t) / Ke(U) (unlevered)

16. Ke (Levered, MM No Tax)
    Ke^L = Ke^U + (Ke^U - Kd)(D/E)

17. Ke (Levered, MM With Tax)
    Ke^L = Ke^U + (Ke^U - Kd)(1-t)(D/E)

──────────────────────────────────────────────────
KEY DECISION RULES
──────────────────────────────────────────────────
- NI: More debt always lowers WACC (unrealistic)
- NOI: WACC constant; leverage irrelevant
- Traditional: Optimal D/E exists (U-shaped WACC)
- MM (no tax): VL = VU; WACC = Ke(U)
- MM (tax): VL = VU + tD; WACC falls with debt
- Trade-off: VL = VU + PV(TS) - PV(distress)
- Pecking order: Internal > Debt > Equity
- DFL = 1 means no financial leverage (all equity)
- Indifference EBIT: Point where EPS is equal under two plans
================================================
"""

    st.text_area("Capital Structure Formulas", formulas, height=800)
    st.download_button("📥 Download Formula Sheet", data=formulas,
                       file_name="Capital_Structure_Formulas.txt")

# =========================================================
# COMMON MISTAKES
# =========================================================

elif menu == "Common Student Mistakes":

    st.header("⚠️ Common Student Mistakes in Capital Structure")

    mistakes = pd.DataFrame({
        "Mistake": [
            "Confusing VL = VU (no tax) with VL = VU + tD (with tax)",
            "Using MM Prop II formula incorrectly (with vs without tax)",
            "Using EPS to choose capital structure for shareholders",
            "Forgetting (1-t) in Prop II with taxes",
            "DOL formula: using Sales instead of Contribution",
            "DFL: forgetting to adjust PD for tax (PD/(1-t))",
            "Indifference EBIT: not cross-multiplying correctly",
            "DTL = DOL + DFL (WRONG — it should be DOL × DFL)",
            "NI approach assumes Ke is constant — but it's unrealistic",
            "Confusing D/E ratio with D/V ratio in WACC weights",
            "Including current liabilities in capital structure",
            "Using book value instead of market value for debt in VL",
        ],
        "Correct Approach": [
            "MM 1958 (no tax): VL=VU. MM 1963 (with tax): VL=VU+tD. Know which year.",
            "No tax: Ke^L=Ke^U+(Ke^U-Kd)(D/E). With tax: Ke^L=Ke^U+(Ke^U-Kd)(1-t)(D/E)",
            "EPS maximisation ≠ wealth maximisation. Use NPV/firm value, not EPS alone.",
            "With corporate tax: the (1-t) factor reduces the Ke premium. Don't forget it.",
            "DOL = Contribution/EBIT not Sales/EBIT. Contribution = Sales - Variable Costs.",
            "DFL = EBIT/[EBIT-I-PD/(1-t)]. PD must be grossed up because it's paid after tax.",
            "Cross-multiply N2×LHS = N1×RHS, then collect EBIT terms on one side.",
            "DTL = DOL × DFL (product, not sum). DOL×DFL = Contribution/(EBIT-I)",
            "NI assumption (constant Ke) is unrealistic and is the basis of criticism.",
            "D/E = Debt/Equity. D/V = Debt/Total Value. WACC uses D/V and E/V weights.",
            "Capital structure = long-term financing only (long-term debt + equity).",
            "Use market value of debt (YTM-based price) not face value for accuracy.",
        ]
    })

    st.table(mistakes)

    st.warning("""
**Top 5 Most Tested Mistakes:**
1. VL formula — know whether taxes are included (tD or not)
2. DTL = DOL × DFL (not sum)
3. DFL denominator — include PD/(1-t) if preference shares exist
4. Indifference EBIT — cross-multiply correctly
5. Capital structure weights — use D/V and E/V (not D/E ratio)
""")

# =========================================================
# ADVANCED QUIZ BANK
# =========================================================

elif menu == "Advanced Quiz Bank":

    st.header("📝 Advanced Quiz Bank — Capital Structure")

    level = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])

    if level == "Beginner":
        st.markdown("""
**Problem:** A firm (VU=₹10L, Ke(U)=14%) adds ₹4L debt at 9% interest.
Corporate tax = 30%.
(a) Find VL  (b) Find equity value E  (c) Find Ke(Levered)
""")
        vu=10; d=4; t=0.30; keu=14; kd=9
        vl=vu+t*d; e=vl-d; de=d/e
        ke_l=keu+(keu-kd)*(1-t)*de

        c1,c2,c3=st.columns(3)
        c1.number_input("(a) VL (₹L)", value=0.0, step=0.01, key="aqb_beg_vl")
        c2.number_input("(b) E (₹L)", value=0.0, step=0.01, key="aqb_beg_e")
        c3.number_input("(c) Ke(L) %", value=0.0, step=0.01, key="aqb_beg_kel")

        if st.button("Evaluate", key="beg_btn"):
            a1=st.session_state.aqb_beg_vl; a2=st.session_state.aqb_beg_e; a3=st.session_state.aqb_beg_kel
            if all([abs(a1-vl)<0.01, abs(a2-e)<0.01, abs(a3-ke_l)<0.1]):
                st.success(f"✅ VL={vl}L, E={round(e,2)}L, Ke(L)={round(ke_l,4)}%")
                st.balloons()
            else:
                st.error(f"VL={vl}L, E={round(e,2)}L, Ke(L)={round(ke_l,4)}%")

    elif level == "Intermediate":
        st.markdown("""
**Problem:** Two plans for a firm with EBIT=₹3,00,000, Tax=30%:
- Plan X: All equity, 1,50,000 shares
- Plan Y: ₹6L debt at 10%, 75,000 shares

(a) Calculate EPS under both plans at given EBIT
(b) Find indifference EBIT
""")
        ebit=300000; t=0.30; n1=150000; i2=60000; n2=75000
        eps_x=(ebit*(1-t))/n1
        eps_y=((ebit-i2)*(1-t))/n2
        indiff_ebit=(n2*0-n1*(-i2)*(1-t))/((1-t)*(n2-n1))
        # Simpler: set equal: ebit/n1 = (ebit-60000)/n2 → n2*ebit = n1*(ebit-60000)
        # 75000*ebit = 150000*(ebit-60000) → 75000*ebit = 150000*ebit - 9000000000
        # -75000*ebit = -9000000000 → ... let me recalc
        # (EBIT)(1-t)/N1 = (EBIT-I2)(1-t)/N2
        # EBIT/150000 = (EBIT-60000)/75000
        # 75000*EBIT = 150000*(EBIT-60000)
        # 75000*EBIT = 150000*EBIT - 9,000,000,000? no
        # 75000E = 150000E - 150000*60000
        # -75000E = -9,000,000,000... no
        # 75000E = 150000E - 9000000000? That's wrong. Let me redo
        # 150000*60000 = 9,000,000. So:
        # 75000E = 150000E - 9000000 → -75000E = -9000000 → E = 120000
        indiff_ebit = 120000.0

        c1,c2,c3=st.columns(3)
        c1.number_input("EPS Plan X (₹)", value=0.0, step=0.0001, key="aqb_int_epsx")
        c2.number_input("EPS Plan Y (₹)", value=0.0, step=0.0001, key="aqb_int_epsy")
        c3.number_input("Indifference EBIT (₹)", value=0.0, step=1.0, key="aqb_int_ind")

        if st.button("Evaluate", key="int_btn"):
            a1=st.session_state.aqb_int_epsx; a2=st.session_state.aqb_int_epsy; a3=st.session_state.aqb_int_ind
            if all([abs(a1-eps_x)<0.01, abs(a2-eps_y)<0.01, abs(a3-indiff_ebit)<500]):
                st.success(f"✅ EPS-X=₹{round(eps_x,4)}, EPS-Y=₹{round(eps_y,4)}, Indiff EBIT=₹{indiff_ebit:,}")
                st.balloons()
            else:
                st.error(f"EPS-X=₹{round(eps_x,4)}, EPS-Y=₹{round(eps_y,4)}, Indiff=₹{indiff_ebit:,}")

    elif level == "Advanced":
        st.markdown("""
**Problem (Trade-off Theory):**
A firm has: VU=₹200Cr, EBIT=₹30Cr (permanent), Tax=30%.
- Adding ₹80Cr debt at 8.5%
- Financial distress costs estimated at 20% of VL if D/V > 0.3

(a) Find VL using MM with taxes
(b) Estimate net firm value after distress costs
(c) Should the firm take on ₹80Cr debt?
""")
        vu=200; d=80; t=0.30
        vl_mm=vu+t*d
        dv=d/vl_mm
        distress=0.20*vl_mm if dv>0.3 else 0
        vl_net=vl_mm-distress

        c1,c2,c3=st.columns(3)
        c1.number_input("(a) VL (MM) ₹Cr", value=0.0, step=0.1, key="aqb_adv_vl")
        c2.number_input("(b) Net VL ₹Cr", value=0.0, step=0.1, key="aqb_adv_nvl")
        choice=st.radio("(c) Decision:", ["Yes — add debt", "No — avoid debt"])

        if st.button("Evaluate", key="adv_btn"):
            a1=st.session_state.aqb_adv_vl; a2=st.session_state.aqb_adv_nvl
            correct_choice = "Yes — add debt" if vl_net > vu else "No — avoid debt"
            if abs(a1-vl_mm)<0.5 and abs(a2-vl_net)<0.5 and choice==correct_choice:
                st.success(f"✅ VL(MM)={vl_mm}Cr, Net VL={round(vl_net,2)}Cr, {correct_choice}")
                st.balloons()
            else:
                st.error(f"VL(MM)={vl_mm}Cr | Distress={round(distress,2)}Cr | Net VL={round(vl_net,2)}Cr | {correct_choice}")

# =========================================================
# PROGRESS TRACKER
# =========================================================

elif menu == "Progress Tracker":

    st.header("📈 Student Progress Tracker")

    if "cs_completed" not in st.session_state:
        st.session_state.cs_completed = []
    if "cs_scores" not in st.session_state:
        st.session_state.cs_scores = []

    all_modules = [
        "Net Income (NI) Approach", "Net Operating Income (NOI) Approach",
        "Traditional Approach", "MM — No Taxes (1958)", "MM — With Corporate Taxes (1963)",
        "Miller Model (Personal Taxes)", "Trade-off Theory", "Pecking Order Theory",
        "Market Timing Theory", "Agency Theory & Costs", "Signalling Theory",
        "Financial Distress & Bankruptcy", "EBIT-EPS Analysis", "Indifference Point",
        "Degree of Financial Leverage (DFL)", "Degree of Operating Leverage (DOL)",
        "Combined Leverage (DTL)", "Capital Structure in India",
        "Determinants of Capital Structure", "Optimal Capital Structure Decision",
    ]

    selected = st.multiselect("Mark completed:", all_modules,
                              default=st.session_state.cs_completed)
    st.session_state.cs_completed = selected

    col1, col2 = st.columns(2)
    with col1:
        topic = st.selectbox("Quiz Topic", ["Traditional Theories", "MM Theorems",
                                             "Modern Theories", "Leverage Analysis",
                                             "Applications"])
    with col2:
        score = st.number_input("Score (%)", 0, 100, 75, key="cs_score_inp")

    if st.button("Log Score"):
        st.session_state.cs_scores.append({"topic": topic, "score": score})
        st.success("Score logged!")

    st.divider()
    n_done = len(selected); n_total = len(all_modules)
    st.metric("Modules Completed", f"{n_done}/{n_total}")
    st.progress(n_done / n_total)

    trad = sum(1 for m in selected if m in ["Net Income (NI) Approach","Net Operating Income (NOI) Approach","Traditional Approach"])
    mm = sum(1 for m in selected if "MM" in m or "Miller" in m)
    modern = sum(1 for m in selected if any(k in m for k in ["Trade-off","Pecking","Market Timing","Agency","Signal","Distress"]))
    lev = sum(1 for m in selected if any(k in m for k in ["EBIT","DFL","DOL","DTL","Indifference"]))

    col1,col2,col3,col4 = st.columns(4)
    col1.metric("Traditional (3)", f"{trad}/3")
    col2.metric("MM Theories (3)", f"{mm}/3")
    col3.metric("Modern (6)", f"{modern}/6")
    col4.metric("Leverage (5)", f"{lev}/5")

    if st.session_state.cs_scores:
        avg = sum(s["score"] for s in st.session_state.cs_scores)/len(st.session_state.cs_scores)
        st.metric("Average Score", f"{round(avg,1)}%")
        st.dataframe(pd.DataFrame(st.session_state.cs_scores), use_container_width=True)

    if n_done == n_total:
        st.success("🏆 All modules complete!")
        st.balloons()

# =========================================================
# CASE-BASED LEARNING
# =========================================================

elif menu == "Case-Based Learning":

    st.header("📚 Case Study: Tata Steel — Capital Structure Decisions")

    st.markdown("""
## Background

Tata Steel is a classic case of capital structure dynamics:
- Capital-intensive (high fixed asset base → high DOL)
- Cyclical industry (volatile EBIT → leverage amplification risk)
- Significant debt taken for Corus acquisition (2007) → leverage challenges
- Subsequent deleveraging (2014–2022)

---

## Financial Data (Simplified — FY2023)

| Item | Value |
|---|---|
| Sales | ₹2,43,353 Crore |
| Variable Costs | ₹1,95,000 Crore |
| Fixed Costs | ₹30,000 Crore |
| EBIT | ₹18,353 Crore |
| Interest Charges | ₹7,500 Crore |
| Preference Dividend | ₹0 |
| Tax Rate | 25% |
| Equity Shares | 1,200 Crore |
| Market Cap | ₹1,70,000 Crore |
| Total Debt (Market) | ₹60,000 Crore |
| VU (Unlevered equivalent) | ₹1,50,000 Crore |
""")

    st.subheader("Step 1: Operating Leverage")

    sales = 243353; vc = 195000; fc = 30000
    contribution = sales - vc
    ebit = 18353
    dol = contribution / ebit

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Contribution", f"₹{contribution:,} Cr")
    with col2:
        st.metric("EBIT", f"₹{ebit:,} Cr")
    with col3:
        st.metric("DOL", round(dol, 2))

    st.info(f"DOL = {round(dol,2)}: A 10% change in sales causes a {round(dol*10,1)}% change in EBIT — HIGH operating risk due to fixed costs")

    st.subheader("Step 2: Financial Leverage")

    interest = 7500
    dfl = ebit / (ebit - interest)

    st.metric("DFL", round(dfl, 2))
    st.info(f"DFL = {round(dfl,2)}: A 10% change in EBIT causes a {round(dfl*10,1)}% change in EPS")

    st.subheader("Step 3: Combined Leverage")

    dtl = dol * dfl
    st.metric("DTL = DOL × DFL", round(dtl, 2))
    st.warning(f"DTL = {round(dtl,2)}: A 10% change in SALES causes a {round(dtl*10,1)}% change in EPS — very high combined risk!")

    st.subheader("Step 4: MM Valuation with Taxes")

    vu = 150000; debt_mkt = 60000; tax = 25
    ts = (tax/100)*debt_mkt
    vl = vu + ts
    equity_v = vl - debt_mkt

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tax Shield (t×D)", f"₹{ts:,} Cr")
    with col2:
        st.metric("VL (MM with tax)", f"₹{vl:,} Cr")
    with col3:
        st.metric("Equity Value", f"₹{equity_v:,} Cr")

    st.subheader("Step 5: Capital Structure Lessons")

    lessons = [
        "**High DOL + High DFL = Very High DTL** — cyclical firms like Tata Steel face amplified EPS volatility",
        "**Corus acquisition (2007)** loaded massive debt → D/E spiked → credit rating downgrade → higher Kd",
        "**Deleveraging (2014-22):** Sold assets, issued equity → reduced D/E → restored investment grade rating",
        "**Trade-off Theory applies:** Tax shield benefit is real but distress cost was significant during commodity downturn",
        "**Current approach:** Moderate leverage with focus on FCF generation to service and reduce debt",
    ]
    for l in lessons:
        st.markdown(f"- {l}")

    st.success(f"""
**Summary:**
- DOL = {round(dol,2)} | DFL = {round(dfl,2)} | DTL = {round(dtl,2)}
- VL (MM with {tax}% tax) = ₹{vl:,} Cr (includes ₹{ts:,} Cr tax shield)
- Tata Steel's story: Heavy leverage for growth → financial distress → managed deleveraging → value recovery
""")
