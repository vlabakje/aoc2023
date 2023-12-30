import collections
import dataclasses
import itertools
import random

@dataclasses.dataclass
class Node:
    name: str
    conn: list

def main(filename):
    with open(filename) as fileh:
        nodes = node_dict(fileh.read().strip())
        keys = list(nodes.keys())
        #for k, v in nodes.items():
        #    print(k, v.name, len(v.conn))
        c = collections.Counter()
        for _ in range(100):
            start, end = random.choices(keys, k=2)
            p = dijkstra(nodes, start, end)
            c.update(tuple(sorted(x)) for x in itertools.pairwise(p))
        disconnect(nodes, (x[0] for x in c.most_common(3)))
        n = group_size(nodes, keys[0])
        return n * (len(keys) - n)

def group_size(nodes, n):
    seen = set((n, ))
    unseen = [n]
    while len(unseen):
        n = unseen.pop()
        for x in nodes[n].conn:
            if x.name not in seen:
                seen.add(x.name)
                unseen.append(x.name)
    return len(seen)

def disconnect(nodes, common):
    for start, end in common:
        # print(f"remove {start=} {end=}")
        nodes[start].conn.remove(nodes[end])
        nodes[end].conn.remove(nodes[start])

def node_dict(data):
    out = {}
    for line in data.split("\n"):
        node, *conn = line.replace(":", "").split()
        if node not in out:
            out[node] = Node(node, [])
        for c in conn:
            if c not in out:
                out[c] = Node(c, [])
            if out[c] not in out[node].conn:
                out[node].conn.append(out[c])
            if out[node] not in out[c].conn:
                out[c].conn.append(out[node])
    return out

def dijkstra(nodes, start, end):
    unvisited_nodes = set(nodes.keys()) | set([start, end])
    shortest_path = dict((n, 2**32) for n in nodes.keys())
    shortest_path[start] = 0
    previous_nodes = {}
    while len(unvisited_nodes):
        lowest = end
        for node in unvisited_nodes:
            if shortest_path[node] < shortest_path[lowest]:
                lowest = node
        if lowest == end:
            break
        for neigh in nodes[lowest].conn:
            path_len = shortest_path[lowest] + 1
            if path_len < shortest_path[neigh.name]:
                shortest_path[neigh.name] = path_len
                previous_nodes[neigh.name] = lowest
        unvisited_nodes.remove(lowest)
    path = [end]
    while path[-1] != start:
        path.append(previous_nodes[path[-1]])
    return path

if __name__ == "__main__":
    print(main("example"))
    print(main("input"))
