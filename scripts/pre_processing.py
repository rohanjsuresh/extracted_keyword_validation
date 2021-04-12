from keyword_relation.models import Keyword_Pages

from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf.urls.static import static
import os
from django.conf import settings
import numpy as np
import random
from gensim.models import Word2Vec
import wikipedia
import networkx as nx
import random
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from nltk.corpus import wordnet
import pandas

import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia('en')

def run():

    print("START")


    # Get all keywords
    all_keywords = Keyword_Pages.objects.all()

    # count
    count = 0

    # iterate over all keywords
    for keyword in all_keywords:

        count += 1
        if count % 1000 == 0:
            print(count)

        # get model datamodels
        if keyword.google_graph_embedding == "":
            model_path = os.path.join(settings.STATIC_ROOT,'../models/related_keywords_graph_embedding.model')
            model = Word2Vec.load(model_path)

            related_main = find_similar_keywords(model, keyword.keyword)

            keyword.google_graph_embedding = related_main
            keyword.save()

        # get wiki path
        if keyword.wiki_path == "":
            print("Finding path for", keyword.keyword)
            visited = set()
            wiki_paths = wiki_bfs(keyword.keyword, "Glossary of computer science", visited, 0, [], 100)
            wiki_path = get_probability_score(wiki_paths)


            if wiki_path == "N/A":
                wiki_path_str = wiki_path
            else:
                first = True
                wiki_path_str = ""
                for val in wiki_path:
                    if first:
                        wiki_path_str += val
                        first = False
                    else:
                        wiki_path_str += " --> " + val
                
                print(wiki_path_str)

            keyword.wiki_path = wiki_path_str
            keyword.save()


def wiki_bfs(source, target, visited, num_found, found_paths, iter_limit):
    queue = []
    visited.add(source)
    queue.append([source])
    iter_count = 0
    output = []
    while len(queue) > 0 and iter_count <= iter_limit:
        iter_count += 1
        path_attempt = queue.pop(0)
        v = path_attempt[-1]
        if v == target.lower():
            if path_attempt not in output:
                output.append(path_attempt)
#                 print(output)
#                 for val in path_attempt:
#                     try:
#                         visited.remove(val)
#                     except:
#                         pass
                visited.remove(target.lower())
                iter_count = 0
            if len(output) == 3:
                # print("hit")
                return output
        try:
            v = wiki_wiki.page(v)
        except:
            continue
        edges = [x.lower() for x in v.links]
        index_push = 0
        for edge in edges:
            if (edge in target.lower() or target.lower() in edge) and edge not in visited:
                visited.add(edge)
                new_path_attempt = path_attempt[:]
                new_path_attempt.append(edge)
                if edge == target.lower():
                    queue.insert(0, new_path_attempt)
                    index_push += 1
                queue.insert(index_push, new_path_attempt)
#                 print(queue)
        
        for edge in edges:
            if edge not in visited:
                visited.add(edge)
                new_path_attempt = path_attempt[:]
                new_path_attempt.append(edge)
                queue.append(new_path_attempt)
    # print("out", iter_count)
    # print(len(queue))
    return output


def get_probability_score(path):

    if path == []:
        return "N/A"

    all_probs = []
    for i in range(len(path)):
        probabilities_path = []
        for val in path[i]:
            probabilities = 1/(len(wiki_wiki.page(val).links))
            probabilities_path.append(probabilities)
        all_probs.append((sum(probabilities_path), path[i]))

    all_probs.sort(key = lambda x: x[0])  
    return all_probs[0][1]

# function to get related keywords
def find_similar_keywords(model, x):
    output = ""
    first = True
    try:
        count = 0
        for node, _ in model.wv.most_similar(x):
            if first:
                output += node
                first = False 
            else:
                output += "|" + node
            count += 1
            if count >=5:
                break
    except:
        # print(x, "not in graph")
        output="NA"
    return output