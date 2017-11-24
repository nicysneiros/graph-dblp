from py2neo import Graph, Node, Relationship, NodeSelector
from py2neo.packages.httpstream import http

http.socket_timeout = 9999

def get_dim_value(node, attributes):
    dim_value_list = []
    for attribute in attributes:
        dim_value_list.append(node[attribute])
    return tuple(dim_value_list)

original_graph = Graph(http_port=7476, password="admin")
original_graph_selector = NodeSelector(original_graph)

aggregated_graph = Graph(http_port=7480, password="admin")

aggregated_nodes = []
non_aggregated_nodes = []
relationships = []

dimensions = [(['year'], 'Publication')]

# Example dim_value = (2007, SIGMOD)

for attributes, label in dimensions:
    original_nodes = original_graph_selector.select(label)

    i = 0
    for original_node in original_nodes:
        i = i + 1
        print "Checking {}".format(i)
        dim_value = get_dim_value(original_node, attributes)
        agg_node_list = [node for node in aggregated_nodes if node['dim_value'] == dim_value]

        if len(agg_node_list) > 0:
            agg_node = agg_node_list[0]
            agg_node['measure'] = agg_node['measure'] + 1
        else:
            agg_node = Node("Aggregated_Publication", dim_value=dim_value, measure=1)
            aggregated_nodes.append(agg_node)

        original_rel_nodes = original_graph.match(rel_type="PUBLISHED", end_node=original_node)
        for original_rel in original_rel_nodes:

            start_node = original_rel.start_node() #Author of the publication
            non_agg_node_list = [node for node in non_aggregated_nodes if dict(node) == dict(start_node)]

            if len(non_agg_node_list) > 0:
                non_agg_node = non_agg_node_list[0]
            else:
                non_agg_node = Node(*list(start_node.labels()), **dict(start_node))
                non_aggregated_nodes.append(non_agg_node)

            exists_rel = False
            for rel in relationships:
                rel_start_node = rel.start_node()
                rel_end_node = rel.end_node()

                if non_agg_node == rel_start_node and agg_node == rel_end_node:
                    rel['measure'] = rel['measure'] + 1
                    exists_rel = True

            if not exists_rel:
                agg_rel = Relationship(non_agg_node, "PUBLISHED", agg_node, measure=1)
                relationships.append(agg_rel)

tx = aggregated_graph.begin()
for agg_node in aggregated_nodes:
    tx.create(agg_node)
tx.commit()

tx = aggregated_graph.begin()
for non_agg_node in non_aggregated_nodes:
    tx.create(non_agg_node)
tx.commit()

i = 0
for agg_rel in relationships:
    i += 1
    try:
        tx = aggregated_graph.begin()
        tx.create(agg_rel)
        tx.commit()
        print "Created Relationship ", i
    except:
        print "Start Node: ", agg_rel.start_node()
        print "End Node: ", agg_rel.end_node()
        print "Measure: ", agg_rel['measure']

                


