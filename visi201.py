from tries import *
from tree import *
from dicoCondense import *
from suffixArray import *

from random import randint
from time import time

def parseTests(name = "tests.txt") -> list:
    tests = []
    file = open(name, "r")
    ligne = file.readline()
    while ligne != "":
        t = {}
        t["mot"] = ligne[:-1]
        t["cherche"] = file.readline()[:-1]
        ligne = file.readline()
        t["res"] = ligne[:-1] if ligne[-1] == "\n" else ligne
        tests += [t]
        ligne = file.readline()
    file.close()
    return tests

def executerTests(tests: list, debut: int = 0, fin: int = -1) -> list:
    fn = [test_tree, test_tree2]
    res = []
    
    if fin == -1:
        fin = len(tests)
    if debut <= fin:
        t = time()
        for i in range(debut, fin):
            test = tests[i]
            mot = test["mot"]
            cherche = test["cherche"]
            v = [fn[i](mot, cherche) for i in range(len(fn))]
            v += [test["res"]]
            res += [v]
    return res

def sauvegarderResultats(resultats: list):
    file = open("resultats.txt", "w")
    i = 0
    while i < len(resultats):
        r = resultats[i]
        file.write("-"*30 + "\n")
        file.write("Test - " + str(i) + "\n")
        for j in range(len(r) - 1):
            file.write(str(r[j]) + "\n")
        file.write(str(r[-1]) + "\n")
        file.write("-"*30 + "\n")
        i += 1
    file.close()


def test_tries(mot: str, cherche: str) -> list:
    return test_structure(mot, cherche, convertion_tries, est_dans_tries)

def test_tree(mot: str, cherche: str) -> list:
    return test_structure(mot, cherche, convertion_tree, est_dans_tree)

def test_tree2(mot: str, cherche: str) -> list:
    return test_structure(mot, cherche, convertion_tree2, est_dans_tree)

def test_dico_condense(mot: str, cherche: str) -> list:
    return test_structure(mot, cherche, convertion_dico_condense, est_dans_dico_condense)

def test_suffix_array(mot: str, cherche: str) -> list:
    return test_structure(mot, cherche, convertion_suffix_array2, est_dans_suffix_array)

def test_structure(mot: str, cherche: str, convertionFn, rechercheFn) -> list:
    t = time()
    struct = convertionFn(mot)
    d = time()
    tps_construction = d - t
    
    estDans = rechercheFn(struct, cherche)
    t = time()
    tps_recherche = t - d

    return [tps_construction, tps_recherche, estDans]

#tests = parseTests()
#resultats = executerTests(tests, 8, fin=10)
#sauvegarderResultats(resultats)

#s = "abrabxabr"
#s = "bonjour à tous et à toutes les amis !"
#t = convertion_tree2(s)
#print(convertion_tree2(s)[1])
#print("b-")
#print(convertion_tree(s)[1])
#print("-"*20)


#m = {(0, 1): {(1, 1): {(2, 4): {}, (5, 1): {}}}, (1, 1): {(2, 4): {}, (5, 1): {}}, (2, 4): {}, (5, 1): {}}
#ajouter_arbre2(m, 7, s)
#print(m)

#print(est_dans_tree(t, "tou"))


#to_write = ""
#tailles = [10, 100, 1000, 10000, 100000, 1000000]
#tailles = [i for i in range(1, 10001)]
#for t in tailles:
#    n = [str(randint(1, 4)) for i in range(t)]
#    ch = "".join(n)
#    i = randint(0, t - 1)
#    c = ch[i // 2:i]
#    to_write += "\n" + ch + "\n"
#    to_write += c + "\n"
#    to_write += "True"
#f = open("bonjour.txt", "w")
#f.write(to_write)
#f.close()

#c = open("c.txt", "r+").read()
#c = "bonjour"
#a = convertion_suffix_array2(c)
#print("a")
#t = sa_en_bw(a)
#print("b")
#ap = bw_en_sa(t)
#print("c")
#print(ap == a)

# ch = open("c.txt", "r+").read()
# t = convertion_suffix_array2(ch)
# print(t[1])

#sa = convertion_suffix_array2("abracadabradad")
#print(sa)


def trieToLatex(trie: dict) -> str:
    res = ""
    keys = list(trie.keys())
    for k in keys:
        t = trie[k]
        res += "[{" + k + "}"
        if t != {}:
            res += trieToLatex(t)
        res += "]"
    return res

def stToLatex(mot: str, arbre: dict) -> str:
    res = ""
    keys = list(arbre.keys())
    for k in keys:
        sa = arbre[k]
        #res += "[{}, edge label={node[midway, sloped, above] {" + mot[k[0] : k[0] + k[1]] + "}}"
        res += "[{}, edge label={node[midway, sloped, above] {" + str(k) + "}}"
        if sa != {}:
            res += stToLatex(mot, sa)
        res += "]"
    return res

def saToLatex(mot: str, sa: list) -> tuple:
    suffixs = ""
    indices = ""
    for j in range(len(sa)):
        i = sa[j]
        suffixs += str(j) + "/" + mot[i:].replace(EOS, "\\$") + ","
        indices += str(i) + " & "
    return (suffixs[:-1], indices[:-3])

def bwToLatex(mot: str, sa: list) -> tuple:
    tab = ""
    c = "c| " + " ".join( ["c" for i in range(len(mot) - 2)] ) + "|"

    for i in sa:
        tab += (" & ".join( mot[i:] + mot[:i] ) + "\\\\" ).replace(EOS, "\\textcolor{red}{\\$}")
    return (tab[:-2], c)

#chaine = "bananas"

#trie = convertion_tries(chaine)
#print(trie["a"]["b"])
#print(trieToLatex(trie))

#st = convertion_tree(chaine)
#print( stToLatex(st[0], st[1]) )

#sa = convertion_suffix_array2(chaine)
#latex = saToLatex(sa[0], sa[1])
#print(latex[0])
#print("\n")
#print(latex[1])

#latex = bwToLatex(sa[0], sa[1])
#print(latex[0])
#print("\n")
#print(latex[1])

#bw = sa_en_bw(sa)
#bw_en_sa(bw)

import gc

def generation_stats():
    fonctions = [("trie", convertion_tries, est_dans_tries, 1), ("tree", convertion_tree, est_dans_tree, 1), ("sa1", convertion_suffix_array2, est_dans_suffix_array, 985)]
    tests = parseTests("f.txt")
    res = {}
    for f in fonctions:
        res[f[0]] = {}

    for t in tests:
        for f in fonctions:
            if f[3] != 0 and f[3] < len(t["mot"]):
                continue
            print("Test " + f[0] + " - " + str(len(t["mot"])))
            res_test = test_structure(t["mot"], t["cherche"], f[1], f[2])
            res_f = res[f[0]]
            res_f[len(t["mot"])] = {"const": res_test[0], "rech": res_test[1], "tr": len(t["cherche"])}
            
            del res_f
            gc.collect()
    
    to_write = ""
    for f in res.keys():
        to_write += ("-"*20) + "\n" + f + "\n"
        vals_f: dict = res[f]
        for t in vals_f.keys():
            v = vals_f[t]
            #to_write += str(t) + "\n"
            #to_write += str(v["tr"]) + "\n"
            to_write += str(v["const"]) + "\n"
            #to_write += str(v["rech"]) + "\n"

    res_file = open("./stats.txt", "w")
    res_file.write(to_write.replace(".", ","))
    res_file.close()

generation_stats()

#tw = ""
#for i in range(1, 100000):
#    tw += "a"*i + "\na\nTrue\n"
#f = open("f.txt", "w")
#f.write(tw)
#f.close()