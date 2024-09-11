import matplotlib.pyplot as plt
import pprint

# Function to parse the stats file
def parse_stats(filename):
    stats = {}
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith("#") or line.strip() == "":
                continue
            try:
                # Strip out any trailing comments starting with '#'
                line = line.split("#")[0].strip()
            
            # Now split the remaining part of the line into key and value
                key, value = line.split(None, 1)  # Split by first whitespace occurrence

            # Remove any extra spaces around the value
                value = value.strip()
            # Store key-value pair after converting value to float
                stats[key] = float(value)
            except ValueError:
                continue
    return stats

# Parse the stats file
stats = parse_stats("m5out/stats.txt")

# Extract the values you want to plot
sim_insts = stats["simInsts"]
icache_hits = stats["system.l1dcache0.overallHits::total"]
dcache_misses = stats["system.l1dcache0.overallMisses::total"]

# Plot the results
labels = ['Instructions', 'I-Cache Hits', 'D-Cache Misses']
values = [sim_insts, icache_hits, dcache_misses]

plt.bar(labels, values)
plt.title("Simulation Statistics")
plt.ylabel("Count")
plt.savefig('plot.png')


