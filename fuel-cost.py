def calculate_costs():
    # Default values
    gasoline_price = 3.50  # per gallon
    diesel_price = 4.00  # per gallon
    electricity_price = 0.12  # per kWh

    gasoline_efficiency = 25.0  # miles per gallon
    diesel_efficiency = 30.0  # miles per gallon
    electric_efficiency = 4.0  # miles per kWh

    annual_mileage = 12000.0  # miles

    # Prompt user for input
    use_defaults = input("Would you like to use the default assumptions? (yes/no): ")
    if use_defaults.lower() != "yes":
        gasoline_price = float(input("Enter the price of gasoline per gallon: "))
        diesel_price = float(input("Enter the price of diesel per gallon: "))
        electricity_price = float(input("Enter the price of electricity per kWh: "))
        gasoline_efficiency = float(input("Enter the fuel efficiency of the gasoline vehicle (miles/gallon): "))
        diesel_efficiency = float(input("Enter the fuel efficiency of the diesel vehicle (miles/gallon): "))
        electric_efficiency = float(input("Enter the fuel efficiency of the electric vehicle (miles/kWh): "))
        annual_mileage = float(input("Enter your annual mileage: "))

    # Calculate annual and per mile costs
    gasoline_cost = (annual_mileage / gasoline_efficiency) * gasoline_price
    diesel_cost = (annual_mileage / diesel_efficiency) * diesel_price
    electric_cost = (annual_mileage / electric_efficiency) * electricity_price

    gasoline_cost_per_mile = gasoline_cost / annual_mileage
    diesel_cost_per_mile = diesel_cost / annual_mileage
    electric_cost_per_mile = electric_cost / annual_mileage

    # Print results
    print(f"\nAnnual and per-mile costs:")
    print(f"Gasoline vehicle: ${gasoline_cost:.2f} per year, ${gasoline_cost_per_mile:.2f} per mile")
    print(f"Diesel vehicle: ${diesel_cost:.2f} per year, ${diesel_cost_per_mile:.2f} per mile")
    print(f"Electric vehicle: ${electric_cost:.2f} per year, ${electric_cost_per_mile:.2f} per mile")


if __name__ == "__main__":
    calculate_costs()
