import networkx as nx

def create_graph(infile):
    """Creates a directed graph as specified by the input file. Edges are annotated with 'capacity'
    and 'weight' attributes, and nodes are annotated with 'demand' attributes.
    
    Args:
        infile: the input file using the format to specify a min-cost flow problem.
        
    Returns:
        A directed graph (but not a multi-graph) with edges annotated with 'capacity' and 'weight' attributes
        and nodes annotated with 'demand' attributes.
    """
    
    G = nx.DiGraph()
    sum_demands = 0
    edge_data = {} # key (node1, node2) : value { 'c': #, 'w': # }

    for line in open(infile):
        if line.startswith('c'):
            continue

        a = line.split()

        if len(a) < 1:
            continue
            # not sure

        

        N = -1
        M = -1 # irrelevant
        if a[0] == 'p':
            # "problem line"
            # p min <nodes> <arcs>
            N = int(a[2])
            M = int(a[3])

        elif a[0] == 'n':
            # node line
            # n <id> <flow>
            # we'll consider <flow> to be the demand
            G.add_node(int(a[1]), demand=int(a[2]))
            sum_demands += int(a[2])

        elif a[0] == 'a':
            # edge line
            # a <v> <w> <low> <cap> <cost>
            # luckily <low>, lower bound for capacity, is always 0
            # not an input into nx
            # G.add_edge(int(a[1]), int(a[2]), capacity=int(a[4]), weight=int(a[5]))
            edge = (int(a[1]), int(a[2]))
            if edge not in edge_data:
                edge_data[edge] = []
            # else:
            #     print "an edge appeared twice!", edge

            edge_data[edge].append({ 'c': int(a[4]), 'w': int(a[5]) })

    # print "edge data", edge_data

    # now add the edges
    for edge, data in edge_data.iteritems():
        if len(data) == 1:
            # just add the edge directly
            G.add_edge(edge[0], edge[1], capacity=data[0]['c'], weight=data[0]['w'])
        else:
            counter = 1 # ensure unique names
            for d in data:
                # we have to create new nodes, ensure they have unique names
                node1 = "%s_%s" % (edge[0], counter)
                node2 = "%s_%s" % (edge[1], counter) # 1 -> 2
                # print "created new nodes:", node1, node2, d['c'], d['w']

                # add new nodes to the graph - they have 0 demand (default)
                G.add_node(node1)
                G.add_node(node2)

                # add edges with 0 cost and infinite capacity (this is the default)
                G.add_edge(edge[0], node1)
                G.add_edge(node2, edge[1])

                # add the weighted edges with capacity
                G.add_edge(node1, node2, capacity=d['c'], weight=d['w'])

                counter += 1


    # print "sum demands:", sum_demands # check = 0
    return G






G_40 = create_graph('gte_bad.40')
G_6830 = create_graph('gte_bad.6830')
G_176280 = create_graph('gte_bad.176280')

# print nx.min_cost_flow_cost(G_40)

print "Correct value for _40 instance:", nx.min_cost_flow_cost(G_40) == 52099553858
print "Correct value for _6830 instance:", nx.min_cost_flow_cost(G_6830) == 299390431788
print "Correct value for _176280 instance:", nx.min_cost_flow_cost(G_176280) == 510585093810