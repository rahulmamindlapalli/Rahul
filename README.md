
import math
import streamlit as st

# Constant
G = 9.81  # Acceleration due to gravity (m/s^2)

# -----------------------------
# Calculation Functions
# -----------------------------

def calculate_reynolds_number(density, velocity, diameter, viscosity):
    """Calculate Reynolds Number."""
    return (density * velocity * diameter) / viscosity


def calculate_friction_factor(reynolds, roughness, diameter):
    """Calculate Darcy Friction Factor."""
    if reynolds <= 0:
        raise ValueError("Reynolds number must be greater than zero.")

    if diameter <= 0:
        raise ValueError("Diameter must be greater than zero.")

    if roughness < 0:
        raise ValueError("Roughness cannot be negative.")

    if reynolds <= 2000:
        # Laminar flow
        return 64.0 / reynolds
    else:
        # Turbulent flow: Swamee-Jain equation
        relative_roughness = roughness / diameter
        term = (relative_roughness / 3.7) + (
            5.74 / (reynolds ** 0.9)
        )
        return 0.25 / (math.log10(term) ** 2)


def calculate_head_loss(f, length, diameter, velocity):
    """Calculate Darcy-Weisbach head loss."""
    return f * (length / diameter) * (velocity**2 / (2 * G))


def calculate_pressure_drop(head_loss, density):
    """Calculate pressure drop in Pascals."""
    return density * G * head_loss


def get_flow_regime(reynolds):
    """Determine flow regime."""
    if reynolds < 2000:
        return "Laminar"
    elif reynolds <= 4000:
        return "Transitional"
    return "Turbulent"


# -----------------------------
# Streamlit Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Pipe Flow Calculator",
    page_icon="🌊",
    layout="wide"
)

st.title("🌊 Streamlined Pipe Flow Calculator")
st.caption(
    "Calculate Reynolds number, Darcy friction factor, "
    "head loss, and pressure drop."
)

st.divider()

# Sidebar navigation
st.sidebar.title("Navigation")

option = st.sidebar.radio(
    "Select calculation",
    [
        "Reynolds Number & Flow Regime",
        "Darcy Friction Factor",
        "Head Loss",
        "Pressure Drop",
        "Complete Pipe Flow Analysis"
    ]
)

# -----------------------------
# 1. Reynolds Number
# -----------------------------

if option == "Reynolds Number & Flow Regime":
    st.header("1. Reynolds Number & Flow Regime")

    col1, col2 = st.columns(2)

    with col1:
        rho = st.number_input(
            "Fluid density (kg/m³)",
            min_value=0.000001,
            value=1000.0,
            format="%.6f"
        )

        velocity = st.number_input(
            "Fluid velocity (m/s)",
            min_value=0.000001,
            value=1.0,
            format="%.6f"
        )

    with col2:
        diameter = st.number_input(
            "Pipe inner diameter (m)",
            min_value=0.000001,
            value=0.1,
            format="%.6f"
        )

        viscosity = st.number_input(
            "Dynamic viscosity (Pa·s)",
            min_value=0.000000001,
            value=0.001,
            format="%.9f"
        )

    if st.button("Calculate Reynolds Number", type="primary"):
        re = calculate_reynolds_number(
            rho, velocity, diameter, viscosity
        )
        regime = get_flow_regime(re)

        st.subheader("Results")
        col1, col2 = st.columns(2)
        col1.metric("Reynolds Number", f"{re:.2f}")
        col2.metric("Flow Regime", regime)

        st.info(
            "Laminar: Re < 2000 | "
            "Transitional: 2000–4000 | "
            "Turbulent: Re > 4000"
        )

# -----------------------------
# 2. Darcy Friction Factor
# -----------------------------

elif option == "Darcy Friction Factor":
    st.header("2. Darcy Friction Factor")

    col1, col2 = st.columns(2)

    with col1:
        reynolds = st.number_input(
            "Reynolds number",
            min_value=0.000001,
            value=10000.0
        )

        diameter = st.number_input(
            "Pipe inner diameter (m)",
            min_value=0.000001,
            value=0.1
        )

    with col2:
        roughness = st.number_input(
            "Pipe roughness (m)",
            min_value=0.0,
            value=0.000045,
            format="%.8f"
        )

    if st.button("Calculate Friction Factor", type="primary"):
        f = calculate_friction_factor(
            reynolds, roughness, diameter
        )
        st.metric("Darcy Friction Factor (f)", f"{f:.5f}")

        if reynolds <= 2000:
            st.info("Using the laminar-flow equation: f = 64/Re")
        else:
            st.info("Using the Swamee–Jain turbulent-flow equation.")

