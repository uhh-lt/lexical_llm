import yaml
import matplotlib.pyplot as plt
import sys
from tqdm import tqdm
import pickle
import numpy as np
import networkx as nx

def clean_dict(pairs, use_lemma, reverse):
    new_pairs = {}
    for key, val in pairs.items():
        if use_lemma:
            term = key[0].split("(")[0].strip()
        else:
            term = key[0]
        target = key[1].split(",")[0]
        new_key = (target, term) if reverse else (term, target)
        new_pairs[new_key] = val

    return new_pairs


def iterative_child(ppl_pairs, low, high, step, max_iter):
    thrs = np.arange(low, high, step)
    Fs = []
    for thr in tqdm(thrs):
        tb = TaxonomyBuilder(root, all_verteces, max_iter)
        tb.build_taxonomy("ppl_thr_collector", ppl_pairs=ppl_pairs, thr=thr)
        edges = tb.all_edges

        P = len(set(G.edges()) & set(edges)) / (len(set(edges)) + 1)
        R = len(set(G.edges()) & set(edges)) / len(set(G.edges()))
        F = (2 * P * R) / (P + R + 1e-15)

        #  print('precision: {} \n recall: {} \n F-score: {}'.format(P,R,F))
        Fs.append(F)

    print(max(Fs), thrs[np.argmax(Fs)])
    plt.plot(thrs, Fs)
    return Fs


def brute_child(ppl_pairs, low, high, step):
    thrs = np.arange(low, high, step)
    Fs = []
    for thr in tqdm(thrs):
        edges = []
        for key, val in ppl_pairs.items():
            if val < thr:
                edges.append(key)

        P = len(set(G.edges()) & set(edges)) / (len(set(edges)) + 1e-15)
        R = len(set(G.edges()) & set(edges)) / len(set(G.edges()))
        # print(len(set(edges)))
        F = (2 * P * R) / (P + R + 1e-15)

        Fs.append(F)

    print(max(Fs), thrs[np.argmax(Fs)])
    plt.plot(thrs, Fs)
    return Fs


with open(r"./configs/build_taxo.yml") as file:
    params_list = yaml.load(file, Loader=yaml.FullLoader)


if __name__ == "__main__":
    data = params_list["DATA"][0]
    in_name = params_list["IN_NAME"][0]
    reverse = params_list["REVERSE"][0]
    lemma = params_list["LEMMA"][0]
    low = params_list["LOW"][0]
    high = params_list["HIGH"][0]
    step = params_list["STEP"][0]

    if data == "food":
        path = "gs_taxo/EN/" + str(data) + "_wordnet_en.taxo"
    else:
        path = "gs_taxo/EN/" + str(data) + "_eurovoc_en.taxo"
    G = nx.DiGraph()

    with open(path, "r") as f:
        for line in f:
            idx, hypo, hyper = line.split("\t")
            hyper = hyper.replace("\n", "")
            G.add_node(hypo)
            G.add_node(hyper)
            G.add_edge(hyper, hypo)

    with open(in_name, "rb") as f:
        ppls = pickle.load(f)

    ppls_pairs = clean_dict(ppls, use_lemma=lemma, reverse=reverse)

    root = data
    all_verteces = list(G.nodes)
    all_verteces.remove(root)

    res = brute_child(ppls_pairs, low=low, high=high, step=step)
    print(res)