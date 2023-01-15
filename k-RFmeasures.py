import functions
import argparse
import json
"""
k-RFmeasures.py computes pairwise k-RF scores of all (rooted) trees in an input file in which each tree is represented by its (directed) edges.
By default, it considers trees as unrooted trees.
For unrooted trees, the command line is 'python3 k-RFmeasures.py inputfile k', and for rooted trees, it is 'python3 k-RFmeasures.py -r inputfile k'.
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find pairwise k-RF scores of a set of trees.')
    parser.add_argument('inputfile')
    parser.add_argument('k')
    parser.add_argument('-r', '--rooted', action='store_true')
    args = parser.parse_args()
    tree_file = open(args.inputfile)
    trees=functions.gettrees(tree_file)
    partitions=functions.getpartitions(trees, int(args.k))
    if args.rooted:
        pairwise_distances=functions.getkRFmeasure_rooted(partitions)
    else:
        pairwise_distances=functions.getkRFmeasure_unrooted(partitions)
    with open("pairwise_distances", "w") as fp:
       json.dump(pairwise_distances, fp)
       
