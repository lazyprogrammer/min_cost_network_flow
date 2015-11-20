from pulp import *


def lp_flow_value(infile):
    # initialize
    prob = LpProblem("myProblem", LpMinimize)
    node_demand_map = {}
    expression_to_minimize = []
    edge_counter = 1 # make sure each variable has a unique name since some edges appear twice

    # formulate the problem
    for line in open(infile):
        if line.startswith('c'):
            continue
            # comment line

        a = line.split()

        if len(a) < 1:
            continue
            # empty line

        if a[0] == 'p':
            # "problem line"
            # p min <nodes> <arcs>
            N = int(a[2])
            M = int(a[3]) # probably still irrelevant

        elif a[0] == 'n':
            # node line
            # n <id> <flow>
            # we'll consider <flow> to be the demand

            # we'll use these later to make the demand constraints
            node_demand_map[int(a[1])] = {
                'into': [],
                'outof': [],
                'demand': int(a[2])
            }

        elif a[0] == 'a':
            # edge line
            # a <v> <w> <low> <cap> <cost>
            v, w, low, cap, cost = [int(i) for i in a[1:]]

            # this creates the variable with a unique name
            # includes low and high constraints
            x = LpVariable("%s_%s_%s" % (v, w, edge_counter), low, cap)

            # add to expression to minimize
            expression_to_minimize.append(cost*x)

            # add to node_demand_map to make demand constaints later
            # only nodes with demands were added by the 'n' tag
            # need to add the rest manually
            if w not in node_demand_map:
                node_demand_map[w] = {
                    'into': [],
                    'outof': [],
                    'demand': 0
                }
            if v not in node_demand_map:
                node_demand_map[v] = {
                    'into': [],
                    'outof': [],
                    'demand': 0
                }
            node_demand_map[w]['into'].append(x)
            node_demand_map[v]['outof'].append(x)

            edge_counter += 1


    for node, data in node_demand_map.iteritems():
        prob += (sum(data['into']) - sum(data['outof']) == data['demand'])

    # add expression to minimize
    prob += sum(expression_to_minimize)

    # solve and return min-cost
    status = prob.solve()
    print LpStatus[status]
    return value(sum(expression_to_minimize))



print "Correct value for _40 instance:", lp_flow_value('gte_bad.40') == 52099553858
print "Correct value for _6830 instance:", lp_flow_value('gte_bad.6830') == 299390431788
print "Correct value for _176280 instance:", lp_flow_value('gte_bad.176280') == 510585093810