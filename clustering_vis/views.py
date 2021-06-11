from django.shortcuts import render
from django.shortcuts import HttpResponse
import pickle
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf.urls.static import static
import os
from django.conf import settings
import scipy.cluster
import functools
import numpy as np
import json
from django.core.management import call_command


# Create your views here.
def visualization(request):

    model_path = os.path.join(settings.STATIC_ROOT,'../models/agglomerative_clustering_83k.pkl')

    with open(model_path, 'rb') as input:
        model = pickle.load(input)

    corpus_path = os.path.join(settings.STATIC_ROOT,'../models/new_keywords_2.csv')

    file1 = open(corpus_path, 'r')
    Lines = file1.readlines()

    corpus_old = []

    for i in range(83000):
        corpus_old.append(Lines[i].strip())

    output = show_hierarchy(len(model.children_), model.children_, corpus_old)

    context = {}
    context["output"] = output
    context["max"] = len(model.children_)
    # context["num_iters"] = len(model.children_)
    context["num_iters"] = 5

    # context["dendogram_data"] = dendogram(model, corpus_old)
    # dendogram(model, corpus_old)

    return render(request, 'clustering_vis/visualization.html', context)

def iteration_input(request):

    model_path = os.path.join(settings.STATIC_ROOT,'../models/agglomerative_clustering_83k.pkl')

    with open(model_path, 'rb') as input:
        model = pickle.load(input)

    corpus_path = os.path.join(settings.STATIC_ROOT,'../models/new_keywords_2.csv')

    file1 = open(corpus_path, 'r')
    Lines = file1.readlines()

    corpus_old = []

    for i in range(83000):
        corpus_old.append(Lines[i].strip())

    # get user input
    num_iters = int(request.POST.get("iter_count"))

    output = show_hierarchy(num_iters, model.children_, corpus_old)

    context = {}
    context["output"] = output
    context["max"] = len(model.children_)
    context["num_iters"] = num_iters
    # context["dendogram_data"] = dendogram(model, corpus_old)
    # dendogram(model, corpus_old)
    return render(request, 'clustering_vis/visualization.html', context)


def show_hierarchy(iteration, children, corpus):
    if iteration > len(children):
        return "N/A"
    else:
        
        clusters = {}
        n_sample = len(children)+1
        curr_sample = len(children)+1
        for i in range(iteration):
            found = False
            # if both are less than n_sample directly add to clusters (no merge)
            if children[i][0] < n_sample and children[i][1] < n_sample:
                clusters[curr_sample] = [children[i][0], children[i][1]]
                curr_sample += 1
            
            # if one is less than n_sample create new cluster with new value
            elif children[i][0] >= n_sample and children[i][1] < n_sample:
                clusters[curr_sample] = clusters[children[i][0]] + [children[i][1]]
                clusters.pop(children[i][0], 'None')
                curr_sample += 1
            elif children[i][0] < n_sample and children[i][1] >= n_sample:
                clusters[curr_sample] = clusters[children[i][1]] + [children[i][0]]
                clusters.pop(children[i][1], 'None')
                curr_sample += 1
                
            # if both are greater than n_sample tghen merge clusters
            elif children[i][0] >= n_sample and children[i][1] >= n_sample:
                clusters[curr_sample] = clusters[children[i][0]] + clusters[children[i][1]]
                clusters.pop(children[i][0], 'None')
                clusters.pop(children[i][1], 'None')
                curr_sample += 1
                
    output = ""
    for key in clusters.keys():
#         print("Key", key)
#         print([corpus_old[x] for x in clusters[key]])
#         print("\n")
        
        x = [corpus[x] for x in clusters[key]]
        first = True
        for val in x:
            if first:
                output += val
                first = False
            else:
                output += ", " + val
        output += "|"
        
    return output
    

def dendogram(model, corpus_old):
    print("Dendogram start")
    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    clusters = np.column_stack([model.children_, model.distances_,
                                        counts]).astype(float)

    labels = corpus_old
    id2name = dict(zip(range(len(labels)), labels))


    # Create a nested dictionary from the ClusterNode's returned by SciPy
    def add_node(node, parent ):
        # First create the new node and append it to its parent's children
        newNode = dict( node_id=node.id, children=[] )
        parent["children"].append( newNode )

        # Recursively add the current node's children
        if node.left: add_node( node.left, newNode )
        if node.right: add_node( node.right, newNode )

    T = scipy.cluster.hierarchy.to_tree( clusters , rd=False )
    d3Dendro = dict(children=[], name="Root1")
    add_node( T, d3Dendro )

    # Label each node with the names of each leaf in its subtree
    def label_tree( n ):
        # If the node is a leaf, then we have its name
        if len(n["children"]) == 0:
            leafNames = [ id2name[n["node_id"]] ]

        # If not, flatten all the leaves in the node's subtree
        else:
            leafNames = functools.reduce(lambda ls, c: ls + label_tree(c), n["children"], [])

        # Delete the node id since we don't need it anymore and
        # it makes for cleaner JSON
        del n["node_id"]

        # Labeling convention: "-"-separated leaf names
        n["name"] = name = "-".join(sorted(map(str, leafNames)))

        return leafNames

    label_tree( d3Dendro["children"][0] )
    print("Dumping")
    print(len(d3Dendro))
    # Output to JSON
    # json.dump(d3Dendro, open("../models/d3-dendrogram.json", "w"), sort_keys=True, indent=4)
    # file1 = open("../models/d3-dendrogram.json", 'w')
    # # Writing a string to file
    # file1.write(d3Dendro)

    # # Closing file
    # file1.close()

    print("Dendogram end")
    return d3Dendro
