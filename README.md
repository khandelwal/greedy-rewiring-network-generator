## A Network Generator That Uses Greedy Rewiring

Starting with a regular random network, we use a greedy rewiring procedure to
gradually generate an exponentially distributed network. In particular, we
iteratively select a random edge in the network, and change its destination to
a new node (chosen in proportion to its degree). This process reduces the
degree of the original destination node and increases the degree of the new
destination node (which already had high degree), and thus progressively
increases the variance in the degree distribution.
