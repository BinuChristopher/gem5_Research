import argparse
from caches import *
import m5
from m5.objects import *
from gem5.resources.resource import Resource

parser = argparse.ArgumentParser(
    description="A simple system with 2-level cache."
)
parser.add_argument(
    "binary",
    default="",
    nargs="?",
    type=str,
    help="Path to the binary to execute.",
)
parser.add_argument(
    "--l1i_size", help=f"L1 instruction cache size. Default: 16kB."
)
parser.add_argument(
    "--l1d_size", help="L1 data cache size. Default: Default: 64kB."
)
parser.add_argument("--l2_size", help="L2 cache size. Default: 256kB.")

options = parser.parse_args()

system = System()

binary = "/home/binu/Gem5/gem5_v23.1/program/simple"

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

num_cpus = 2
system.cpu = [X86TimingSimpleCPU() for i in range(num_cpus)]

# Set up the cache hierarchy
system.l1dcache = [L1DCache(options) for i in range(num_cpus)]
system.l1icache = [L1ICache(options) for i in range(num_cpus)]

system.l2bus = L2XBar()

system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)
system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)

system.system_port = system.membus.cpu_side_ports

# Memory
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports


# Set the command
# cmd is a list which begins with the executable (like argv)

# process = Process(executable=binary, cmd=[binary, str(num_cpus)])

process = Process(executable=binary, cmd=[binary, str(num_cpus)])
system.multi_thread = True

for i in range(num_cpus):
    system.cpu[i].workload = process
    system.cpu[i].createThreads()

    system.l1dcache[i].connectCPU(system.cpu[i])
    system.l1icache[i].connectCPU(system.cpu[i])
    system.l1dcache[i].connectToMemSideBus(system.l2bus)
    system.l1icache[i].connectToMemSideBus(system.l2bus)

    system.cpu[i].createInterruptController()
    system.cpu[i].interrupts[0].pio = system.membus.mem_side_ports
    system.cpu[i].interrupts[0].int_requestor = system.membus.cpu_side_ports
    system.cpu[i].interrupts[0].int_responder = system.membus.mem_side_ports


system.workload = SEWorkload.init_compatible(binary)


root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()

print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
