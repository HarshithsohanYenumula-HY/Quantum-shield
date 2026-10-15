
import random

import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="QuantumShield | Quantum Cybersecurity",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #07111f 0%, #101b30 100%);
        color: #F8FAFC;
    }

    [data-testid="stSidebar"] {
        background-color: #0B1424;
        border-right: 1px solid #26364D;
    }

    h1, h2, h3, h4, p, label {
        color: #F8FAFC;
    }

    .hero {
        padding: 26px;
        border-radius: 18px;
        background: linear-gradient(110deg, #142C49, #183B55);
        border: 1px solid #34516E;
        margin-bottom: 22px;
    }

    .hero h1 {
        margin-bottom: 8px;
        font-size: 36px;
    }

    .hero p {
        color: #D5E4F5;
        font-size: 16px;
        margin-bottom: 0;
    }

    .section-card {
        background: #111E30;
        border: 1px solid #2A3D55;
        padding: 18px;
        border-radius: 14px;
        margin-bottom: 12px;
    }

    .small-muted {
        color: #C1D0E0;
        font-size: 14px;
    }

    [data-testid="stMetric"] {
        background-color: #142338;
        border: 1px solid #334A65;
        padding: 16px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: #D5E4F5 !important;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }

    [data-testid="stMetricDelta"] {
        color: #D5E4F5 !important;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #0D9488, #0891B2);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        min-height: 44px;
    }

    div.stButton > button:hover {
        border: 1px solid #67E8F9;
        color: white;
    }

    div[data-baseweb="tab-list"] {
        gap: 8px;
    }

    button[data-baseweb="tab"] {
        color: #D5E4F5;
    }

    hr {
        border-color: #2A3D55;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# BB84 SIMULATION
# --------------------------------------------------

def run_bb84_simulation(number_of_bits, eve_enabled, noise_percent):
    """
    Educational BB84 simulation.

    Each basis is represented by 0 or 1.
    Matching bases allow the receiver to recover the bit.
    A mismatched basis produces a random measurement.
    """

    alice_bits = [random.randint(0, 1) for _ in range(number_of_bits)]
    alice_bases = [random.randint(0, 1) for _ in range(number_of_bits)]
    bob_bases = [random.randint(0, 1) for _ in range(number_of_bits)]

    bob_bits = []
    eve_bases = []

    for i in range(number_of_bits):
        transmitted_bit = alice_bits[i]

        # Eve intercepts and measures the quantum state.
        if eve_enabled:
            eve_basis = random.randint(0, 1)
            eve_bases.append(eve_basis)

            if eve_basis == alice_bases[i]:
                eve_bit = transmitted_bit
            else:
                eve_bit = random.randint(0, 1)

            transmitted_bit = eve_bit
            measurement_basis = eve_basis
        else:
            measurement_basis = alice_bases[i]

        # Bob measures the state using his chosen basis.
        if bob_bases[i] == measurement_basis:
            bob_bit = transmitted_bit
        else:
            bob_bit = random.randint(0, 1)

        # Optional noise in the communication channel.
        if random.random() < noise_percent / 100:
            bob_bit = 1 - bob_bit

        bob_bits.append(bob_bit)

    # Sifting: retain positions where Alice and Bob chose
    # the same measurement basis.
    sifted_positions = [
        i for i in range(number_of_bits)
        if alice_bases[i] == bob_bases[i]
    ]

    alice_key = [alice_bits[i] for i in sifted_positions]
    bob_key = [bob_bits[i] for i in sifted_positions]

    sifted_length = len(alice_key)

    if sifted_length == 0:
        qber = 0.0
        errors = 0
    else:
        errors = sum(
            a != b for a, b in zip(alice_key, bob_key)
        )
        qber = (errors / sifted_length) * 100

    return {
        "transmitted": number_of_bits,
        "sifted": sifted_length,
        "errors": errors,
        "qber": qber,
        "alice_key": alice_key,
        "bob_key": bob_key,
        "eve_enabled": eve_enabled,
        "noise_percent": noise_percent,
    }


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🛡️ QuantumShield</h1>
        <p>
            Exploring quantum key distribution and
            post-quantum cryptography through an interactive
            cybersecurity dashboard.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("## ⚙️ Simulation Controls")

    number_of_bits = st.slider(
        "Number of transmitted bits",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100,
    )

    noise_percent = st.slider(
        "Channel noise (%)",
        min_value=0,
        max_value=10,
        value=1,
        help="Artificial noise added to Bob's measurements.",
    )

    st.markdown("---")
    st.markdown("### How to use")
    st.write("1. Select the number of bits.")
    st.write("2. Choose a channel noise level.")
    st.write("3. Run the simulation.")
    st.write("4. Compare Eve OFF and Eve ON.")

    st.caption(
        "Educational simulation only. "
        "It does not create or exchange real cryptographic keys."
    )


# --------------------------------------------------
# TABS
# --------------------------------------------------

bb84_tab, pqc_tab, about_tab = st.tabs(
    [
        "🔬 BB84 Quantum Lab",
        "🔐 PQC Readiness",
        "ℹ️ About QuantumShield",
    ]
)


# --------------------------------------------------
# TAB 1: BB84 LAB
# --------------------------------------------------

with bb84_tab:
    st.subheader("BB84 Quantum Key Distribution")
    st.write(
        "Compare the observed quantum bit error rate (QBER) "
        "when an eavesdropper is absent and when Eve intercepts "
        "and measures the transmitted states."
    )

    col_a, col_b = st.columns(2)

    with col_a:
        run_off = st.button(
            "▶ Run Eve OFF",
            use_container_width=True,
        )

    with col_b:
        run_on = st.button(
            "▶ Run Eve ON",
            use_container_width=True,
        )

    if run_off:
        st.session_state["eve_off_result"] = run_bb84_simulation(
            number_of_bits,
            eve_enabled=False,
            noise_percent=noise_percent,
        )

    if run_on:
        st.session_state["eve_on_result"] = run_bb84_simulation(
            number_of_bits,
            eve_enabled=True,
            noise_percent=noise_percent,
        )

    # Run both scenarios the first time the page is opened.
    if (
        "eve_off_result" not in st.session_state
        or "eve_on_result" not in st.session_state
    ):
        st.info(
            "Run both scenarios to compare their results. "
            "The initial comparison is generated automatically."
        )

        st.session_state["eve_off_result"] = run_bb84_simulation(
            number_of_bits,
            eve_enabled=False,
            noise_percent=noise_percent,
        )

        st.session_state["eve_on_result"] = run_bb84_simulation(
            number_of_bits,
            eve_enabled=True,
            noise_percent=noise_percent,
        )

    off_result = st.session_state["eve_off_result"]
    on_result = st.session_state["eve_on_result"]

    # Avoid comparing results generated with different settings.
    settings_changed = (
        off_result["transmitted"] != number_of_bits
        or on_result["transmitted"] != number_of_bits
        or off_result["noise_percent"] != noise_percent
        or on_result["noise_percent"] != noise_percent
    )

    if settings_changed:
        st.warning(
            "Your settings have changed. Run both scenarios again "
            "for a fair comparison."
        )

    st.markdown("---")
    st.subheader("📊 Simulation Results")

    # Four readable summary metrics.
    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Bits Transmitted",
        f"{number_of_bits:,}",
    )

    m2.metric(
        "Eve OFF QBER",
        f"{off_result['qber']:.1f}%",
    )

    m3.metric(
        "Eve ON QBER",
        f"{on_result['qber']:.1f}%",
    )

    qber_difference = on_result["qber"] - off_result["qber"]

    m4.metric(
        "QBER Difference",
        f"{qber_difference:+.1f} pp",
    )

    st.markdown("---")
    st.subheader("QBER Comparison")

    chart_data = pd.DataFrame(
        {
            "Scenario": ["Eve OFF", "Eve ON"],
            "QBER (%)": [
                off_result["qber"],
                on_result["qber"],
            ],
        }
    )

    chart = px.bar(
        chart_data,
        x="Scenario",
        y="QBER (%)",
        color="Scenario",
        color_discrete_map={
            "Eve OFF": "#22C55E",
            "Eve ON": "#F97316",
        },
        text="QBER (%)",
    )

    chart.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
    )

    chart.update_layout(
        height=340,
        showlegend=False,
        plot_bgcolor="#111827",
        paper_bgcolor="#111827",
        font=dict(
            color="#FFFFFF",
            size=14,
        ),
        yaxis=dict(
            title="QBER (%)",
            range=[
                0,
                max(
                    10,
                    min(
                        100,
                        max(
                            off_result["qber"],
                            on_result["qber"],
                        ) + 8,
                    ),
                ),
            ],
            ticksuffix="%",
            tickfont=dict(color="#FFFFFF"),
            title_font=dict(color="#FFFFFF"),
            gridcolor="#374151",
            zerolinecolor="#64748B",
        ),
        xaxis=dict(
            title="Simulation scenario",
            tickfont=dict(color="#FFFFFF"),
            title_font=dict(color="#FFFFFF"),
            showgrid=False,
        ),
        margin=dict(l=35, r=35, t=35, b=45),
    )

    st.plotly_chart(
        chart,
        use_container_width=True,
        config={"displayModeBar": False},
    )

    st.caption(
        "QBER = incorrect bits ÷ sifted bits × 100. "
        "The sifted key contains only positions where Alice and Bob "
        "chose the same basis."
    )

    # Security interpretation.
    st.subheader("🛡️ Security Interpretation")

    if settings_changed:
        st.info(
            "Run both Eve OFF and Eve ON again to update the "
            "comparison using your current settings."
        )
    elif qber_difference > 5:
        st.warning(
            "The Eve ON simulation produced a noticeably higher "
            "error rate. This is consistent with the disturbance "
            "that intercept-and-resend eavesdropping can introduce."
        )
    elif qber_difference < -5:
        st.info(
            "Eve ON happened to produce a lower observed error rate "
            "in this sample. Random measurement outcomes and channel "
            "noise can affect finite simulations. Repeat the test."
        )
    else:
        st.info(
            "The observed error rates are close in this sample. "
            "A small difference does not prove that eavesdropping "
            "is absent."
        )

    st.markdown(
        """
        <div class="section-card">
            <b>Important:</b>
            A QBER threshold cannot be chosen from this demonstration
            alone. Real QKD security depends on the protocol,
            authentication, implementation, noise model, and
            statistical analysis of the observed data.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("View simulation details"):
        detail_data = pd.DataFrame(
            [
                {
                    "Measurement": "Eve OFF",
                    "Transmitted bits": off_result["transmitted"],
                    "Sifted bits": off_result["sifted"],
                    "Bit errors": off_result["errors"],
                    "QBER (%)": round(off_result["qber"], 2),
                },
                {
                    "Measurement": "Eve ON",
                    "Transmitted bits": on_result["transmitted"],
                    "Sifted bits": on_result["sifted"],
                    "Bit errors": on_result["errors"],
                    "QBER (%)": round(on_result["qber"], 2),
                },
            ]
        )

        st.dataframe(
            detail_data,
            hide_index=True,
            use_container_width=True,
        )


# --------------------------------------------------
# TAB 2: POST-QUANTUM CRYPTOGRAPHY
# --------------------------------------------------

with pqc_tab:
    st.subheader("Post-Quantum Cryptography Readiness")
    st.write(
        "Post-quantum cryptography (PQC) uses algorithms designed "
        "to resist attacks from both classical and sufficiently "
        "powerful quantum computers."
    )

    st.markdown("### Standardized NIST algorithms")

    pqc_data = pd.DataFrame(
        [
            {
                "Algorithm": "ML-KEM",
                "Standard": "FIPS 203",
                "Purpose": "Key establishment",
                "Readiness": "Review integration",
            },
            {
                "Algorithm": "ML-DSA",
                "Standard": "FIPS 204",
                "Purpose": "Digital signatures",
                "Readiness": "Review integration",
            },
            {
                "Algorithm": "SLH-DSA",
                "Standard": "FIPS 205",
                "Purpose": "Digital signatures",
                "Readiness": "Review integration",
            },
        ]
    )

    st.dataframe(
        pqc_data,
        hide_index=True,
        use_container_width=True,
    )

    st.caption(
        "These are standardized algorithms, not algorithms "
        "implemented or tested by this dashboard."
    )

    st.markdown("---")
    st.subheader("Example Readiness Inventory")

    st.write(
        "Use this checklist to record which parts of a hypothetical "
        "system need review. It is an educational inventory, not a "
        "real vulnerability scanner."
    )

    inventory_items = [
        "TLS / HTTPS certificates and connections",
        "Digital signatures and software updates",
        "Key exchange and key-management systems",
        "Long-term sensitive data and stored encrypted data",
        "Third-party libraries and vendor dependencies",
    ]

    if "pqc_inventory" not in st.session_state:
        st.session_state["pqc_inventory"] = {
            item: False for item in inventory_items
        }

    for item in inventory_items:
        st.session_state["pqc_inventory"][item] = st.checkbox(
            item,
            value=st.session_state["pqc_inventory"][item],
            key=f"pqc_{item}",
        )

    reviewed_count = sum(
        st.session_state["pqc_inventory"].values()
    )

    st.progress(
        reviewed_count / len(inventory_items),
        text=(
            f"{reviewed_count} of {len(inventory_items)} "
            "inventory areas reviewed"
        ),
    )

    st.info(
        "Reviewing an item means you have examined it. "
        "It does not mean that it is already quantum-safe."
    )


# --------------------------------------------------
# TAB 3: ABOUT
# --------------------------------------------------

with about_tab:
    st.subheader("About QuantumShield")

    st.markdown(
        """
        <div class="section-card">
            <h3>🎯 Project Objective</h3>
            Demonstrate the principles of quantum key distribution
            and introduce the need for post-quantum cryptography.
        </div>

        <div class="section-card">
            <h3>🔬 Module 1 — BB84 Simulation</h3>
            Models random quantum-basis measurements, key sifting,
            optional intercept-and-resend eavesdropping, channel
            noise, and the resulting QBER.
        </div>

        <div class="section-card">
            <h3>🔐 Module 2 — PQC Readiness</h3>
            Introduces standardized post-quantum algorithms and
            provides a checklist for reviewing cryptographic assets.
        </div>

        <div class="section-card">
            <h3>⚠️ Limitations</h3>
            This is a simplified educational simulation. It does not
            simulate a physical quantum channel, implement a complete
            QKD security proof, exchange real secret keys, or scan a
            computer for vulnerabilities.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Key takeaway")

    st.success(
        "QuantumShield demonstrates how quantum communication "
        "and post-quantum cryptography can contribute to "
        "future cybersecurity."
    )

    st.caption(
        "Prototype for educational and competition use."
    )
