import math

# Constant
G = 9.81  # Acceleration due to gravity (m/s^2)

def calculate_reynolds_number(density, velocity, diameter, viscosity):
    """Calculates Reynolds Number (Re)"""
    return (density * velocity * diameter) / viscosity

def calculate_friction_factor(reynolds, roughness, diameter):
    """Calculates Darcy Friction Factor (f)"""
    if reynolds <= 0:
        raise ValueError("Reynolds number must be greater than zero.")
    if reynolds <= 2000:
        # Laminar flow
        return 64.0 / reynolds
    else:
        # Turbulent flow (Swamee-Jain equation)
        relative_roughness = roughness / diameter
        term = (relative_roughness / 3.7) + (5.74 / (reynolds ** 0.9))
        f = 0.25 / (math.log10(term) ** 2)
        return f

def calculate_head_loss(f, length, diameter, velocity):
    """Calculates Head Loss (hf) in meters"""
    return f * (length / diameter) * ((velocity ** 2) / (2 * G))

def calculate_pressure_drop(head_loss, density):
    """Calculates Pressure Drop (delta_p) in Pascals"""
    return density * G * head_loss

def get_positive_float(prompt_text):
    """Helper to get validated positive float input from user."""
    while True:
        try:
            val = float(input(prompt_text))
            if val <= 0:
                print("Error: Value must be greater than zero. Please try again.")
                continue
            return val
        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")

def main():
    while True:
        print("\n" + "="*42)
        print("      STREAMLINED PIPE FLOW CALCULATOR")
        print("="*42)
        print("1. Calculate Reynolds Number & Regime")
        print("2. Calculate Darcy Friction Factor")
        print("3. Calculate Head Loss")
        print("4. Calculate Pressure Drop")
        print("5. All-in-One Complete Pipe Flow Analysis")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            rho = get_positive_float("Enter fluid density (kg/m^3): ")
            v = get_positive_float("Enter fluid velocity (m/s): ")
            d = get_positive_float("Enter pipe inner diameter (m): ")
            mu = get_positive_float("Enter dynamic viscosity (Pa·s): ")
            
            re = calculate_reynolds_number(rho, v, d, mu)
            print(f"\nResult: Reynolds Number (Re) = {re:.2f}")
            if re < 2000:
                print("Flow Regime: Laminar")
            elif re <= 4000:
                print("Flow Regime: Transitional")
            else:
                print("Flow Regime: Turbulent")

        elif choice == '2':
            re = get_positive_float("Enter Reynolds number: ")
            d = get_positive_float("Enter pipe inner diameter (m): ")
            epsilon = get_positive_float("Enter pipe roughness (m) [e.g., 0.000045 for commercial steel]: ")
            
            try:
                f = calculate_friction_factor(re, epsilon, d)
                print(f"\nResult: Darcy Friction Factor (f) = {f:.5f}")
            except ValueError as e:
                print(f"\nError: {e}")

        elif choice == '3':
            f = get_positive_float("Enter Darcy friction factor (f): ")
            L = get_positive_float("Enter pipe length (m): ")
            d = get_positive_float("Enter pipe inner diameter (m): ")
            v = get_positive_float("Enter fluid velocity (m/s): ")
            
            hf = calculate_head_loss(f, L, d, v)
            print(f"\nResult: Head Loss (hf) = {hf:.4f} m")

        elif choice == '4':
            hf = get_positive_float("Enter head loss (m): ")
            rho = get_positive_float("Enter fluid density (kg/m^3): ")
            
            dp = calculate_pressure_drop(hf, rho)
            print(f"\nResult: Pressure Drop (ΔP) = {dp:.2f} Pa ({dp/1000:.3f} kPa)")

        elif choice == '5':
            print("\n--- All-in-One Pipe Flow Analysis ---")
            rho = get_positive_float("Enter fluid density (kg/m^3): ")
            v = get_positive_float("Enter fluid velocity (m/s): ")
            d = get_positive_float("Enter pipe inner diameter (m): ")
            mu = get_positive_float("Enter dynamic viscosity (Pa·s): ")
            epsilon = get_positive_float("Enter pipe roughness (m) [e.g., 0.000045]: ")
            L = get_positive_float("Enter pipe length (m): ")

            re = calculate_reynolds_number(rho, v, d, mu)
            regime = "Laminar" if re < 2000 else ("Transitional" if re <= 4000 else "Turbulent")
            
            try:
                f = calculate_friction_factor(re, epsilon, d)
                hf = calculate_head_loss(f, L, d, v)
                dp = calculate_pressure_drop(hf, rho)

                print("\n" + "-"*42)
                print("             ANALYSIS RESULTS")
                print("-"*42)
                print(f"Reynolds Number (Re)      : {re:.2f}")
                print(f"Flow Regime               : {regime}")
                print(f"Darcy Friction Factor (f) : {f:.5f}")
                print(f"Head Loss (hf)            : {hf:.4f} m")
                print(f"Pressure Drop (ΔP)        : {dp:.2f} Pa ({dp/1000:.3f} kPa)")
                print("-"*42)
            except ValueError as e:
                print(f"\nCalculation Error: {e}")

        elif choice == '6':
            print("\nExiting calculator. Goodbye!")
            break
        else:
            print("\nInvalid selection. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()
