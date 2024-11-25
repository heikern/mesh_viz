import pypsa

# Create a new PyPSA network
network = pypsa.Network()

# Set the snapshot time (can be expanded for multiple time steps)
network.set_snapshots(["2024-01-01 00:00"])

# Add buses (nodes)
for i in range(5):
    network.add("Bus", f"Bus {i+1}",
                v_nom=110,  # Nominal voltage in kV
                x=0, y=i)  # Dummy coordinates for visualization

# Add lines to form a mesh network
lines = [
    ("Bus 1", "Bus 2"),
    ("Bus 1", "Bus 3"),
    ("Bus 2", "Bus 4"),
    ("Bus 3", "Bus 5"),
    ("Bus 4", "Bus 5"),
    ("Bus 1", "Bus 4"),
    ("Bus 2", "Bus 5"),
]
for i, (bus0, bus1) in enumerate(lines):
    network.add("Line", f"Line {i+1}",
                bus0=bus0,
                bus1=bus1,
                length=100,  # Length in km
                r=0.1,       # Resistance per km
                x=0.4,       # Reactance per km
                c=0.01)      # Capacitance per km

# Add generators at two buses
generators = [("Bus 1", 100), ("Bus 3", 150)]  # (bus, p_nom)
for i, (bus, p_nom) in enumerate(generators):
    network.add("Generator", f"Generator {i+1}",
                bus=bus,
                p_nom=p_nom,    # Nominal power in MW
                marginal_cost=50,  # Cost per MWh
                carrier="solar")

# Add loads at all buses
for i in range(5):
    network.add("Load", f"Load {i+1}",
                bus=f"Bus {i+1}",
                p_set=50)  # Set load in MW

# Output the network to verify
print(network)

# Optionally export to file
# network.export_to_netcdf("5_node_mesh.nc")

# Solve the network's optimal power flow (OPF)
network.lopf(network.snapshots)

# Print results for generators and loads
print(network.generators_t.p)  # Generator outputs
print(network.loads_t.p)       # Load power consumptions
