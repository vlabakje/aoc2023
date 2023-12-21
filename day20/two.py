import queue
import math

def main(filename):
    with open(filename) as fileh:
        sim = Simulator(fileh.read().strip())
        return sim.simulate()
        #print(f"{low=} {high=}")
        return low * high

class Simulator:
    output_strings = []
    name = "output"
    high = 0
    low = 0

    def __init__(self, data):
        self.modules = {"output": self}
        for line in data.split("\n"):
            name, _, outputs = line.strip().partition(" -> ")
            match name[0]:
                case "%":
                    self.modules[name[1:]] = FlipFlop(name[1:], outputs.split(", "))
                case "&":
                    self.modules[name[1:]] = Conjunction(name[1:], outputs.split(", "))
                case _:
                    self.modules[name] = Module(name, outputs.split(", "))
        # fix dead ends
        self.modules["rx"] = Sink("rx", [])
        [m.register(self.modules) for m in self.modules.values()]
        #print(self.modules)

    def output_vis(self):
        import pyvis
        net = pyvis.network.Network(directed=True)
        nodetypes = {Conjunction: "square", FlipFlop: "triangle"}
        [net.add_node(m.name, shape=nodetypes.get(m.__class__, "dot")) for m in self.modules.values()]
        for m in self.modules.values():
            if hasattr(m, "outputs"):
                for out in m.outputs:
                    net.add_edge(m.name, out.name)
        #net.toggle_physics(True)
        net.show("net.html", notebook=False)

    def simulate(self, n=1000):
        # build a graph
        self.output_vis()
        # there are four clusters on the graph
        # each is a binary counter
        # looking at the arrow directions for each FlipFlop attached to a Conjunction
        # you can determine wheter that needs to be a 1 or 0
        # for a 1 it's an output to the Conjuction, for a 0 an input from
        # read clusters from graph:
        km = int("101001001111"[::-1], 2)
        vk = int("100110111111"[::-1], 2)
        pk = int("100111010111"[::-1], 2)
        xt = int("111000001111"[::-1], 2)
        # the answer is multiplying them together
        return km*vk*pk*xt

    def press(self, signal):
        # print(f"press {signal}")
        self.low += 1
        self.outputs = []
        q = queue.Queue()
        q.put((None, self.modules["broadcaster"], signal))
        while not q.empty():
            source, module, signal = q.get()
            for out, newsig in module.pulse(source, signal):
                # print(f"{module.name} -{'high' if newsig else 'low'}-> {out.name}")
                q.put((module, out, newsig))
        return self.outputs

    def register(self, _):
        pass

    def pulse(self, source, signal):
        self.outputs.append(signal)
        if False:
            yield None

class Module:
    def __init__(self, name, outputs):
        self.name = name
        self.output_strings = outputs
        self.outputs = []
        self.high = 0
        self.low = 0

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.name}>"
    
    def register(self, modules):
        for out in self.output_strings:
            self.outputs.append(modules[out])

    def pulse(self, source, signal):
        for output in self.outputs:
            if signal:
                self.high += 1
            else:
                self.low += 1
            yield output, signal

class Sink(Module):
    pass

class FlipFlop(Module):
    state = 0

    def pulse(self, source, signal):
        if signal == 0:
            self.state = 1 if self.state == 0 else 0
            yield from super().pulse(source, self.state)

class Conjunction(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.inputs = {}

    def register(self, modules):
        super().register(modules)
        for module in modules.values():
            if self.name in module.output_strings:
                self.inputs[module.name] = 0
                #print(self.name, self.inputs)

    def pulse(self, source, signal):
        #print(self.name, self.inputs, source.name, signal)
        self.inputs[source.name] = signal
        yield from super().pulse(source, 1 if 0 in self.inputs.values() else 0)

    def __repr__(self):
        return f"{super().__repr__()} {','.join(o.name for o in self.outputs)} {self.inputs}"

if __name__ == "__main__":
    print("===")
    #print(main("example"))
    #print(main("example2"))
    print(main("input"))
