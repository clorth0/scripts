import nmap

# Create an instance of the nmap.PortScanner class
scanner = nmap.PortScanner()

# Ask the user for the target host or network
target = input("Enter the target host or network: ")

# Ask the user for the nmap timing template
timing = input("Enter the nmap timing template (0-5): ")

# Ask the user for the scan type
scan_type = input("Enter the scan type (sT, sU, sS, sA, sW, sM): ")

# Ask the user for the output format
output_format = input("Enter the output format (normal, csv, xml, grepable, all, none): ")

# Ask the user for the verbosity level
verbosity = input("Enter the verbosity level (0-9, with 9 being the most verbose): ")

# Build the arguments string
arguments = f"-{scan_type} --timing {timing} -v{verbosity}"
if output_format != "none":
    arguments += f" -o{output_format}"

# Perform a scan on the target with the specified options
print("Scanning...")
scanner.scan(target, arguments=arguments)

# Print the results of the scan
print("Hosts found:")
for host in scanner.all_hosts():
    print(host)
    print("Open ports:")
    for port in scanner[host]['tcp']:
        print(f"{port}: {scanner[host]['tcp'][port]['name']}")