# -----------------------------
# 3. Head Loss
# -----------------------------

elif option == "Head Loss":
    st.header("3. Head Loss (Darcy–Weisbach Equation)")

    col1, col2 = st.columns(2)

    with col1:
        friction_factor = st.number_input(
            "Darcy friction factor",
            min_value=0.000001,
            value=0.03
        )

        length = st.number_input(
            "Pipe length (m)",
            min_value=0.000001,
            value=100.0
        )

    with col2:
        diameter = st.number_input(
            "Pipe inner diameter (m)",
            min_value=0.000001,
            value=0.1
        )

        velocity = st.number_input(
            "Fluid velocity (m/s)",
            min_value=0.000001,
            value=1.0
        )

    if st.button("Calculate Head Loss", type="primary"):
        hf = calculate_head_loss(
            friction_factor, length, diameter, velocity
        )
        st.metric("Head Loss (hf)", f"{hf:.4f} m")

# -----------------------------
# 4. Pressure Drop
# -----------------------------

elif option == "Pressure Drop":
    st.header("4. Pressure Drop")

    col1, col2 = st.columns(2)

    with col1:
        head_loss = st.number_input(
            "Head loss (m)",
            min_value=0.0,
            value=1.0
        )

    with col2:
        rho = st.number_input(
            "Fluid density (kg/m³)",
            min_value=0.000001,
            value=1000.0
        )

    if st.button("Calculate Pressure Drop", type="primary"):
        dp = calculate_pressure_drop(head_loss, rho)

        col1, col2 = st.columns(2)
        col1.metric("Pressure Drop (Pa)", f"{dp:.2f}")
        col2.metric("Pressure Drop (kPa)", f"{dp / 1000:.3f}")

# -----------------------------
# 5. Complete Pipe Flow Analysis
# -----------------------------

elif option == "Complete Pipe Flow Analysis":
    st.header("5. Complete Pipe Flow Analysis")
    st.write("Enter all pipe and fluid properties below.")

    st.subheader("Fluid Properties")

    col1, col2 = st.columns(2)

    with col1:
        rho = st.number_input(
            "Fluid density (kg/m³)",
            min_value=0.000001,
            value=1000.0,
            key="all_rho"
        )

        velocity = st.number_input(
            "Fluid velocity (m/s)",
            min_value=0.000001,
            value=1.0,
            key="all_velocity"
        )

        viscosity = st.number_input(
            "Dynamic viscosity (Pa·s)",
            min_value=0.000000001,
            value=0.001,
            format="%.9f",
            key="all_viscosity"
        )

    with col2:
        diameter = st.number_input(
            "Pipe inner diameter (m)",
            min_value=0.000001,
            value=0.1,
            key="all_diameter"
        )

        roughness = st.number_input(
            "Pipe roughness (m)",
            min_value=0.0,
            value=0.000045,
            format="%.8f",
            key="all_roughness"
        )

        length = st.number_input(
            "Pipe length (m)",
            min_value=0.000001,
            value=100.0,
            key="all_length"
        )

    if st.button("Run Complete Analysis", type="primary"):
        re = calculate_reynolds_number(
            rho, velocity, diameter, viscosity
        )
        regime = get_flow_regime(re)

        f = calculate_friction_factor(
            re, roughness, diameter
        )

        hf = calculate_head_loss(
            f, length, diameter, velocity
        )

        dp = calculate_pressure_drop(hf, rho)

        st.divider()
        st.subheader("Analysis Results")

        col1, col2, col3 = st.columns(3)
        col1.metric("Reynolds Number", f"{re:.2f}")
        col2.metric("Flow Regime", regime)
        col3.metric("Friction Factor", f"{f:.5f}")

        col1, col2 = st.columns(2)
        col1.metric("Head Loss (m)", f"{hf:.4f}")
        col2.metric("Pressure Drop (kPa)", f"{dp / 1000:.3f}")

        with st.expander("View detailed results"):
            st.write(f"**Reynolds Number:** {re:.2f}")
            st.write(f"**Flow Regime:** {regime}")
            st.write(f"**Darcy Friction Factor:** {f:.5f}")
            st.write(f"**Head Loss:** {hf:.4f} m")
            st.write(f"**Pressure Drop:** {dp:.2f} Pa")
            st.write(f"**Pressure Drop:** {dp / 1000:.3f} kPa")

st.divider()
st.caption(
    "Pipe Flow Calculator | Darcy–Weisbach equation | "
    "Gravity = 9.81 m/s²"
)

