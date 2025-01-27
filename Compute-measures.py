# Using NetworkX package and conllu package
import os
from io import open
from conllu import parse
import networkx as nx
from operator import itemgetter
from Measures import  Compute_measures
import random
import treegen as gen


directory = "./SUD"                   # directory containing the UD scheme tree files in CONLLU format
ud_files = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.conllu'):
            fullpath = os.path.join(root, file)
            ud_files.append(fullpath)            # creates a list of path of all files (file of each language) from the directory

for i in ud_files:                                       # reads file of each language one by one
    lang = str(i)
    dfile = open(lang,'r',encoding='utf-8')
    data_file=dfile.read()
    sentences = []
    #sentences = parse(data_file)                         # parses the CONLLU format
    sent_id=0
    print(lang)
    num_sent=0
    num_edge=0
    sentences = data_file.split('\n\n')
    print(sentences)
    for sentence in sentences:
        sent_id += 1
        lines = sentence.strip().split('\n')
        tree = nx.DiGraph()
        for line in lines:
            if line.startswith('#'):
                continue
            parts = line.split('\t')
            print(parts)
            node_id = parts[0]
            if len(parts)>5:
                if not parts[6]=='punct':
                    tree.add_node(int(node_id), form=parts[1], lemma=parts[2], upostag=parts[3], xpostag=parts[4], head=int(parts[5]), deprel=parts[6])                #adds node to the directed graph
        ROOT=0
        tree.add_node(ROOT)                            # adds an abstract root node to the directed graph

        for nodex in tree.nodes:
            if not nodex==0:
                if tree.has_node(tree.nodes[nodex]['head']):                                         # to handle disjoint trees
                    tree.add_edge(tree.nodes[nodex]['head'],nodex,drel=tree.nodes[nodex]['deprel'])       # adds edges as relation between nodes
        print(tree.edges)
        n=len(tree.edges)
        if n<30 and n>1:
            get = Compute_measures(tree)
            #Computes the measures for the real tree
            projection_degree_real=get.projection_degree(0)          # gives the projection degree of the tree i.e., size of longest projection chain in the tree
            sent_len=0
            for edgey in tree.edges:
                if not edgey[0]==0:
                    direction_real = get.dependency_direction(edgey)    # direction of the edge in terms of relative linear order of head and its dependent
                    dep_distance_real=get.dependency_distance(edgey)    # gives the distance between nodes connected by an edge
                    dep_depth_real=get.dependency_depth(edgey)
                    
                    
                    #print(dep_distance_real)
                    results2 = open('English-measures.csv','a')
                    results2.write(str(lang)+"\t"+"real"+"\t"+str(sent_id)+"\t"+str(n)+"\t"+str(projection_degree_real)+"\t"+str(edgey)+"\t"+str(direction_real)+"\t"+str(dep_distance_real)+"\t"+str(dep_depth_real)+"\n")
                    results2.close()
                print("\n-----------------\n"+str(tree.edges))
                # Assuming 'tree' is your NetworkX DiGraph with the appropriate structure
