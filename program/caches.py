from m5.objects import Cache

class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def __init__(self, options=None):
        super().__init__()
        pass

    def connectCPU(self, cpu):
        # need to define this in a base class!
        raise NotImplementedError

    def connectToMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports


class L1ICache(L1Cache):
    size = "16kB"

    def __init__(self, options=None):
        super().__init__(options)
        if not options or not options.l1i_size:
            return
        self.size = options.l1i_size

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port


class L1DCache(L1Cache):
    size = "64kB"

    def __init__(self, options=None):
        super().__init__(options)
        if not options or not options.l1d_size:
            return
        self.size = options.l1d_size

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port


class L2Cache(Cache):
    size = "256kB"
    assoc = 8
    tag_latency = 6
    data_latency = 6
    response_latency = 6
    mshrs = 10
    tgts_per_mshr = 12

    def __init__(self, options=None):
        super().__init__()
        if not options or not options.l2_size:
            return
        self.size = options.l2_size

    def connectCPU(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports


class L3Cache(Cache):
    size = "32MB"
    assoc = 16
    tag_latency = 11
    data_latency = 12.5
    response_latency = 12.5
    mshrs = 20
    tgts_per_mshr = 12
    clusivity="mostly_excl"

    def __init__(self, options=None):
        super().__init__()
        if not options or not options.l3_size:
            return
        self.size = options.l3_size

    def connectCPU(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports